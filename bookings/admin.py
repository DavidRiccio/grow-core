from django.contrib import admin

# Register your models here.
# bookings/admin.py
from .models import Booking, TimeSlot


# Registrar Service
@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    pass


# Registrar Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass
