from django.contrib import admin

# Register your models here.
# bookings/admin.py
from .models import Barber, Booking, Service


# Registrar Barber
@admin.register(Barber)
class BarberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('first_name', 'last_name')


# Registrar Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name',)
    list_filter = ('price',)


# Registrar Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'barber', 'date', 'time', 'status', 'created_at')
    search_fields = (
        'user__first_name',
        'user__last_name',
        'service__name',
        'barber__first_name',
        'barber__last_name',
    )
    list_filter = ('status', 'date', 'service', 'barber')
