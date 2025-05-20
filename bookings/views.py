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

from .decorators import (
    validate_barber_and_timeslot_existence,
    validate_barber_availability,
    verify_booking,
)
from .models import Booking
from .serializers import BookingEarningsSerializer, BookingSerializer

User = get_user_model()


@login_required
@csrf_exempt
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
@validate_barber_and_timeslot_existence
@validate_barber_availability
def create_booking(request):
    service_pk = request.json_body['service']
    date = request.json_body['date']

    try:
        service = Service.objects.get(pk=service_pk)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Servicio no encontrado.'}, status=400)

    booking = Booking.objects.create(
        user=request.user,
        barber=request.barber_profile.user,
        service=service,
        date=date,
        time_slot=request.time_slot,
    )

    return JsonResponse({'id': booking.pk})


@login_required
@csrf_exempt
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
@validate_barber_and_timeslot_existence
@validate_barber_availability
def edit_booking(request, booking_pk):
    service_pk = request.json_body['service']
    date = request.json_body['date']

    service = Service.objects.get(pk=service_pk)
    booking = request.booking

    booking.service = service
    booking.barber = request.barber_profile.user
    booking.date = date
    booking.time_slot = request.time_slot
    booking.save()

    return JsonResponse({'msg': 'Booking has been edited'})


@login_required
@csrf_exempt
@required_method('GET')
@verify_booking
def booking_detail(request, booking_pk):
    booking = request.booking
    serializer = BookingSerializer(booking, request=request)
    return serializer.json_response()


@login_required
@csrf_exempt
@required_method('POST')
@verify_token
@verify_booking
def delete_booking(request, booking_pk):
    booking = request.booking
    booking.delete()
    return JsonResponse({'msg': 'Booking has been deleted'})
