import os

import django

# Configuración de Django
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'main.settings'
)  # Cambia 'main.settings' si es necesario
django.setup()

from bookings.models import Booking
from tele_bot.utils import get_updates, send_message


def handle_reservas(chat_id):
    """Obtiene todas las reservas y las envía al administrador."""
    bookings = Booking.objects.all()
    if not bookings.exists():
        send_message(chat_id, 'No hay reservas disponibles.')
        return

    response = 'Reservas actuales:\n'
    for booking in bookings:
        response += (
            f'Cliente: {booking.user.first_name} {booking.user.last_name}\n'
            f'Servicio: {booking.service.name}\n'
            f'Barbero: {booking.barber.first_name} {booking.barber.last_name}\n'
            f'Fecha: {booking.date}\n\n'
        )
    send_message(chat_id, response)


def main():
    """Procesa los comandos del bot."""
    updates = get_updates()
    for update in updates.get('result', []):
        message = update.get('message', {})
        chat_id = message.get('chat', {}).get('id')
        text = message.get('text', '')

        if text == '/r':
            handle_reservas(chat_id)


if __name__ == '__main__':
    main()
