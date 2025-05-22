from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from products.models import Product
from shared.decorators import (
    load_json_body,
    required_fields,
    required_method,
    verify_admin,
    verify_token,
)

from .decorators import validate_credit_card, validate_status, verify_order, verify_user
from .models import Order
from .serializers import OrderSerializer


@csrf_exempt
@required_method('GET')
@verify_token
def user_order_list(request):
    """
    Recupera los detalles de un pedido específico.

    Este endpoint permite a un usuario autenticado obtener la información de una orden,
    validando que el pedido exista y que pertenezca al usuario que realiza la solicitud.

    Decoradores aplicados:
        - csrf_exempt: Exime de la verificación CSRF.
        - required_method('GET'): Restringe el método HTTP a GET.
        - verify_user: Verifica que el usuario autenticado sea el propietario de la orden.

    :param request: Objeto de solicitud HTTP.
    :param order_pk: ID de la orden a recuperar.
    :return: JsonResponse con los datos serializados de la orden.
    """
    orders = Order.objects.filter(user=request.user)
    orders_serializer = [OrderSerializer(order).serialize() for order in orders]
    return JsonResponse(orders_serializer, safe=False, status=200)


@login_required
@csrf_exempt
@required_method('GET')
@verify_order
@verify_user
def order_detail(request, order_pk: int):
    """
    Recupera los detalles de un pedido específico.

    Este endpoint permite a un usuario autenticado obtener la información de una orden,
    validando que el pedido exista y que pertenezca al usuario que realiza la solicitud.

    Decoradores aplicados:
        - login_required: Verifica que el usuario esté autenticado.
        - csrf_exempt: Exime de la verificación CSRF.
        - required_method('GET'): Restringe el método HTTP a GET.
        - verify_order: Carga la orden en request.order si existe.
        - verify_user: Verifica que el usuario autenticado sea el propietario de la orden.

    :param request: Objeto de solicitud HTTP.
    :param order_pk: ID de la orden a recuperar.
    :return: JsonResponse con los datos serializados de la orden.
    """
    serializer = OrderSerializer(request.order, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
def add_order(request):
    """
    Crea una nueva orden de pedido.

    Este endpoint permite a un usuario autenticado generar una orden,
    siempre que exista suficiente stock para los productos solicitados.
    Calcula el precio total y actualiza el stock de los productos.

    Decoradores aplicados:
        - csrf_exempt: Exime de la verificación CSRF.
        - required_method('POST'): Restringe el método HTTP a POST.
        - load_json_body: Carga el cuerpo de la solicitud como JSON.
        - verify_token: Verifica que el token de autenticación sea válido.

    :param request: Objeto de solicitud HTTP con los datos de productos.
    :return: JsonResponse con el ID de la orden creada o un mensaje de error.
    """
    order_data = request.json_body
    order = Order(user=request.user)
    order.save()
    total_price = Decimal('0.00')
    for item in order_data['products']:
        product_pk = item['id']
        quantity = item['quantity']
        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with id {product_pk} not found'}, status=404)
        if product.stock < quantity:
            return JsonResponse({'error': f'Insufficient stock for {product.name}'}, status=400)
        product.stock -= quantity
        product.save()
        order.products.add(product)
        total_price += product.price * Decimal(quantity)
    order.price = total_price
    order.save()

    return JsonResponse({'id': order.pk})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('card-number', 'exp-date', 'cvc', model=Order)
@verify_token
@verify_order
@validate_credit_card
@verify_user
@validate_status
def pay_order(request, order_pk: int):
    """
    Procesa el pago de una orden.

    Cambia el estado de la orden a 'COMPLETED' si se valida correctamente la tarjeta.
    Solo se puede pagar una orden válida, pendiente y propiedad del usuario autenticado.

    Decoradores aplicados:
        - csrf_exempt: Exime de la verificación CSRF.
        - required_method('POST'): Restringe el método HTTP a POST.
        - load_json_body: Carga el cuerpo de la solicitud como JSON.
        - required_fields: Verifica la presencia de campos de pago.
        - verify_token: Verifica el token JWT del usuario.
        - verify_order: Carga la orden si existe.
        - validate_credit_card: Valida los campos de la tarjeta.
        - verify_user: Verifica que el usuario sea el dueño de la orden.
        - validate_status: Verifica que la orden esté en estado 'PENDING'.

    :param request: Objeto de solicitud HTTP con los datos de pago.
    :param order_pk: ID de la orden a pagar.
    :return: JsonResponse con un mensaje de confirmación.
    """
    request.order.status = Order.Status.COMPLETED
    request.order.save()
    return JsonResponse({'msg': 'Your order has been paid and complete successfully'})


@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
@verify_order
@verify_user
@validate_status
def cancel_order(request, order_pk: int):
    """
    Cancela una orden de pedido.

    Cambia el estado de la orden a 'CANCELLED' y repone el stock de los productos involucrados.
    Solo se puede cancelar una orden válida, pendiente y propiedad del usuario.

    Decoradores aplicados:
        - csrf_exempt: Exime de la verificación CSRF.
        - required_method('POST'): Restringe el método HTTP a POST.
        - load_json_body: Carga el cuerpo de la solicitud como JSON.
        - verify_token: Verifica el token JWT del usuario.
        - verify_order: Carga la orden si existe.
        - verify_user: Verifica que el usuario sea el dueño de la orden.
        - validate_status: Verifica que la orden no esté ya cancelada o completada.

    :param request: Objeto de solicitud HTTP con los productos a devolver.
    :param order_pk: ID de la orden a cancelar.
    :return: JsonResponse con un mensaje de éxito o de error si falla.
    """
    order_data = request.json_body
    for item in order_data['products']:
        product_pk = item['id']
        quantity = item['quantity']
        try:
            product = Product.objects.get(pk=product_pk)
        except Product.DoesNotExist:
            return JsonResponse({'error': f'Product with id {product_pk} not found'}, status=404)
        product.stock += quantity
        product.save()
    request.order.status = Order.Status.CANCELLED
    request.order.save()
    return JsonResponse({'msg': f'Order {order_pk} has been cancelled'})


@csrf_exempt
@required_method('GET')
@verify_token
@verify_admin
def get_earnings(request):
    now = timezone.now()
    first_day_of_month = now.replace(day=1)
    last_day_of_month = (first_day_of_month + timezone.timedelta(days=31)).replace(
        day=1
    ) - timezone.timedelta(days=1)
    total_earnings = []
    labels = []
    for day in range(1, last_day_of_month.day + 1):
        date = first_day_of_month.replace(day=day)
        orders = Order.objects.filter(created_at__date=date, status=Order.Status.COMPLETED)
        earnings = 0
        for order in orders:
            earnings += order.price
        total_earnings.append(earnings)
        labels.append(date.strftime('%Y-%m-%d'))
    return JsonResponse(
        {
            'labels': labels,
            'values': total_earnings,
        }
    )
