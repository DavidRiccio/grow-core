from django.http import JsonResponse

from .models import Product


def verify_product(func):
    def wrapper(request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['product_pk'])
            request.product = product
        except Product.DoesNotExists:
            return JsonResponse({'error', 'Product not found'}, status=404)
