from django import template
from Blog.models import Blog, BlogLike, Comment, CommentLike


register = template.Library()

@register.filter
def blog_likers(blg):
    pk = blg.pk
    blog = Blog.objects.get(pk=pk)
    likers = list(BlogLike.objects.filter(blog=blog).values_list('liker', flat=True))

    return likers

@register.filter
def comment_likers(cmt):
    pk = cmt.pk
    comment = Comment.objects.get(pk=pk)
    likers = list(CommentLike.objects.filter(comment=comment).values_list('liker', flat=True))

    return likers

@register.filter
def test(str):
    return f'it works {str}'