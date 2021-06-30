from django.contrib import admin
from Blog.models import Blog, Comment, BlogLike, CommentLike

# Register your models here.

admin.site.register(Blog)
admin.site.register(BlogLike)
admin.site.register(Comment)
admin.site.register(CommentLike)