from django.shortcuts import redirect


def index(req):
    return redirect('blog:home')