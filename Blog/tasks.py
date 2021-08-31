from celery import shared_task
from .forms import CommentForm
from .models import Blog
from django.contrib.auth.models import User


@shared_task
def comment(data, user_pk, blog_pk):
    form = CommentForm(data=data)
    blog = Blog.objects.get(pk=blog_pk)

    if form.is_valid():
        comment = form.save(commit=False)
        user = User.objects.get(pk=user_pk)
        comment.commentor = user
        comment.blog = blog
        comment.save()

    return None