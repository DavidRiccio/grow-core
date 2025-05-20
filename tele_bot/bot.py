from django.conf import settings
from telegram.ext import Application

from .handlers.query_handler import (
    hoy_handler,
    semana_handler,
    servicios_handler,
    start_handler,
)


def setup_bot():
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(start_handler)
    application.add_handler(hoy_handler)
    application.add_handler(semana_handler)
    application.add_handler(servicios_handler)

    return application
