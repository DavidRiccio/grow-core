from django.http import JsonResponse

from users.models import Profile

from .models import Booking, TimeSlot


def verify_booking(func):
    def wrapper(request, *args, **kwargs):
        try:
            booking = Booking.objects.get(id=booking.pk)
            request.booking = booking
        except Booking.DoesNotExists:
            return JsonResponse({'error', 'Booking not found'}, status=404)


def verify_time_slot(func):
    def wrapper(request, *args, **kwargs):
        try:
            time_slot = TimeSlot.objects.get(id=request.json_body['time_slot'])
            request.time_slot = time_slot
        except TimeSlot.DoesNotExists:
            return JsonResponse({'error', 'Time Slot not found'}, status=404)


def verify_barber(func):
    def wrapper(request, *args, **kwargs):
        try:
            profile = Profile.objects.get(id=request.json_body[barber])
            if profile.role != 'W':
                return JsonResponse({'error': 'The user is not a Barber'}, status=404)
            request.barber = profile
        except Profile.DoesNotExist:
            return JsonResponse({'error': 'The barber does not exists'})
