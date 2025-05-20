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

from .decorators import validate_credit_card, verify_order, verify_order_item
from .models import Order, OrderItem
from .serializers import OrderSerializer


@login_required
@csrf_exempt
@required_method('GET')
def order_list(request):
    orders = OrderSerializer(Order.objects.all())
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
    order = Order.objects.create(user=request.user)
    OrderItem.objects.create(order=order)
    return JsonResponse({'id': order.pk})


@login_required
@csrf_exempt
@required_method('POST')
@verify_token
@verify_order
def delete_order(request, order_pk: int):
    order = request.order
    order.delete()
    return JsonResponse({'msg': 'Product has been deleted'})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('id', model=Product)
@verify_token
@verify_order
@verify_order_item
def add_product_to_order(request, order_pk: int):
    order_item = request.order_item
    try:
        product = Product.objects.get(pk=request.json_body['id'])
    except Product.DoesNotExist:
        return JsonResponse({'msg': 'Product not found'}, status=404)
    order_item.add(product)
    order_item.decrease_stock()
    return JsonResponse({'msg': f'Se añadio correctamente el Producto {product}'})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('card-number', 'exp-date', 'cvc', model=Order)
@verify_token
@verify_order
@validate_credit_card
def pay_order(request, order_pk: int):
    request.order.update_status(Order.Status.COMPLETED)
    return JsonResponse({'msg': 'Your order has been paid successfully'})


@csrf_exempt
@required_method('POST')
@verify_token
@verify_order
def cancell_order(request, order_pk: int):
    request.order.update_status(Order.Status.CANCELLED)
    request.order.increase_stock()
    return JsonResponse({'msg': 'Your order has been cancelled successfully'})
