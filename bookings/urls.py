from django.urls import path

from . import views

name = 'bookings'
urlpatterns = [
    path('', views.user_booking_list, name='user_booking_list'),
    path('get-earnings/', views.get_earnings, name='get-earnings'),
    path('<int:booking_pk>/', views.booking_detail, name='booking_detail'),
    path('add/', views.create_booking, name='add-booking'),
    path('dates/', views.get_available_dates, name='add-available-dates'),
    path('<int:booking_pk>/edit/', views.edit_booking, name='edit-booking'),
    path('<int:booking_pk>/cancel/', views.cancel_booking, name='cancel-booking'),
]
