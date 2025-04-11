from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'

    def ready(self):
        pass  # Asegúrate de que las señales se registren cuando se inicie la aplicación
