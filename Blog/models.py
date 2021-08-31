from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import pre_save
from django.dispatch import receiver

import re
import uuid

# Create your models here.

class Blog(models.Model):
    blogger = models.ForeignKey(User, null=True, on_delete = models.CASCADE, related_name = 'blogs')
    blog_title = models.CharField(max_length=264, verbose_name='Blog Title')
    slug = models.SlugField(unique=True, null=True)
    blog_post = models.TextField(max_length=10000, verbose_name="Blog Content")
    post_image = models.ImageField(upload_to='blog_images', blank=True, verbose_name='Image')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    _og_title = None

    def __str__(self):
        return self.blog_title

    def get_likers(self):
        likes = self.blog_like.all()
        return [like.liker for like in likes]

    def get_likes(self):
        return self.blog_like.count()

    def get_total_comments(self):
        return self.blog_comment.count()

    class Meta:
        ordering = ('-publish_date',)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    commentor = models.ForeignKey(User, on_delete=CASCADE, related_name='comments')
    comment = models.TextField(max_length=1000, verbose_name='Write a comment..')
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def get_likes(self):
        return self.comment_like.count()

    def get_likers(self):
        return [like.liker for like in self.comment_like.all()]

    class Meta:
        ordering = ('-comment_date',)

class BlogLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_like')
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_liker')

    def __str__(self):
        return self.blog.blog_title

    def likers(self):
        liker_list = self.objects.values_list('liker', flat=True)
        return liker_list

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_like')
    liker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_liker')

    def __str__(self):
        return self.liker.username


@receiver(pre_save, sender=Blog)
def slugit(sender, instance, **kwargs):
    if instance.blog_title != instance._og_title:
        title = instance.blog_title
        title = re.sub('[^0-9a-zA-Z\s]+', '', title)
        instance.slug = title.replace(' ', '-') + '-' + str(uuid.uuid4())
        instance._og_title = instance.blog_title
