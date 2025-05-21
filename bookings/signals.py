from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Booking
from .tasks import send_booking_confirmation


@receiver(post_save, sender=Booking)
def notify_booking_creation(sender, instance, created, **kwargs):
    """
    Notifica la creación de una reserva.

    Este receptor se activa después de que se guarda una instancia de
    `Booking`. Si la reserva se ha creado y su estado es 'CONFIRMADO',
    se encola una tarea para enviar una confirmación de la reserva.

    Parameters
    ----------
    sender : type
        La clase del modelo que envía la señal (en este caso, `Booking`).
    instance : Booking
        La instancia de reserva que se ha creado o actualizado.
    created : bool
        Indica si la instancia fue creada (True) o actualizada (False).
    **kwargs : dict
        Argumentos adicionales que pueden ser pasados a la señal.
    """
    if created and instance.status == Booking.Status.CONFIRMED:
        # Encolar tarea
        send_booking_confirmation.delay(
            user_email=instance.user.email,
            service_name=instance.service.name,
            date=str(instance.date),
            time_slot=str(instance.time_slot),
        )
