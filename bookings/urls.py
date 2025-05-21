from django.urls import path

from . import views

name = 'bookings'
urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('get-earnings/', views.get_earnings, name='get-earnings'),
    path('<int:booking_pk>/', views.booking_detail, name='booking_detail'),
    path('earnings/', views.earnings_summary, name='earnings'),
    path('add/', views.create_booking, name='add-booking'),
    path('dates/', views.get_available_dates, name='add-available-dates'),
    path('<int:booking_pk>/edit/', views.edit_booking, name='edit-booking'),
    path('<int:booking_pk>/delete/', views.delete_booking, name='delete-booking'),
]
