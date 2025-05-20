from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import (
    load_json_body,
    required_fields,
    required_method,
    verify_admin,
    verify_token,
)

from .decorators import verify_product
from .models import Product
from .serializers import ProductSerializer


@csrf_exempt
@required_method('GET')
def product_list(request):
    products = ProductSerializer(Product.objects.all())
    return products.json_response()


@csrf_exempt
@required_method('GET')
@verify_product
def product_detail(request, product_pk):
    serializer = ProductSerializer(request.product, request=request)
    return serializer.json_response()


@login_required
@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'price', 'stock', model=Product)
@verify_token
@verify_admin
def add_product(request):
    name = request.json_body['name']
    description = request.json_body['description']
    price = request.json_body['price']
    stock = request.json_body['stock']

    product = Product.objects.create(name=name, description=description, price=price, stock=stock)
    return JsonResponse({'id': product.pk})


@login_required
@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'price', 'stock', model=Product)
@verify_token
@verify_admin
@verify_product
def edit_product(request, product_pk: int):
    product = request.product
    product.name = request.json_body['name']
    product.description = request.json_body['description']
    product.price = request.json_body['price']
    product.stock = request.json_body['stock']
    product.image = request.image
    product.save()
    return JsonResponse({'msg': 'Product has been edited'})


@login_required
@csrf_exempt
@required_method('POST')
@verify_token
@verify_admin
@verify_product
def delete_product(request, product_pk: int):
    product = request.product
    product.delete()
    return JsonResponse({'msg': 'Product has been deleted'})
