# users/urls.py
from django.urls import path

from . import views

name = 'users'
urlpatterns = [
    path('', views.list_users, name='list_users'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
]
