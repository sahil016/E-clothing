from django.urls import path
from . import views  # Import views from the current app
from .views import *

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.User_login, name='login'), 
    path('index/', views.index, name='index'), 
    path('logout/', views.custom_logout, name='logout'), 
    path('member/', views.member, name='member'),
    path('add_watchman/', add_watchman, name='add_watchman'),
    path('delete_watchman/<int:watchman_id>/', delete_watchman, name='delete_watchman'),
    
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/add/', views.add_notice, name='add_notice'),
    path('notices/delete/<int:notice_id>/', views.delete_notice, name='delete_notice'),
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.add_event, name='add_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
]   