import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from users.models import User

from .models import Booking, Service
from .serializers import BookingEarningsSerializer, BookingSerializer


def booking_list(request):
    if request.method == 'GET':
        bookings = Booking.objects.all()
        bookings_serializer = [BookingSerializer(booking).serialize() for booking in bookings]
        return JsonResponse(bookings_serializer, safe=False, status=200)


@csrf_exempt
def create_booking(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        user = get_object_or_404(User, pk=data['user'])
        service = get_object_or_404(Service, pk=data['service'])
        booking_time = datetime.fromisoformat(data['booking_time'])
        status = data.get('status', 'pending')

        booking = Booking.objects.create(
            user=user,
            service=service,
            barber=None,
            booking_time=booking_time,
            status=status,
        )

        booking_serializer = BookingSerializer(booking)
        return JsonResponse(booking_serializer.serialize(), status=201)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    serializer = BookingSerializer(booking, request=request)
    return serializer.json_response()


def earnings_summary(request):
    serializer = BookingEarningsSerializer(None, request=request)
    return serializer.json_response()
