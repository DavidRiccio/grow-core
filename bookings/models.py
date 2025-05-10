from django.db import models

from services.models import Service
from users.models import User


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.start_time}-{self.end_time}'


class Booking(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1, 'Initiated'
        CONFIRMED = 2, 'Confirmed'
        CANCELLED = -1, 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='bookings')
    status = models.IntegerField(choices=Status.choices, default=Status.INITIATED)
    created_at = models.DateTimeField(auto_now_add=True)
