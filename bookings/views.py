from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
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

from .decorators import (
    validate_barber_and_timeslot_existence,
    validate_barber_availability,
    verify_booking,
)
from .models import Booking
from .serializers import BookingSerializer
from .utils import get_available_time_slots, is_working_day

User = get_user_model()


@csrf_exempt
@required_method('GET')
@verify_token
def user_booking_list(request):
    """
    Devuelve una lista de todas las reservas de usuario en formato JSON.

    Este endpoint requiere que el usuario esté autenticado.
    Realiza una consulta a la base de datos para obtener todas las reservas de un usuario
    y las serializa antes de devolverlas en una respuesta JSON.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    JsonResponse
        Respuesta JSON con la lista de reservas.
    """
    bookings = Booking.objects.filter(user=request.user)
    bookings_serializer = [BookingSerializer(booking).serialize() for booking in bookings]
    return JsonResponse(bookings_serializer, safe=False, status=200)


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('service', 'time_slot', 'date', 'barber', model=Booking)
@verify_token
@validate_barber_and_timeslot_existence
@validate_barber_availability
def create_booking(request):
    """
    Crea una nueva reserva.

    Este endpoint permite a un usuario autenticado crear una nueva reserva
    proporcionando el servicio, el horario, la fecha y el barbero.
    Si el servicio no existe, devuelve un error.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP que contiene los datos de la reserva.

    Returns
    -------
    JsonResponse
        Respuesta JSON con el ID de la nueva reserva o un error si el servicio no se encuentra.
    """
    service_pk = request.json_body['service']
    barber_id = request.json_body['barber']
    date = request.json_body['date']

    try:
        service = Service.objects.get(pk=service_pk)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Servicio no encontrado.'}, status=400)

    try:
        # Buscar al barbero con su perfil y rol de WORKER
        barber_profile = Profile.objects.get(user_id=barber_id, role=Profile.Role.WORKER)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Barbero no encontrado o no válido.'}, status=404)

    booking = Booking.objects.create(
        user=request.user,
        barber=barber_profile.user,
        service=service,
        date=date,
        time_slot=request.time_slot,
    )

    return JsonResponse({'id': booking.pk})


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
    """
    Edita una reserva existente.

    Este endpoint permite a un usuario autenticado editar una reserva
    existente proporcionando el nuevo servicio, horario, fecha y barbero.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP que contiene los datos de la reserva.
    booking_pk : int
        ID de la reserva a editar.

    Returns
    -------
    JsonResponse
        Respuesta JSON con un mensaje de éxito.
    """
    service_pk = request.json_body['service']
    date = request.json_body['date']

    service = Service.objects.get(pk=service_pk)
    booking = request.booking

    booking.service = service
    booking.barber = request.barber_profile.user
    booking.date = date
    booking.time_slot = request.time_slot
    booking.save()

    return JsonResponse({'msg': 'La reserva ha sido editada'})


@login_required
@csrf_exempt
@required_method('GET')
@verify_booking
def booking_detail(request, booking_pk):
    """
    Devuelve los detalles de una reserva específica.

    Este endpoint permite a un usuario autenticado obtener los detalles
    de una reserva específica utilizando su ID.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.
    booking_pk : int
        ID de la reserva.

    Returns
    -------
    JsonResponse
        Respuesta JSON con los detalles de la reserva.
    """
    booking = request.booking
    serializer = BookingSerializer(booking, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@verify_token
@verify_booking
def cancel_booking(request, booking_pk):
    """
    Cancela una reserva existente.

    Este endpoint permite a un usuario autenticado Cancela una reserva
    específica utilizando su ID.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.
    booking_pk : int
        ID de la reserva a Cancelar.

    Returns
    -------
    JsonResponse
        Respuesta JSON con un mensaje de éxito.
    """
    booking = request.booking
    booking.delete()
    return JsonResponse({'msg': 'La reserva ha sido cancelada'})


@csrf_exempt
@required_method('GET')
@verify_token
def get_available_dates(request):
    """
    Devuelve las fechas disponibles para reservas de un barbero específico.

    Parámetros GET:
    - barber_id: ID del barbero para filtrar (requerido)

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    JsonResponse
        Respuesta JSON con las fechas y horarios disponibles para el barbero especificado.
    """
    barber_id = request.GET.get('barber_id')

    if not barber_id:
        return JsonResponse({'error': 'El parámetro barber_id es requerido'}, status=400)

    try:
        barber = User.objects.get(id=barber_id, profile__role=Profile.Role.WORKER)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Barbero no encontrado'}, status=404)

    now = timezone.now()
    today = now.date()
    start_date = today
    end_date = today + timedelta(days=13)  # 14 días desde hoy, incluyendo hoy.

    available_slots = {}
    current_date = start_date

    while current_date <= end_date:
        if is_working_day(current_date):
            current_time = now.time() if current_date == today else None
            available_slots[current_date.isoformat()] = get_available_time_slots(
                barber, current_date, current_time
            )
        current_date += timedelta(days=1)

    return JsonResponse(
        {
            'barber_id': barber.id,
            'barber_name': barber.get_full_name() or barber.username,
            'available_dates': available_slots,
        }
    )


@csrf_exempt
@required_method('GET')
@verify_token
@verify_admin
def get_earnings(request):
    """
    Obtiene las ganancias diarias del mes actual basadas en reservas confirmadas.

    Esta vista recorre cada día del mes actual y calcula el total de ingresos generados
    por las reservas confirmadas (status = CONFIRMED). Las ganancias se determinan
    a partir del precio del servicio asociado a cada reserva.

    Parámetros
    ----------
    request : HttpRequest
        La solicitud HTTP entrante. Debe ser de tipo GET y debe incluir un token de autenticación válido.
        Solo accesible por usuarios con permisos de administrador.

    Retorna
    -------
    JsonResponse
        Un objeto JSON con:
            - 'labels': Lista de fechas (str) en formato 'YYYY-MM-DD'.
            - 'values': Lista de floats representando las ganancias totales por día.

    Ejemplo
    -------
    {
        "labels": ["2025-05-01", "2025-05-02", ..., "2025-05-31"],
        "values": [100.0, 75.5, ..., 120.0]
    }
    """
    now = timezone.now()
    first_day_of_month = now.replace(day=1)
    last_day_of_month = (first_day_of_month + timezone.timedelta(days=31)).replace(
        day=1
    ) - timezone.timedelta(days=1)

    total_earnings = []
    labels = []

    for day in range(1, last_day_of_month.day + 1):
        date = first_day_of_month.replace(day=day)
        bookings = Booking.objects.filter(created_at__date=date, status=Booking.Status.CONFIRMED)
        earnings = sum(booking.service.price for booking in bookings)
        total_earnings.append(earnings)
        labels.append(date.strftime('%Y-%m-%d'))

    return JsonResponse(
        {
            'labels': labels,
            'values': total_earnings,
        }
    )
