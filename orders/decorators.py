import re
from datetime import datetime

from django.http import JsonResponse

from .models import Order


def verify_user(func):
    def wrapper(request, order_pk, *args, **kwargs):
        order = Order.objects.get(pk=order_pk)

        if order.user != request.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        return func(request, order_pk, *args, **kwargs)

    return wrapper


def verify_order(func):
    def wrapper(request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs['order_pk'])
            request.order = order
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper


def validate_credit_card(func):
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
