from django.urls import path

from . import views

name = 'services'
urlpatterns = [
    path('', views.service_list, name='service-list'),
    path('add/', views.add_service, name='add-service'),
    path('<int:service_pk>/', views.service_detail, name='service-detail'),
    path('<int:service_pk>/edit/', views.edit_service, name='edit-service'),
    path('<int:service_pk>/delete/', views.delete_service, name='delete-service'),
]
