from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import fields, HiddenInput
from .models import UserProfile



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class InfoUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(InfoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = HiddenInput()
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        
class PfpUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic',)
        
class BioUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio',)