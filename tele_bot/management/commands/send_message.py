from django.core.management.base import BaseCommand

from tele_bot.utils import send_message


class Command(BaseCommand):
    help = 'Envía un mensaje a tu chat de Telegram'

    def add_arguments(self, parser):
        parser.add_argument('chat_id', type=str, help='El chat ID del destinatario')
        parser.add_argument('message', type=str, help='El mensaje que deseas enviar')

    def handle(self, *args, **options):
        chat_id = options['chat_id']
        message = options['message']

        # Enviar el mensaje usando la función de send_message
        response = send_message(chat_id, message)

        # Mostrar la respuesta de la API
        self.stdout.write(self.style.SUCCESS(f'Mensaje enviado: {response}'))
