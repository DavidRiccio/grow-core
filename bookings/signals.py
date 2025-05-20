from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Booking
from .tasks import send_booking_confirmation


@receiver(post_save, sender=Booking)
def notify_booking_creation(sender, instance, created, **kwargs):
    if created and instance.status == Booking.Status.CONFIRMED:
        # Encolar tarea
        send_booking_confirmation.delay(
            user_email=instance.user.email,
            service_name=instance.service.name,
            date=str(instance.date),
            time_slot=str(instance.time_slot),
        )
