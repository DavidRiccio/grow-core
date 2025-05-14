from django.db import models
from django.db.models import Sum
from django.utils.timezone import now, timedelta

from services.models import Service
from users.models import User


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.start_time}-{self.end_time}'


class Booking(models.Model):
    class Status(models.IntegerChoices):
        CONFIRMED = 2, 'Confirmed'
        CANCELLED = -1, 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='bookings')
    status = models.IntegerField(choices=Status.choices, default=Status.CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def earnings_summary(cls):
        today = now().date()
        start_week = today - timedelta(days=today.weekday())  # lunes
        start_month = today.replace(day=1)

        daily = (
            cls.objects.filter(date=today, status=cls.Status.CONFIRMED).aggregate(
                total=Sum('service__price')
            )['total']
            or 0
        )

        weekly = (
            cls.objects.filter(
                date__gte=start_week, date__lte=today, status=cls.Status.CONFIRMED
            ).aggregate(total=Sum('service__price'))['total']
            or 0
        )

        monthly = (
            cls.objects.filter(
                date__gte=start_month, date__lte=today, status=cls.Status.CONFIRMED
            ).aggregate(total=Sum('service__price'))['total']
            or 0
        )

        return {'daily': daily, 'weekly': weekly, 'monthly': monthly}

    def __str__(self):
        return f'{self.user} {self.service} {self.date} {self.time_slot}'
