# Create your views here.
from .models import Order
from .serializers import OrderSerializer


def order_list(request):
    orders = OrderSerializer(Order.objects.all())
    return orders.json_response()


def order_detail(request, order_pk):
    pass
