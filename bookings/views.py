import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from users.models import User

from .models import Barber, Booking, Service
from .serializers import BarberSerializer, BookingSerializer, ServiceSerializer


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


def service_list(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, request=request)
    return serializer.json_response()


def service_detail(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        serializer = ServiceSerializer(service, request=request)
        return serializer.json_response()
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)


def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    serializer = BookingSerializer(booking, request=request)
    return serializer.json_response()


def barber_list(request):
    barbers = Barber.objects.all()
    serializer = BarberSerializer(barbers, request=request)
    return serializer.json_response()


# Vista para obtener los detalles de un barbero específico
def barber_detail(request, barber_id):
    try:
        barber = Barber.objects.get(id=barber_id)
        serializer = BarberSerializer(barber, request=request)
        return serializer.json_response()
    except Barber.DoesNotExist:
        return JsonResponse({'error': 'Barber not found'}, status=404)
