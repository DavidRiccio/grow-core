# Create your views here.
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
