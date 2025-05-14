from django.urls import path

from . import views

name = 'bookings'
urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('earnings/', views.earnings_summary, name='earnings'),
]
