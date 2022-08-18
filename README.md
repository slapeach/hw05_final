# yatube
## **Описание проекта**
Проект «Yatube» – социальная сеть, где пользователи делятся своими историями и мыслями, общаются в комментариях и имеют возможность отслеживать публикации интересных им авторов посредством подписки.
Проект «Yatube» реализован на Django. В проекте используется пагинация постов и кэширование. Реализована регистрация с верификацией данных, а также возможность сбора пароля и его восстановления через почту.
В дальнейшем планируется реализация API для Yatube.


## **Как запустить проект**
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/slapeach/hw05_final.git
```
```
cd hw05_final
```

Cоздать виртуальное окружение:
```
python3 -m venv env
```
На Windows:
```
python -m venv venv
```
Активировать виртуальное окружение:
```
source env/bin/activate
```
На Windows:
```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
На Windows:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
На Windows:
```
python manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```
На Windows:
```
python manage.py runserver
```

[![CI](https://github.com/slapeach/hw05_final/actions/workflows/python-app.yml/badge.svg)]