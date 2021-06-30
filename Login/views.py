from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .forms import SignUpForm, InfoUpdateForm, PfpUpdateForm, BioUpdateForm
from .models import UserProfile


# Create your views here.

def UserProfile_init(form):
    username = form.cleaned_data.get('username')
    user = User.objects.get(username=username)
    profile_form = UserProfile()
    profile_form.user = user
    profile_form.save()

# =================================================================================

def signup(req):
    form = SignUpForm()
    registered = False

    if req.user.is_authenticated:
        return redirect('blog:home')

    if req.method == 'POST':
        form = SignUpForm(data=req.POST)
        if form.is_valid():
            form.save()
            UserProfile_init(form)
            registered = True

    dict = {'form':form, 'registered':registered}
    return render(req, 'Login/signup.html', context=dict)

def user_login(req):
    form = AuthenticationForm()

    if req.user.is_authenticated:
        return redirect('blog:home')

    if req.method == 'POST':
        form = AuthenticationForm(data=req.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('blog:profile', pk=req.user.pk)

    return render(req, 'Login/login.html', context={'form':form})

@login_required
def user_logout(req):
    logout(req)
    return redirect('home')

@login_required
def update(req):
    user = req.user
    form = InfoUpdateForm(instance=user)
    bio_form = BioUpdateForm(instance=user.user_profile)
    if req.method == 'POST':
        form = InfoUpdateForm(instance=user, data=req.POST)
        bio_form = BioUpdateForm(instance=user.user_profile, data=req.POST)
        if form.is_valid() and bio_form.is_valid():
            form.save()
            bio_form.save()
            return redirect('blog:profile', pk=req.user.pk)

    return render(req, 'Login/update.html', context={'form':form, 'bio_form':bio_form})

@login_required
def change_pass(req):
    success = False
    user = req.user
    form = PasswordChangeForm(user)
    if req.method == 'POST':
        form = PasswordChangeForm(user, data=req.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(req, user)
            success = True

    return render(req, 'Login/change_pass.html', context={'form':form, 'success':success})

@login_required
def change_pfp(req):
    form = PfpUpdateForm(instance=req.user.user_profile)
    if req.method == 'POST':
        form = PfpUpdateForm(req.POST, req.FILES, instance=req.user.user_profile)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', pk=req.user.pk)
    return render(req, 'Login/change_pfp.html', context={'form':form})