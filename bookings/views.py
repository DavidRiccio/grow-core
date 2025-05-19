from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from services.models import Service
from shared.decorators import (
    load_json_body,
    required_fields,
    required_method,
    verify_admin,
    verify_token,
)
from users.models import Profile

from .decorators import verify_barber, verify_booking, verify_time_slot
from .models import Booking, TimeSlot
from .serializers import BookingEarningsSerializer, BookingSerializer

User = get_user_model()


@login_required
@required_method('GET')
def booking_list(request):
    bookings = Booking.objects.all()
    bookings_serializer = [BookingSerializer(booking).serialize() for booking in bookings]
    return JsonResponse(bookings_serializer, safe=False, status=200)


@login_required
@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('service', 'time_slot', 'date', 'barber', model=Booking)
@verify_token
def create_booking(request):
    service_pk = request.json_body['service']
    date = request.json_body['date']

    service = Service.objects.get(pk=service_pk)
    barber = Profile.objects.get(pk=request.json_body['barber'])
    time_slot = TimeSlot.objects.get(pk=request.json_body['time_slot'])

    booking = Booking.objects.create(
        user=request.user,
        barber=barber.user,
        service=service,
        date=date,
        time_slot=time_slot,
    )

    return JsonResponse({'id': booking.pk})


@login_required
@required_method('GET')
@verify_admin
def earnings_summary(request):
    serializer = BookingEarningsSerializer(None, request=request)
    return serializer.json_response()


@login_required
@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('service', 'time_slot', 'date', 'barber', model=Booking)
@verify_token
@verify_booking
@verify_time_slot
@verify_barber
def edit_booking(request, booking_pk):
    service_pk = request.json_body['service']
    date = request.json_body['date']

    service = Service.objects.get(pk=service_pk)
    time_slot = request.time_slot.pk
    barber = request.barber.pk
    booking = request.booking

    booking.service = service
    booking.barber = barber
    booking.date = date
    booking.time_slot = time_slot
    booking.save()

    return JsonResponse({'msg': 'Booking has been edited'})


@login_required
@required_method('GET')
@verify_booking
def booking_detail(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    serializer = BookingSerializer(booking, request=request)
    return serializer.json_response()


@login_required
@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
@verify_booking
def delete_booking(request, booking_pk):
    booking = Booking.objects.get(pk=booking_pk)
    booking.delete()
    return JsonResponse({'msg': 'Event has been deleted'})
