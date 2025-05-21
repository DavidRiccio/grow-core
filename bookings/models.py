from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now, timedelta

from services.models import Service
from users.models import Profile


class TimeSlot(models.Model):
    """
    Modelo que representa un bloque horario para una reserva.

    Attributes
    ----------
    start_time : TimeField
        Hora de inicio del bloque.
    end_time : TimeField
        Hora de fin del bloque.
    """

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        """
        Devuelve una representación legible del bloque horario.

        Returns
        -------
        str
            Cadena con el formato 'HH:MM:SS-HH:MM:SS'.
        """
        return f'{self.start_time}-{self.end_time}'


class Booking(models.Model):
    """
    Modelo que representa una reserva de servicio entre un cliente y un barbero.

    Attributes
    ----------
    user : ForeignKey
        Usuario que realiza la reserva.
    barber : ForeignKey
        Usuario con rol de barbero que atiende la reserva.
    service : ForeignKey
        Servicio seleccionado para la reserva.
    date : DateField
        Fecha de la reserva.
    time_slot : ForeignKey
        Bloque horario en el que se agenda la reserva.
    status : IntegerField
        Estado de la reserva (confirmada o cancelada).
    created_at : DateTimeField
        Fecha de creación de la reserva.

    Notes
    -----
    - La restricción `unique_together` asegura que no haya reservas duplicadas
      para el mismo barbero, fecha y horario.
    """

    class Meta:
        unique_together = ['barber', 'date', 'time_slot']

    class Status(models.IntegerChoices):
        """
        Enumeración de los posibles estados de una reserva.
        """

        CONFIRMED = 2, 'Confirmed'
        CANCELLED = -1, 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings'
    )
    barber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='barber_bookings',
        limit_choices_to={'profile__role': Profile.Role.WORKER},
        verbose_name='Barbero',
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='bookings')
    status = models.IntegerField(choices=Status.choices, default=Status.CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def earnings_summary(cls):
        """
        Calcula los ingresos totales por reservas confirmadas en distintos periodos.

        Returns
        -------
        dict
            Diccionario con las llaves `'daily'`, `'weekly'` y `'monthly'` indicando
            el total de ingresos en cada periodo.
        """
        today = now().date()
        start_week = today - timedelta(days=today.weekday())
        start_month = today.replace(day=1)

        daily = (
            cls.objects.filter(date=today, status=cls.Status.CONFIRMED).aggregate(
                total=Sum('service__price')
            )['total']
            or 0
        )

        weekly = (
            cls.objects.filter(
                date__gte=start_week, date__lte=today, status=cls.Status.CONFIRMED
            ).aggregate(total=Sum('service__price'))['total']
            or 0
        )

        monthly = (
            cls.objects.filter(
                date__gte=start_month, date__lte=today, status=cls.Status.CONFIRMED
            ).aggregate(total=Sum('service__price'))['total']
            or 0
        )

        return {'daily': daily, 'weekly': weekly, 'monthly': monthly}

    def __str__(self):
        """
        Devuelve una representación legible de la reserva.

        Returns
        -------
        str
            Cadena con el formato 'usuario servicio fecha horario'.
        """
        return f'{self.user} {self.service} {self.date} {self.time_slot}'
