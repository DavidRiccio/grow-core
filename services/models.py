import re
from datetime import timedelta

from django.db import models


class Service(models.Model):
    """
    Modelo que representa un servicio que puede ser ofrecido por un profesional (por ejemplo, un barbero).

    Atributos
    ----------
    name : CharField
        Nombre del servicio.
    description : TextField
        Descripción opcional del servicio.
    price : DecimalField
        Precio del servicio, con hasta 8 dígitos y 2 decimales.
    image : ImageField
        Imagen representativa del servicio. Puede estar vacía o usar una por defecto.
    duration : DurationField
        Duración del servicio como objeto timedelta.
    created_at : DateTimeField
        Fecha y hora en que el servicio fue creado.

    Métodos
    -------
    __str__ : str
        Devuelve el nombre del servicio como representación legible.
    convert_duration_string : timedelta
        Método utilitario para convertir una cadena de duración en formato ISO 8601
        (como 'PT1H30M') a un objeto timedelta.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(
        upload_to='media/services_images/',
        default='services_images/no_service.png',
        blank=True,
        null=True,
    )
    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Retorna una representación legible del servicio.

        Returns
        -------
        str
            Nombre del servicio.
        """
        return self.name

    @staticmethod
    def convert_duration_string(duration_str):
        """
        Convierte una cadena en formato ISO 8601 (por ejemplo, 'PT1H30M') a un objeto timedelta.

        Parameters
        ----------
        duration_str : str
            Cadena de duración en formato ISO 8601.

        Returns
        -------
        timedelta
            Objeto que representa la duración.

        Raises
        ------
        ValueError
            Si el formato de la cadena no es válido.
        """
        pattern = re.compile(r'P(?:\d+D)?T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?')
        match = pattern.match(duration_str)
        if not match:
            raise ValueError('Formato de duración no válido')
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(2)) if match.group(2) else 0
        seconds = int(match.group(3)) if match.group(3) else 0
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
