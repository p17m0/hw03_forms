from . import views

from django.urls import path

app_name = 'posts'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    path('group/<slug:slug>/', views.posts_group, name='posts_group'),
    # Профайл пользователя
    path('profile/<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # Создание поста
    path('posts/post_new', views.post_create, name='post_create'),
]
