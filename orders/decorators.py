from django.http import JsonResponse

from .models import Order


def verify_order(func):
    def wrapper(request, order_pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=order_pk)
            request.order = order
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        return func(request, order_pk, *args, **kwargs)

    return wrapper
