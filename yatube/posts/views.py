from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator

from .models import Group, Post

from django.contrib.auth.decorators import login_required

from .forms import PostForm

from datetime import timezone


@login_required
def index(request):
    posts = Post.objects.all()[:10]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


@login_required
def posts_group(request, slug):
    # Функция get_object_or_404 получает по заданным критериям объект
    # из базы данных или возвращает сообщение об ошибке, если объект не найден.
    # В нашем случае в переменную group будут переданы объекты модели Group,
    # поле slug у которых соответствует значению slug в запросе
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)


@login_required
def profile(request, username):
    author = get_object_or_404(User, username=username)
    paginator = Paginator(author, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


@login_required
def post_detail(request, post_id):
    group = get_object_or_404(Group, post_id=post_id)
    posts = group.posts.all()[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post:profile', pk=post.pk)
    else:
        form = PostForm()
        context = {'form': form}
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request):
    post = get_object_or_404(Post, post_id=post_id)
    if post.author != request.user:
        return redirect('post_detail', pk=post.pk)
    form = PostForm(request.Post)
    context = {
        'is_edit': True,
        'form': form,
    }
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    return render(request, 'posts/create_post.html', context)

