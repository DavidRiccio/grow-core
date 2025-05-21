from django.http import JsonResponse

from users.models import Profile

from .models import Booking, TimeSlot


def verify_booking(func):
    """
    Decorador que intenta recuperar una reserva (booking) a partir de 'booking_pk' en los parámetros de la URL.

    Si la reserva existe, se adjunta al objeto request como 'request.booking'.
    Si no existe, devuelve una respuesta JSON con error 404 (Not Found).

    Args:
        func (callable): Vista a decorar.

    Returns:
        callable: Vista decorada con la verificación de existencia de la reserva.
    """

    def wrapper(request, *args, **kwargs):
        try:
            booking = Booking.objects.get(id=kwargs['booking_pk'])
            request.booking = booking
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)

        return func(request, *args, **kwargs)

    return wrapper


def validate_barber_and_timeslot_existence(view_func):
    def wrapper(request, *args, **kwargs):
        data = request.json_body

        try:
            request.barber_profile = Profile.objects.get(user_id=data['barber'])
            if request.barber_profile.role != Profile.Role.WORKER:
                return JsonResponse({'error': 'The user is not a Barber'}, status=400)
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'Barber not found'}, status=404)

        try:
            request.time_slot = TimeSlot.objects.get(pk=data['time_slot'])
        except TimeSlot.DoesNotExist:
            return JsonResponse({'error': 'Invalid time slot'}, status=404)

        return view_func(request, *args, **kwargs)

    return wrapper


def validate_barber_availability(view_func):
    """
    Decorador que valida si el barbero está disponible en la fecha y hora solicitadas.

    Utiliza los datos 'date', 'barber_profile' y 'time_slot' previamente cargados en el request.
    Si ya existe una reserva para ese barbero en la fecha y horario indicados,
    devuelve una respuesta JSON con error 400 (Bad Request).

    Args:
        view_func (callable): Vista a decorar.

    Returns:
        callable: Vista decorada que valida la disponibilidad del barbero.
    """

    def wrapper(request, *args, **kwargs):
        date = request.json_body['date']
        barber_user = request.barber_profile.user
        time_slot = request.time_slot

        if Booking.objects.filter(barber=barber_user, date=date, time_slot=time_slot).exists():
            return JsonResponse(
                {'error': 'El barbero no está disponible en ese horario.'}, status=400
            )

        return view_func(request, *args, **kwargs)

    return wrapper
