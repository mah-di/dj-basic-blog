from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('update-profile/', views.update, name='update'),
    path('password/', views.change_pass, name='change_pass'),
    path('change-profile-image/', views.change_pfp, name='change_pfp')
]