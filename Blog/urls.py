from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Index.as_view(), name='home'),
    path('profile/<pk>', views.Profile.as_view(), name='profile'),
    # path('profile/<str:success>', views.profile_pass_chng, name='pass_chng'),
    path('write-blog/', views.WriteBlog.as_view(), name='write_blog'),
    path('post/<slug>', views.ViewBlog.as_view(), name='single_blog'),
    path('update-blog/<slug>', views.UpdateBlog.as_view(), name='update'),
    path('delete-blog/<slug>', views.DeleteBlog.as_view(), name='delete'),
    path('commented/<pk>/', views.commented, name='comment'),
    path('like/<pk>', views.like_blog, name='like'),
    path('unlike/<pk>', views.unlike_blog, name='unlike'),
    path('update-comment/<pk>', views.UpdateComment.as_view(), name='edit_comment'),
    path('delete-comment/<pk>', views.delete_comment, name='delete_comment'),
    path('comment-liked/<pk>', views.like_comment, name='comment_like'),
    path('comment-unliked/<pk>', views.unlike_comment, name='comment_unlike'),
]