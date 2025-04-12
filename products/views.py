from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

# Create your views here.


def product_list(request):
    products = ProductSerializer(Product.objects.all())
    return products.json_response()


def product_detail(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    serializer = ProductSerializer(product, request=request)
    return serializer.json_response()
