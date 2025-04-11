# tele_bot/management/commands/run_bot.py
from django.core.management.base import BaseCommand

from tele_bot.telegram_bot import AdminTelegramBot


class Command(BaseCommand):
    help = 'Inicia el bot de administrador de Telegram'

    def handle(self, *args, **options):
        bot = AdminTelegramBot()
        bot.start_polling()
