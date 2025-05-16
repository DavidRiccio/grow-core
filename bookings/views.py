from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from services.models import Service
from shared.decorators import (
    load_json_body,
    required_fields,
    required_method,
    verify_token,
)

from .models import Booking, TimeSlot
from .serializers import BookingEarningsSerializer, BookingSerializer


def booking_list(request):
    if request.method == 'GET':
        bookings = Booking.objects.all()
        bookings_serializer = [BookingSerializer(booking).serialize() for booking in bookings]
        return JsonResponse(bookings_serializer, safe=False, status=200)


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('service', 'time_slot', 'date', model=Booking)
@verify_token
def create_booking(request):
    service_pk = request.json_body['service']
    date = request.json_body['date']
    time_slot_pk = request.json_body['time_slot']

    service = Service.objects.get(pk=service_pk)
    time_slot = TimeSlot.objects.get(pk=time_slot_pk)
    booking = Booking.objects.create(
        user=request.user, service=service, date=date, time_slot=time_slot
    )

    return JsonResponse({'id': booking.pk})


def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    serializer = BookingSerializer(booking, request=request)
    return serializer.json_response()


def earnings_summary(request):
    serializer = BookingEarningsSerializer(None, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
def edit_booking(request, booking_pk):
    service_pk = request.json_body['service']
    date = request.json_body['date']
    time_slot_pk = request.json_body['time_slot']
    service = Service.objects.get(pk=service_pk)
    time_slot = TimeSlot.objects.get(pk=time_slot_pk)
    booking = Booking.objects.get(pk=booking_pk)
    booking.service = service
    booking.date = date
    booking.time_slot = time_slot
    booking.save()
    return JsonResponse({'msg': 'Booking has been edited'})


@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
def delete_booking(request, booking_pk):
    booking = Booking.objects.get(pk=booking_pk)
    booking.delete()
    return JsonResponse({'msg': 'Event has been deleted'})
