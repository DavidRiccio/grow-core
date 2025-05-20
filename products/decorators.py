from django.http import JsonResponse

from .models import Product


def verify_product(func):
    """
    Verifica que el producto especificado exista.

    Este decorador intenta obtener un producto de la base de datos utilizando
    el ID proporcionado en los argumentos de la función. Si el producto existe,
    se asigna al objeto de solicitud. Si no se encuentra el producto, se devuelve
    un error 404.

    :param func: La función a la que se aplica el decorador.
    :return: Función envuelta que verifica la existencia del producto.
    """

    def wrapper(request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['product_pk'])
            request.product = product
        except Product.DoesNotExist:  # Corrección aquí: 'DoesNotExists' debe ser 'DoesNotExist'
            return JsonResponse({'error': 'Product not found'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper
