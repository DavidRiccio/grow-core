from .models import Booking, TimeSlot


def get_available_time_slots(barber, date, current_time=None):
    """
    Obtiene los horarios disponibles para un barbero en una fecha específica.

    :param barber: Instancia del barbero.
    :param date: Fecha para la que se buscan los horarios.
    :param current_time: Hora actual, utilizada para excluir horarios pasados (opcional).
    :return: Lista de horarios disponibles.
    """
    time_slots = TimeSlot.objects.all()
    booked_slots = Booking.objects.filter(barber=barber, date=date).values_list(
        'time_slot', flat=True
    )
    available_time_slots = time_slots.exclude(id__in=booked_slots)

    if current_time:
        available_time_slots = available_time_slots.filter(start_time__gt=current_time)

    return [
        {
            'id': slot.id,
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M'),
        }
        for slot in available_time_slots
    ]


def is_working_day(date):
    """
    Determina si una fecha es día laboral (excluye domingos).

    :param date: Fecha a evaluar.
    :return: True si es día laboral, False en caso contrario.
    """
    return date.weekday() != 6  # Excluye domingos.
