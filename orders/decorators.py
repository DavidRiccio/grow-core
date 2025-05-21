import re
from datetime import datetime

from django.http import JsonResponse

from .models import Order


def verify_user(func):
    """
    Verifica que el usuario autenticado sea el propietario de la orden.

    Si el usuario que realiza la solicitud no es el propietario de la orden
    especificada en `order_pk`, se devuelve una respuesta con error 403 (Forbidden).

    Parameters
    ----------
    func : callable
        Vista a decorar.

    Returns
    -------
    callable
        Vista decorada que incluye la verificación de propiedad del usuario.
    """

    def wrapper(request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['order_pk'])
        if order.user != request.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        return func(request, *args, **kwargs)

    return wrapper


def verify_order(func):
    """
    Verifica si la orden especificada por `order_pk` existe.

    Si existe, se asigna a `request.order`; de lo contrario, se retorna un error 404.

    Parameters
    ----------
    func : callable
        Vista a decorar.

    Returns
    -------
    callable
        Vista decorada con la validación de existencia de la orden.
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
    Valida los datos de la tarjeta de crédito enviados en la solicitud.

    Comprueba el formato del número de tarjeta, la fecha de expiración y el CVC.
    También verifica que la tarjeta no esté expirada.

    Parameters
    ----------
    func : callable
        Vista a decorar.

    Returns
    -------
    callable
        Vista decorada que incluye la validación de los datos de la tarjeta.
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
    Valida el estado actual de una orden antes de permitir cambios.

    Impide modificar órdenes con estado `CANCELLED` o `COMPLETED`.

    Requiere que `request.order` esté definido.

    Parameters
    ----------
    func : callable
        Vista a decorar.

    Returns
    -------
    callable
        Vista decorada que incluye la validación del estado de la orden.
    """

    def wrapper(request, *args, **kwargs):
        if request.order.status == Order.Status.CANCELLED:
            return JsonResponse({'error': 'You cannot modify a canceled order.'}, status=400)
        if request.order.status == Order.Status.COMPLETED:
            return JsonResponse({'error': 'You cannot modify a completed order.'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper
