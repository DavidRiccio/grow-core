from django.urls import path

from . import views

name = 'events'
urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_pk>/', views.event_detail, name='event-detail'),
    path('add/', views.add_event, name='add-event'),
    path('<int:event_pk>/edit/', views.edit_event, name='edit-event'),
    path('<int:event_pk>/delete/', views.delete_event, name='delete-event'),
]
