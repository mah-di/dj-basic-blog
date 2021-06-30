from django.contrib.auth.models import User
from django.http.response import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.views.generic.edit import DeleteView, FormMixin
from .models import Blog, Comment, BlogLike, CommentLike
from .forms import CommentForm
import uuid
import re

# Create your views here.

class Index(ListView):
    model = Blog
    template_name = 'Blog/index.html'
    context_object_name = 'blogs'

class Profile(DetailView):
    model = User
    context_object_name = 'blogger'
    template_name = 'Blog/profile.html'

    # def get_blog_list(self):
    #     user = self.get_object()
    #     blogs = Blog.objects.filter(blogger=user)
    #     return blogs

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     blogs = self.get_blog_list()
    #     context['blogs'] = blogs
    #     return context

# @login_required
# def profile_pass_chng(req, success):
#     return render(req, 'Blog/profile.html', context={'success':success})

class WriteBlog(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('blog_title', 'blog_post', 'post_image')
    template_name = 'Blog/create_blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = self.request.META.get('HTTP_REFERER')
        context['url'] = url

        return context

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.blogger = self.request.user
        title = blog.blog_title
        title = re.sub('[^0-9a-zA-Z\s]+', '', title)
        blog.slug = title.replace(' ', '-') + '-' + str(uuid.uuid4())
        blog.save()
        return redirect('blog:single_blog', slug=blog.slug)

class ViewBlog(DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'Blog/single_blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()

        return context

class UpdateBlog(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ('blog_title', 'blog_post', 'post_image',)
    context_object_name = 'form'
    template_name = 'Blog/create_blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update'] = True
        url = self.request.META.get('HTTP_REFERER')
        context['url'] = url

        return context

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.blogger.pk != self.request.user.pk:
            raise Http404
        return super(UpdateBlog, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        blog = form.save(commit=False)
        object = Blog.objects.get(pk=self.object.pk)
        if blog.blog_title != object.blog_title:
            title = blog.blog_title
            title = re.sub('[^0-9a-zA-Z\s]+', '', title)
            blog.slug = title.replace(' ', '-') + '-' + str(uuid.uuid4())
        blog.save()
        return redirect('blog:single_blog', slug=blog.slug)

class DeleteBlog(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'Blog/delete.html'
    context_object_name = 'blog'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.blogger.pk != self.request.user.pk:
            raise Http404
        return super(DeleteBlog, self).dispatch(request, *args, **kwargs)

@login_required
def commented(req, pk):
    if req.method == 'POST':
        form = CommentForm(req.POST)
        blog = Blog.objects.get(pk=pk)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.commentor = req.user
            comment.blog = blog
            comment.save()

    return redirect('blog:single_blog', slug=blog.slug)

@login_required
def like_blog(req, pk):
    if not BlogLike.objects.filter(blog=Blog.objects.get(pk=pk), liker=req.user):
        like = BlogLike()
        like.blog = Blog.objects.get(pk=pk)
        like.liker = req.user
        like.save()

    else:
        like = BlogLike.objects.get(blog=Blog.objects.get(pk=pk), liker=req.user)
    
    return redirect('blog:single_blog', slug=like.blog.slug)

@login_required
def unlike_blog(req, pk):
    blog = Blog.objects.get(pk=pk)
    liker = req.user
    like = BlogLike.objects.get(liker=liker, blog=blog)
    like.delete()

    return redirect('blog:single_blog', slug=blog.slug)

class UpdateComment(LoginRequiredMixin, UpdateView):
    model = Comment
    context_object_name = 'form'
    template_name = 'Blog/edit_comment.html'
    fields = ('comment',)

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().commentor.pk != self.request.user.pk:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('blog:single_blog', slug=self.object.blog.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        context['pk'] = pk
        url = self.request.META.get('HTTP_REFERER')
        context['url'] = url

        return context

@login_required
def delete_comment(req, pk):
    comment = Comment.objects.get(pk=pk)
    blog = comment.blog
    comment.delete()

    return redirect('blog:single_blog', slug=blog.slug)

@login_required
def like_comment(req, pk):
    if not CommentLike.objects.filter(comment=Comment.objects.get(pk=pk), liker=req.user):
        like = CommentLike()
        like.comment = Comment.objects.get(pk=pk)
        like.liker = req.user
        like.save()

    else:
        like = CommentLike.objects.get(comment=Comment.objects.get(pk=pk), liker=req.user)
    
    comm = Comment.objects.get(pk=pk)
    return redirect('blog:single_blog', slug=comm.blog.slug)

@login_required
def unlike_comment(req, pk):
    comment = Comment.objects.get(pk=pk)
    liker = req.user
    like = CommentLike.objects.get(liker=liker, comment=comment)
    like.delete()

    return redirect('blog:single_blog', slug=comment.blog.slug)