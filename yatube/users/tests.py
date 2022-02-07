from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from http import HTTPStatus


User = get_user_model()


class UsersURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')

    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_users_urls_exists_at_desired_location(self):
        """Проверка доступности user адресов."""
        addresses = {
            '/auth/signup/': HTTPStatus.OK,
            '/auth/login/': HTTPStatus.OK,
            '/auth/logout/': HTTPStatus.OK,
            '/auth/password_reset/': HTTPStatus.OK,
        }
        for address, status in addresses.items():
            response = self.guest_client.get(address)
            self.assertEqual(response.status_code, status)

    def test_user_urls_uses_correct_template(self):
        """Проверка шаблонов для user адресов."""
        templates_address_names = {
            '/auth/signup/': 'users/signup.html',
            '/auth/login/': 'users/login.html',
            '/auth/logout/': 'users/logged_out.html',
            '/auth/password_reset/': 'users/password_reset_form.html',
        }
        for address, template in templates_address_names.items():
            response = self.guest_client.get(address)
            self.assertTemplateUsed(response, template)

    def test_password_change_urls_exists_at_desired_location(self):
        """Проверка доступности password_change/."""
        response = self.authorized_client.get('/auth/password_change/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_change_urls_uses_correct_template(self):
        """Проверка шаблона для password_change/."""
        response = self.authorized_client.get('/auth/password_change/')
        self.assertTemplateUsed(response, 'users/password_change_form.html')

    def test_password_change_url_redirect_anonymous_on_auth_login(self):
        """Страница password_change/ перенаправит анонимного
         пользователя на страницу логина.
        """
        response = self.guest_client.get('/auth/password_change/')
        self.assertRedirects(
            response, '/auth/login/?next=/auth/password_change/')


class UsersViewsTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_user_pages_accessible_by_name(self):
        """Генерируемые URL приложения user доступны."""
        STATUS = HTTPStatus.OK
        url_names = [
            reverse('users:signup'), reverse('users:login'),
            reverse('users:logout'), reverse('users:password_reset')
        ]
        for url in url_names:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, STATUS)

    def test_user_pages_uses_correct_template(self):
        """При запросе к странице применяется корректный шаблон."""
        templates_urls_names = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:login'): 'users/login.html',
            reverse('users:logout'): 'users/logged_out.html',
            reverse('users:password_reset'): 'users/password_reset_form.html',
        }
        for url, template in templates_urls_names.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_users_signup_uses_correct_context(self):
        """Шаблон signup сформирован с правильным контекстом."""
        response = self.guest_client.get(reverse('users:signup'))
        form_fields = {
            'first_name': forms.fields.CharField,
            'last_name': forms.fields.CharField,
            'username': forms.fields.CharField,
            'email': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class UsersFormsTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_signup_form_creates_new_user(self):
        """При заполнении формы users:signup создается новый пользователь."""
        users_count = User.objects.count()
        form_data = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'username': 'Ivanych',
            'email': 'moon_pie_777@mail.ru',
            'password1': 'zFmvlksv@!$@#Rfs',
            'password2': 'zFmvlksv@!$@#Rfs',
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                first_name='Ivan',
                last_name='Ivanov',
                username='Ivanych',
                email='moon_pie_777@mail.ru',
            ).exists()
        )
