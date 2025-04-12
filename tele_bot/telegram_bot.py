# tele_bot/telegram_bot.py
import time

import requests
from django.conf import settings
from django.db import models
from django.utils import timezone

from bookings.models import Barber, Booking


class AdminTelegramBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.admin_chat_id = settings.ADMIN_CHAT_ID
        self.base_url = f'https://api.telegram.org/bot{self.token}'

    def send_message(self, text):
        """Envía mensajes solo al admin"""
        requests.post(
            f'{self.base_url}/sendMessage',
            json={'chat_id': self.admin_chat_id, 'text': text, 'parse_mode': 'HTML'},
        )

    def get_future_bookings(self):
        """Obtiene reservas futuras (hoy y posteriores) excluyendo pasadas"""
        now = timezone.now()
        current_date = now.date()
        current_time = now.time()

        bookings = Booking.objects.filter(
            models.Q(date__gt=current_date) | models.Q(date=current_date, time__gte=current_time)
        ).order_by('date', 'time')

        if not bookings.exists():
            return '📭 No hay reservas futuras'

        response = ['<b>🗓 Reservas Futuras:</b>\n']
        for booking in bookings:
            is_today = booking.date == current_date
            date_display = 'Hoy' if is_today else booking.date.strftime('%d/%m/%Y')

            status_icon = (
                '🟢'
                if booking.status == 'confirmed'
                else '🟡'
                if booking.status == 'pending'
                else '🔴'
            )

            response.append(
                f'{status_icon} <b>ID {booking.id}</b>\n'
                f'📅 {date_display} ⏰ {booking.time.strftime("%H:%M")}\n'
                f'👤 {booking.user.first_name}\n'
                f'💈 {booking.barber.first_name}\n'
                f'📌 {booking.service.name}\n'
                '――――――――――――――――――――'
            )
        return '\n'.join(response)

    def get_today_bookings(self):
        """Obtiene reservas de hoy formateadas (solo horas futuras)"""
        today = timezone.now().date()
        current_time = timezone.now().time()

        bookings = Booking.objects.filter(date=today, time__gte=current_time).order_by('time')

        if not bookings.exists():
            return '📭 No hay reservas para hoy'

        response = ['<b>🗓 Reservas de hoy:</b>\n']
        for booking in bookings:
            status_icon = (
                '🟢'
                if booking.status == 'confirmed'
                else '🟡'
                if booking.status == 'pending'
                else '🔴'
            )
            response.append(
                f'{status_icon} <b>ID {booking.id}</b>\n'
                f'⏰ {booking.time.strftime("%H:%M")}\n'
                f'👤 {booking.user.first_name}\n'
                f'💈 {booking.barber.first_name}\n'
                f'📌 {booking.service.name}\n'
                '――――――――――――――――――――'
            )
        return '\n'.join(response)

    def get_bookings_by_barber(self, barber_name):
        """Filtra reservas futuras por barbero"""
        now = timezone.now()
        current_date = now.date()
        current_time = now.time()

        try:
            barber = Barber.objects.get(
                models.Q(first_name__icontains=barber_name)
                | models.Q(last_name__icontains=barber_name)
            )
        except Barber.DoesNotExist:
            return '⚠️ Barbero no encontrado'
        except Barber.MultipleObjectsReturned:
            return '⚠️ Varios barberos coinciden. Usa el nombre completo'

        bookings = Booking.objects.filter(
            (models.Q(date__gt=current_date) | models.Q(date=current_date, time__gte=current_time)),
            barber=barber,
            status='confirmed',  # Otro keyword argument
        ).order_by('date', 'time')

        if not bookings.exists():
            return f'📭 No hay reservas futuras para {barber.first_name}'

        response = [f'<b>💈 Citas de {barber.first_name}:</b>\n']
        for booking in bookings:
            status_icon = '🟢' if booking.status == 'confirmed' else '🟡'
            date_display = (
                'Hoy' if booking.date == current_date else booking.date.strftime('%d/%m/%Y')
            )

            response.append(
                f'{status_icon} <b>ID {booking.id}</b>\n'
                f'📅 {date_display} ⏰ {booking.time.strftime("%H:%M")}\n'
                f'👤 {booking.user.first_name}\n'
                f'📌 {booking.service.name}\n'
                '――――――――――――――――――――'
            )
        return '\n'.join(response)

    def process_command(self, command):
        """Ejecuta los comandos del admin"""
        cmd_parts = command.split()

        if command == '/reservas':
            return self.get_future_bookings()

        elif command == '/reservas-hoy':
            return self.get_today_bookings()

        elif cmd_parts[0] == '/barbero' and len(cmd_parts) >= 2:
            barber_name = ' '.join(cmd_parts[1:])
            return self.get_bookings_by_barber(barber_name)

        elif cmd_parts[0] == '/reserva' and len(cmd_parts) == 2:
            try:
                booking = Booking.objects.get(id=int(cmd_parts[1]))
                return (
                    f'<b>📋 Reserva #{booking.id}</b>\n'
                    f'📅 Fecha: {booking.date.strftime("%d/%m/%Y")}\n'
                    f'⏰ Hora: {booking.time.strftime("%H:%M")}\n'
                    f'👤 Cliente: {booking.user.first_name} {booking.user.last_name}\n'
                    f'✂️ Servicio: {booking.service.name}\n'
                    f'💈 Barbero: {booking.barber.first_name}\n'
                    f'🔄 Estado: {booking.get_status_display()}'
                )
            except (Booking.DoesNotExist, ValueError):
                return '⚠️ <b>Error:</b> Reserva no encontrada'

        elif cmd_parts[0] == '/cancelar' and len(cmd_parts) == 2:
            try:
                booking = Booking.objects.get(id=int(cmd_parts[1]))
                booking.status = 'cancelled'
                booking.save()
                return f'✅ <b>Reserva #{cmd_parts[1]} cancelada</b>'
            except Exception as e:
                return f'❌ <b>Error:</b> {str(e)}'

        else:
            return (
                'No he entendido ese comando\n'
                '<b>💡 Aquí tienes los comandos disponibles:</b>\n'
                '/reservas - Todas las reservas futuras\n'
                '/reservas-hoy - Reservas restantes de hoy\n'
                '/barbero [nombre] - Citas de un barbero\n'
                '/reserva [id] - Detalle de reserva\n'
                '/cancelar [id] - Cancelar reserva'
            )

    def start_polling(self):
        """Inicia el servicio de escucha"""
        last_update_id = 0
        print('🤖 Bot de administrador iniciado...')

        while True:
            try:
                updates = (
                    requests.get(
                        f'{self.base_url}/getUpdates',
                        params={'offset': last_update_id + 1, 'timeout': 20},
                    )
                    .json()
                    .get('result', [])
                )

                for update in updates:
                    message = update.get('message', {})
                    if str(message.get('chat', {}).get('id')) == self.admin_chat_id:
                        response = self.process_command(message.get('text', '').strip())
                        self.send_message(response)

                    last_update_id = update['update_id']

            except Exception as e:
                print(f'🔴 Error: {str(e)}')
                time.sleep(5)
