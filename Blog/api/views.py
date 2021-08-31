from django import http
from django.db.models.query_utils import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from DjangoBlog.apps.custom_pagination import CustomPagination

from ..models import Blog, BlogLike, Comment
from .serializers import BlogSerializer, CommentSerializer, SingleBlogSerializer



@api_view(['GET',])
def all_blogs_api(request):
    if request.query_params.get('search'):
        search = request.query_params.get('search')
        blog_posts = Blog.objects.filter(Q(blog_title__icontains = search) | Q(blog_post__icontains = search) | Q(blogger__username__startswith = search))
    else:
        blog_posts = Blog.objects.all()

    if request.query_params.get('ordering'):
        ordering = request.query_params.get('ordering')
        blog_posts =blog_posts.order_by(ordering)

    paginate = CustomPagination()
    paginate.page_size = 3
    posts_to_show = paginate.paginate_queryset(blog_posts, request)
    serialize = BlogSerializer(posts_to_show, context={'request': request}, many=True)
    data = paginate.get_paginated_response(serialize.data if serialize.data else 'No Data')
    
    return Response(data, status=status.HTTP_200_OK)



@api_view(['POST',])
def create_blog_api(request):
    request.data['blogger'] = request.user
    serialize = BlogSerializer(data=request.data)
    
    data = {}
    if serialize.is_valid():
        serialize.save()
        data['response'] = 'success'
        data['success'] = 'Blog posted!'
        state = status.HTTP_201_CREATED
    else:
        data['response'] = 'error'
        data['error'] = serialize.errors
        state = status.HTTP_400_BAD_REQUEST
    
    return Response(data=data, status=state)



@api_view(['GET',])
def single_blog_api(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(data={'response': 'error', 'errors': "blog doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
    
    serialize = SingleBlogSerializer(blog, context={'request': request}, many=False)

    return Response(serialize.data, status=status.HTTP_200_OK)



@api_view(['PUT',])
def update_blog_api(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(data={'response': 'error', 'errors': "blog doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
    
    data = {}
    if request.user == blog.blogger:
        serialize = BlogSerializer(blog, data=request.data)

        if serialize.is_valid():
            serialize.save()
            data['response'] = 'success'
            data['success'] = 'blog update success'
            state = status.HTTP_200_OK
        else:
            data['response'] = 'error'
            data['errors'] = serialize.errors
            state = status.HTTP_400_BAD_REQUEST
    
    else:
        data['response'] = 'error'
        data['errors'] = 'unauthorized request'
        state = status.HTTP_401_UNAUTHORIZED
    
    return Response(data=data, status=state)



@api_view(['DELETE',])
def delete_blog_api(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(data={'response': 'error', 'errors': "blog doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
    
    data = {}
    if request.user == blog.blogger:
        action = blog.delete()
        if action:
            data['response'] = 'success'
            data['success'] = 'Blog deleted'
            state = status.HTTP_200_OK
        else:
            data['response'] = 'error'
            data['errors'] = 'unexpected error occured'
            state = status.HTTP_400_BAD_REQUEST
    else:
        data['response'] = 'error'
        data['errors'] = "unauthorized request"
        state = status.HTTP_401_UNAUTHORIZED

    return Response(data=data, status=state)



@api_view(['POST', 'DELETE'])
def blog_like_unlike_api(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        return Response(data={'response': 'error', 'errors': "blog doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    data = {}
    if request.method == 'POST':
        if not request.data['liked']:
            liked = BlogLike.objects.create(blog=blog, liker=user)
            if liked:
                data['response'] = 'success'
                data['success'] = 'blog liked'
                state = status.HTTP_200_OK
            else:
                data['response'] = 'error'
                data['errors'] = 'unexpected error occured'
                state = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            data['response'] = 'error'
            data['errors'] = 'blog already liked'
            state = status.HTTP_400_BAD_REQUEST

    elif request.method == 'DELETE':
        unliked = BlogLike.objects.filter(blog=blog, liker=user)
        if unliked:
            unliked.delete()
            data['response'] = 'success'
            data['success'] = 'blog unliked'
            state = status.HTTP_200_OK
        else:
            data['response'] = 'error'
            data['errors'] = 'unexpected error occured'
            state = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=state)



@api_view(['POST',])
def create_comment_api(request):
    try:
        Blog.objects.get(pk=request.data['blog'])
    except Blog.DoesNotExist:
        return Response(data={'response': 'error', 'errors': "blog doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    request.data['commentor'] = user.pk

    serialize = CommentSerializer(data=request.data)

    data = {}
    if serialize.is_valid():
        serialize.save()
        data['response'] = 'success'
        data['success'] = 'comment added'
        state = status.HTTP_201_CREATED
    else:
        data['response'] = 'error'
        data['errors'] = serialize.errors
        state = status.HTTP_400_BAD_REQUEST

    return Response(data=data, status=state)



@api_view(['PUT',])
def update_comment_api(request):
    try:
        comment = Comment.objects.get(pk=request.data['pk'])
    except Comment.DoesNotExist:
        return Response(data={'response': 'error', 'errors': "invalid request, comment object doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    data = {}

    if request.user == comment.commentor:
        serialize = CommentSerializer(instance=comment, data=request.data)
        if serialize.is_valid():
            serialize.save()
            data['response'] = 'success'
            data['success'] = 'comment updated'
            state = status.HTTP_200_OK
        else:
            data['response'] = 'error'
            data['errors'] = serialize.errors
            state = status.HTTP_400_BAD_REQUEST
    else:
        data['response'] = 'error'
        data['errors'] = "you don't have permission to perform this action"
        state = status.HTTP_401_UNAUTHORIZED

    return Response(data=data, status=state)



@api_view(['DELETE',])
def delete_comment_api(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(data={'response': 'error', 'errors': "invalid request, comment object doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    data = {}
    if request.user == comment.commentor:
        delete = comment.delete()
        if delete:
            data['response'] = 'success'
            data['success'] = 'comment deleted'
            state = status.HTTP_200_OK
        else:
            data['response'] = 'error'
            data['errors'] = 'unexpected error occured while trying to delete the comment'
            state = status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        data['response'] = 'error'
        data['errors'] = "you don't have permission to perform this action"
        state = status.HTTP_401_UNAUTHORIZED

    return Response(data=data, status=state)