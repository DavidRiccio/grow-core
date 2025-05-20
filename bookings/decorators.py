from django.http import JsonResponse

from users.models import Profile

from .models import Booking, TimeSlot


def verify_booking(func):
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
            request.barber_profile = Profile.objects.get(pk=data['barber'])
            if request.barber_profile.role != 'W':
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
