import re
from datetime import datetime

from django.http import JsonResponse

from .models import Order


def verify_user(func):
    """
    Decorador que verifica si el usuario autenticado es el propietario de la orden.

    Si el usuario que realiza la solicitud no es el dueño de la orden especificada en 'order_pk',
    se devuelve una respuesta JSON con error 403 (Forbidden).

    Args:
        func (callable): Vista a decorar.

    Returns:
        callable: Vista decorada que incluye la verificación del usuario.
    """

    def wrapper(request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['order_pk'])

        if order.user != request.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        return func(request, *args, **kwargs)

    return wrapper


def verify_order(func):
    """
    Decorador que intenta recuperar la orden según el 'order_pk' de la URL.

    Si la orden existe, se adjunta al objeto request como 'request.order'.
    Si no existe, devuelve una respuesta JSON con error 404 (Not Found).

    Args:
        func (callable): Vista a decorar.

    Returns:
        callable: Vista decorada que incluye la verificación de existencia de la orden.
    """

    def wrapper(request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['order_pk'])
            request.order = order
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper


def validate_credit_card(func):
    """
    Decorador que valida los datos de la tarjeta de crédito enviados en el cuerpo JSON de la solicitud.

    Verifica el formato del número de tarjeta, la fecha de expiración y el CVC.
    También comprueba que la tarjeta no esté expirada.
    Devuelve una respuesta JSON con error 400 si alguno de los campos es inválido.

    Args:
        func (callable): Vista a decorar.

    Returns:
        callable: Vista decorada que incluye la validación de la tarjeta de crédito.
    """

    def wrapper(request, *args, **kwargs):
        CARD_NUMBER_PATTERN = re.compile(r'^\d{4}-\d{4}-\d{4}-\d{4}$')
        EXP_DATE_PATTERN = re.compile(r'^(0[1-9]|1[0-2])\/\d{4}$')
        CVC_PATTERN = re.compile(r'^\d{3}$')
        card_number = request.json_body['card-number']
        exp_date = request.json_body['exp-date']
        cvc = request.json_body['cvc']
        if not CARD_NUMBER_PATTERN.match(card_number):
            return JsonResponse({'error': 'Invalid card number'}, status=400)
        if not EXP_DATE_PATTERN.match(exp_date):
            return JsonResponse({'error': 'Invalid expiration date'}, status=400)
        if not CVC_PATTERN.match(cvc):
            return JsonResponse({'error': 'Invalid CVC'}, status=400)
        card_exp_date = datetime.strptime(exp_date, '%m/%Y')
        current_date = datetime.now()
        if card_exp_date < current_date:
            return JsonResponse({'error': 'Card expired'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


def validate_status(func):
    """
    Decorador que valida el estado de una orden antes de permitir modificaciones.

    Si la orden tiene estado 'CANCELLED' o 'COMPLETED', devuelve un error 400 (Bad Request)
    indicando que no se puede modificar la orden.

    Requiere que 'request.order' esté definido (usualmente proporcionado por el decorador verify_order).

    Args:
        func (callable): Vista a decorar.

    Returns:
        callable: Vista decorada con validación de estado de la orden.
    """

    def wrapper(request, *args, **kwargs):
        if request.order.status == Order.Status.CANCELLED:
            return JsonResponse({'error': 'You cannot modify a canceled order.'}, status=400)
        if request.order.status == Order.Status.COMPLETED:
            return JsonResponse({'error': 'You cannot modify a completed order.'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper
