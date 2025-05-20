from django.http import JsonResponse

from users.models import Profile

from .models import Booking, TimeSlot


def verify_booking(func):
    def wrapper(request, *args, **kwargs):
        try:
            booking = Booking.objects.get(id=request.booking_pk)
            request.booking = booking
        except Booking.DoesNotExist:
            return JsonResponse({'error', 'Booking not found'}, status=404)


def verify_time_slot(func):
    def wrapper(request, *args, **kwargs):
        try:
            time_slot = TimeSlot.objects.get(pk=request.json_body.get('time_slot'))
            request.time_slot = time_slot
        except TimeSlot.DoesNotExist:
            return JsonResponse({'error', 'Time Slot not found'}, status=404)


def validate_barber_and_timeslot_existence(view_func):
    def _wrapped_view(request, *args, **kwargs):
        data = request.json_body

        try:
            request.barber_profile = Profile.objects.get(pk=data['barber'])
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'Barbero no encontrado.'}, status=400)

        try:
            request.time_slot = TimeSlot.objects.get(pk=data['time_slot'])
        except TimeSlot.DoesNotExist:
            return JsonResponse({'error': 'Horario no válido.'}, status=400)

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def validate_barber_availability(view_func):
    def _wrapped_view(request, *args, **kwargs):
        date = request.json_body['date']
        barber_user = request.barber_profile.user
        time_slot = request.time_slot

        if Booking.objects.filter(barber=barber_user, date=date, time_slot=time_slot).exists():
            return JsonResponse(
                {'error': 'El barbero no está disponible en ese horario.'}, status=400
            )

        return view_func(request, *args, **kwargs)

    return _wrapped_view
