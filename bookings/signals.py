import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from tele_bot.utils import (
    send_message,  # Asegúrate de que esta función esté correctamente importada
)

from .models import Booking

# Configuración del logger para errores
logger = logging.getLogger(__name__)


@receiver(post_save, sender=Booking)
def enviar_reserva_telegram(sender, instance, created, **kwargs):
    """
    Señal que se ejecuta después de que se guarda una nueva reserva.
    Envia un mensaje con los detalles de la reserva a Telegram.
    """
    if created:  # Verifica si la reserva se acaba de crear
        try:
            # Formatear el mensaje con los detalles de la reserva
            mensaje = 'Se ha realizado una nueva reserva:\n\n'
            mensaje += f'Usuario: {instance.user.first_name} {instance.user.last_name} ({instance.user.email})\n'
            mensaje += f'Servicio: {instance.service.name} - {instance.service.price} EUR\n'
            mensaje += f'Barbero: {instance.barber.first_name} {instance.barber.last_name}\n'
            mensaje += f'Fecha: {instance.date} | Hora: {instance.time}\n'
            mensaje += f'Estado: {instance.status}\n'

            # Enviar el mensaje al chat de Telegram
            chat_id = 1920633138  # Reemplaza con tu propio chat_id de Telegram
            send_message(chat_id, mensaje)
            logger.info('Mensaje enviado a Telegram con éxito.')
        except Exception as e:
            logger.error(f'Error al enviar el mensaje de Telegram: {e}')
