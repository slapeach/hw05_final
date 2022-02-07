from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .forms import PostForm, CommentForm
from .models import Post, Group, User, Follow

NUMBER_OF_POSTS = 10


def index(request):
    template_name = 'posts/index.html'
    post_list = Post.objects.all().order_by('-created')
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


def group_posts(request, slug):
    template_name = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.all().filter(group=group)
    paginator = Paginator(posts, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Записи сообщества'
    context = {
        'group': group,
        'title': title + ' ' + str(group),
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


def profile(request, username):
    template_name = 'posts/profile.html'
    user_profile = get_object_or_404(User, username=username)
    user = request.user
    if user.is_authenticated:
        follow = Follow.objects.filter(
            user=user, author=user_profile
        )
        if user_profile != user and follow.exists():
            following = True
        else:
            following = False
    else:
        following = False
    user_posts = user_profile.posts.all()
    paginator = Paginator(user_posts, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_counter = user_posts.count()
    title = f'Профайл пользователя {user_profile.get_full_name()}'
    context = {
        'title': title,
        'author': user_profile,
        'page_obj': page_obj,
        'post_counter': post_counter,
        'following': following,
    }
    return render(request, template_name, context)


def post_detail(request, post_id):
    template_name = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    post_list = Post.objects.all()
    post_counter = post_list.filter(author=post.author).count()
    title = post.text[:30]
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    context = {
        'title': title,
        'post': post,
        'post_list': post_list,
        'post_counter': post_counter,
        'form': form,
        'comments': comments,
    }
    return render(request, template_name, context)


@login_required
def post_create(request):
    template_name = 'posts/create_post.html'
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    context = {
        'title': 'Создать новую запись',
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', post.author.username)
        return render(request, template_name, context)
    return render(request, template_name, context)


@login_required
def post_edit(request, post_id):
    template_name = 'posts/create_post.html'
    post = get_object_or_404(Post, pk=post_id)
    if request.user.id != post.author.id:
        return redirect('posts:post_detail', post.pk)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.id)
    context = {
        'title': 'Редактировать запись',
        'post': post,
        'form': form,
        'is_edit': True,
    }
    return render(request, template_name, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template_name = 'posts/follow.html'
    user = request.user
    authors = Follow.objects.filter(user=user).values('author')
    posts = Post.objects.filter(author__in=authors)
    paginator = Paginator(posts, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template_name, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        user=request.user,
        author=author)
    if request.user != author and not follow.exists():
        Follow.objects.create(user=request.user, author=author)
    return redirect('posts:profile', username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(
        user=request.user,
        author=author)
    if request.user != author and follow.exists():
        Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('posts:profile', username)
