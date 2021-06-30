from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'user_profile')
    profile_pic = models.ImageField(upload_to = 'profile_pics', blank = True)
    bio = models.CharField(max_length = 400, verbose_name = 'Write a short bio representing yourself..', blank=True)

    def __str__(self):
        return self.user.username