from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from products.models import Product
from shared.decorators import load_json_body, required_fields, required_method, verify_token

from .decorators import verify_order
from .models import Order
from .serializers import OrderSerializer


def order_list(request):
    orders = OrderSerializer(Order.objects.all())
    return orders.json_response()


@verify_order
def order_detail(request, order_pk: int):
    serializer = OrderSerializer(request.order, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@verify_token
def add_order(request):
    order = Order.objects.create(user=request.user)
    return JsonResponse({'id': order.pk})


@csrf_exempt
@required_method('POST')
@verify_token
def delete_order(request, order_pk: int):
    order = Order.objects.get(pk=order_pk)
    order.delete()
    return JsonResponse({'msg': 'Product has been deleted'})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('id', model=Product)
@verify_token
def add_product_to_order(request, order_pk: int):
    order = Order.objects.get(pk=order_pk)
    product = Product.objects.get(pk=request.json_body['id'])
    order.add(product)
    order.decrease_stock()
    return JsonResponse({'msg': f'Se añadio correctamente el Producto {product}'})
