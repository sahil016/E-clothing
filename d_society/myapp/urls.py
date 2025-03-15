from django.urls import path
from . import views  # Import views from the current app
from .views import *

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.User_login, name='login'), 
    path('index/', views.index, name='index'), 
    path('logout/', views.custom_logout, name='logout'), 
    path('member/', views.member, name='member')
    
]