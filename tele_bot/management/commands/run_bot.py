from django.core.management.base import BaseCommand

from tele_bot.bot import setup_bot


class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        application = setup_bot()
        application.run_polling()
