from django.db import models


class Event(models.Model):
    """
    Modelo que representa un evento programado.

    Atributos
    ----------
    name : CharField
        Nombre del evento.
    description : TextField
        Descripción opcional del evento.
    date : DateField
        Fecha en la que se llevará a cabo el evento.
    time : TimeField
        Hora en la que comenzará el evento.
    image : ImageField
        Imagen representativa del evento. Puede estar vacía o usar una imagen por defecto.
    location : CharField
        Dirección o lugar donde se realiza el evento.
    created_at : DateTimeField
        Fecha y hora en la que se creó el evento (automáticamente asignada).

    Métodos
    -------
    __str__ : str
        Devuelve una representación legible del evento.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(
        upload_to='media/events_images/',
        default='events_images/no_event.png',
        blank=True,
        null=True,
    )
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Retorna una representación legible del evento.

        Returns
        -------
        str
            Cadena con el formato 'Nombre en Fecha en Ubicación'.
        """
        return f'{self.name} on {self.date} at {self.location}'
