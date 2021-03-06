from django.urls import path
from . import views

app_name = 'blog_api'

urlpatterns = [
    path('', views.all_blogs_api, name='all_blogs'),
    path('create', views.create_blog_api, name='create_blog'),
    path('comment', views.create_comment_api, name='create_comment'),
    path('comment/<pk>/like-unlike', views.comment_like_unlike_api, name='comment_like_unlike'),
    path('comment/update', views.update_comment_api, name='update_comment'),
    path('comment/<pk>/delete', views.delete_comment_api, name='delete_comment'),
    path('<slug>/', views.single_blog_api, name='single_blog'),
    path('<slug>/like-unlike', views.blog_like_unlike_api, name='like_unlike'),
    path('<slug>/update', views.update_blog_api, name='update_blog'),
    path('<slug>/delete', views.delete_blog_api, name='delete_blog'),
]