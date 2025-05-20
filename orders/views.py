from decimal import Decimal

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

from .decorators import validate_credit_card, validate_status, verify_order, verify_user
from .models import Order
from .serializers import OrderSerializer


@login_required
@csrf_exempt
@required_method('GET')
@verify_order
@verify_user
def order_detail(request, order_pk: int):
    """
    Devuelve los detalles de un pedido específico.

    Este endpoint permite a un usuario autenticado obtener los detalles de un pedido
    utilizando su ID. Solo se puede acceder a este endpoint si el pedido existe y
    pertenece al usuario.

    :param request: Objeto de solicitud HTTP.
    :param order_pk: ID del pedido.
    :return: JsonResponse con los detalles del pedido.
    """
    serializer = OrderSerializer(request.order, request=request)
    return serializer.json_response()


@login_required
@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
def add_order(request):
    """
    Agrega un nuevo pedido.

    Este endpoint permite a un usuario autenticado crear un nuevo pedido
    proporcionando los productos y sus cantidades. Se verifica la disponibilidad
    de stock antes de completar el pedido.

    :param request: Objeto de solicitud HTTP que contiene los datos del pedido.
    :return: JsonResponse con el ID del nuevo pedido creado o un error si hay problemas con el stock.
    """
    order_data = request.json_body
    order = Order(user=request.user)
    order.save()
    total_price = Decimal('0.00')
    for item in order_data['products']:
        product_pk = item['id']
        quantity = item['quantity']
        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with id {product_pk} not found'}, status=404)
        if product.stock < quantity:
            return JsonResponse({'error': f'Insufficient stock for {product.name}'}, status=400)
        product.stock -= quantity
        product.save()
        order.products.add(product)
        total_price += product.price * Decimal(quantity)
    order.price = total_price
    order.save()

    return JsonResponse({'id': order.pk})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('card-number', 'exp-date', 'cvc', model=Order)
@verify_token
@verify_order
@validate_credit_card
@verify_user
@validate_status
def pay_order(request, order_pk: int):
    """
    Procesa el pago de un pedido.

    Este endpoint permite a un usuario autenticado completar el pago de un pedido
    utilizando la información de la tarjeta de crédito. Cambia el estado del pedido a
    "COMPLETADO".

    :param request: Objeto de solicitud HTTP que contiene los datos de pago.
    :param order_pk: ID del pedido a pagar.
    :return: JsonResponse con un mensaje de éxito.
    """
    request.order.status = Order.Status.COMPLETED
    request.order.save()
    return JsonResponse({'msg': 'Your order has been paid and complete successfully'})


@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
@verify_order
@verify_user
@validate_status
def cancell_order(request, order_pk: int):
    """
    Cancela un pedido existente.

    Este endpoint permite a un usuario autenticado cancelar un pedido.
    Se restablece el stock de los productos del pedido y se cambia el estado
    del pedido a "CANCELADO".

    :param request: Objeto de solicitud HTTP que contiene los datos del pedido.
    :param order_pk: ID del pedido a cancelar.
    :return: JsonResponse con un mensaje de éxito o un error si hay problemas con los productos.
    """
    order_data = request.json_body
    for item in order_data['products']:
        product_pk = item['id']
        quantity = item['quantity']
        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with id {product_pk} not found'}, status=404)
        product.stock += quantity
        product.save()
    request.order.status = Order.Status.CANCELLED
    request.order.save()
    return JsonResponse({'msg': f'Order {order_pk} has been cancelled'})
