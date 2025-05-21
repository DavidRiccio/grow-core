from .models import Booking, TimeSlot


def get_available_time_slots(barber, date, current_time=None):
    """
    Obtiene los horarios disponibles para un barbero en una fecha específica.

    Parameters
    ----------
    barber : Barber
        Instancia del barbero.
    date : datetime.date
        Fecha para la que se buscan los horarios.
    current_time : datetime.time, opcional
        Hora actual, utilizada para excluir horarios pasados.

    Returns
    -------
    list of dict
        Lista de horarios disponibles, donde cada horario es un diccionario
        que contiene las siguientes claves:
            - id : int
            - start_time : str
            - end_time : str
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

    Parameters
    ----------
    date : datetime.date
        Fecha a evaluar.

    Returns
    -------
    bool
        True si es día laboral, False en caso contrario.
    """
    return date.weekday() != 6  # Excluye domingos.
