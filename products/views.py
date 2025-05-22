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


@required_method('GET')
def product_list(request):
    """
    Devuelve una lista de todos los productos en formato JSON.

    Este endpoint permite obtener todos los productos registrados en la base de datos.
    Los productos se serializan y se devuelven en una respuesta JSON.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    JsonResponse
        Respuesta JSON con la lista de productos.
    """
    products = ProductSerializer(Product.objects.all())
    return products.json_response()


@csrf_exempt
@required_method('GET')
@verify_product
def product_detail(request, product_pk):
    """
    Devuelve los detalles de un producto específico.

    Este endpoint permite obtener los detalles de un producto utilizando su ID.
    Solo se puede acceder a este endpoint si el producto existe.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.
    product_pk : int
        ID del producto.

    Returns
    -------
    JsonResponse
        Respuesta JSON con los detalles del producto.
    """
    serializer = ProductSerializer(request.product, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'price', 'stock', model=Product)
@verify_token
@verify_admin
def add_product(request):
    """
    Agrega un nuevo producto.

    Este endpoint permite a un administrador autenticado crear un nuevo producto
    proporcionando el nombre, descripción, precio y stock del producto.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP que contiene los datos del nuevo producto.

    Returns
    -------
    JsonResponse
        Respuesta JSON con el ID del nuevo producto creado.
    """
    name = request.json_body['name']
    description = request.json_body['description']
    price = request.json_body['price']
    stock = request.json_body['stock']

    product = Product.objects.create(name=name, description=description, price=price, stock=stock)
    return JsonResponse({'id': product.pk})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'price', 'stock', model=Product)
@verify_token
@verify_admin
@verify_product
def edit_product(request, product_pk: int):
    """
    Edita un producto existente.

    Este endpoint permite a un administrador autenticado editar un producto
    existente proporcionando los nuevos datos del producto.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP que contiene los datos del producto.
    product_pk : int
        ID del producto a editar.

    Returns
    -------
    JsonResponse
        Respuesta JSON con un mensaje de éxito.
    """
    product = request.product
    product.name = request.json_body['name']
    product.description = request.json_body['description']
    product.price = request.json_body['price']
    product.stock = request.json_body['stock']
    product.image = request.image
    product.save()
    return JsonResponse({'msg': 'El producto ha sido editado'})


@csrf_exempt
@required_method('POST')
@verify_token
@verify_admin
@verify_product
def delete_product(request, product_pk: int):
    """
    Elimina un producto existente.

    Este endpoint permite a un administrador autenticado eliminar un producto
    específico utilizando su ID.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.
    product_pk : int
        ID del producto a eliminar.

    Returns
    -------
    JsonResponse
        Respuesta JSON con un mensaje de éxito.
    """
    product = request.product
    product.delete()
    return JsonResponse({'msg': 'El producto ha sido eliminado'})
