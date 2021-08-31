from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token


app_name = 'accounts'

urlpatterns = [
    path('registration', views.registration_api, name='registration'),
    path('login', obtain_auth_token, name='login'),
    path('update', views.profile_update_api_view, name='update'),
    path('<username>/', views.profile_api_view, name='profile'),
]