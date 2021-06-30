from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_init

# Create your models here.

class Blog(models.Model):
    blogger = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blogs')
    blog_title = models.CharField(max_length=264, verbose_name='Blog Title')
    slug = models.SlugField(unique=True)
    blog_post = models.TextField(max_length=10000, verbose_name="Blog Content")
    post_image = models.ImageField(upload_to='blog_images', blank=True, verbose_name='Image')
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.blog_title

    class Meta:
        ordering = ('-publish_date',)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    commentor = models.ForeignKey(User, on_delete=CASCADE, related_name='commentor')
    comment = models.TextField(max_length=1000, verbose_name='Write a comment..')
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

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