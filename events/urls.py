from django.urls import path

from . import views

name = 'events'
urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_pk>/', views.event_detail, name='event-detail'),
]
