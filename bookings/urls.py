from django.urls import path

from . import views

name = 'bookings'
urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('barbers/', views.barber_list, name='barber_list'),
    path('barbers/<int:barber_id>/', views.barber_detail, name='barber_detail'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
]
