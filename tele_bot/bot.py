from django.conf import settings
from telegram.ext import Application

from .handlers.query_handler import (
    hoy_handler,
    semana_handler,
    servicios_handler,
    start_handler,
)


def setup_bot():
    """
    Configura y devuelve la instancia de la aplicación del bot de Telegram.

    Este método crea una instancia de la aplicación del bot usando el token
    configurado en los ajustes, y añade los handlers para los comandos
    disponibles.

    Returns
    -------
    Application
        Instancia configurada de la aplicación del bot de Telegram.
    """
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(start_handler)
    application.add_handler(hoy_handler)
    application.add_handler(semana_handler)
    application.add_handler(servicios_handler)

    return application
