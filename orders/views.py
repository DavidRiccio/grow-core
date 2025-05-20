from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from products.models import Product
from shared.decorators import (
    load_json_body,
    required_fields,
    required_method,
    verify_token,
)

from .decorators import validate_credit_card, verify_order
from .models import Order
from .serializers import OrderSerializer


@login_required
@csrf_exempt
@required_method('GET')
def order_list(request):
    orders = OrderSerializer(Order.objects.all(), request=request)
    return orders.json_response()


@login_required
@csrf_exempt
@required_method('GET')
@verify_order
def order_detail(request, order_pk: int):
    serializer = OrderSerializer(request.order, request=request)
    return serializer.json_response()


@login_required
@csrf_exempt
@required_method('POST')
@verify_token
def add_order(request):
    # Crear orden usando el serializador (ahora maneja productos)
    serializer = OrderSerializer(data=request.POST, context={'request': request})
    if serializer.is_valid():
        order = serializer.save()
        return JsonResponse({'id': order.pk})
    return JsonResponse(serializer.errors, status=400)


@login_required
@csrf_exempt
@required_method('POST')
@verify_token
@verify_order
def delete_order(request, order_pk: int):
    order = request.order
    order.delete()
    return JsonResponse({'msg': 'Order has been deleted'})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('id', model=Product)
@verify_token
@verify_order
def add_product_to_order(request, order_pk: int):
    order = request.order
    try:
        product = Product.objects.get(pk=request.json_body['id'])
    except Product.DoesNotExist:
        return JsonResponse({'msg': 'Product not found'}, status=404)
    order.add(product)
    # Stock se manejará al confirmar la orden, no aquí
    return JsonResponse({'msg': f'Producto {product} añadido correctamente'})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('card-number', 'exp-date', 'cvc', model=Order)
@verify_token
@verify_order
@validate_credit_card
def pay_order(request, order_pk: int):
    try:
        request.order.confirm_order()  # Nuevo método integrado
        return JsonResponse({'msg': 'Orden pagada y confirmada'})
    except Exception as e:
        return JsonResponse({'msg': str(e)}, status=400)


@csrf_exempt
@required_method('POST')
@verify_token
@verify_order
def cancell_order(request, order_pk: int):
    try:
        request.order.cancel_order()  # Nuevo método que maneja stock y estado
        return JsonResponse({'msg': 'Orden cancelada correctamente'})
    except Exception as e:
        return JsonResponse({'msg': str(e)}, status=400)
