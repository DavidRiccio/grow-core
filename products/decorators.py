from django.http import JsonResponse

from .models import Product


def verify_product(func):
    """
    Decorador que verifica la existencia de un producto por su ID.

    Este decorador intenta recuperar un producto desde la base de datos utilizando
    el parámetro 'product_pk' proporcionado en la URL. Si el producto existe, se
    adjunta al objeto `request` como `request.product` para que esté disponible
    en la vista. Si el producto no existe, retorna una respuesta JSON con error 404.

    :param func: Función vista a la que se aplicará el decorador.
    :return: Función decorada que incluye la verificación del producto.
    """

    def wrapper(request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['product_pk'])
            request.product = product
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper
