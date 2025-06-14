from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
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
from .models import Order, OrderItem
from .serializers import OrderSerializer


@csrf_exempt
@required_method('GET')
@verify_token
def user_order_list(request):
    """
    Recupera todas las órdenes del usuario autenticado.

    Este endpoint permite a un usuario autenticado obtener la lista de todas sus órdenes
    con información detallada de los productos y cantidades.

    Decoradores aplicados:
        - csrf_exempt: Exime de la verificación CSRF.
        - required_method('GET'): Restringe el método HTTP a GET.
        - verify_token: Verifica que el token de autenticación sea válido.

    :param request: Objeto de solicitud HTTP.
    :return: JsonResponse con la lista de órdenes serializadas.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    orders_serializer = OrderSerializer(orders, request=request)
    return JsonResponse(orders_serializer.serialize(), safe=False, status=200)


@login_required
@csrf_exempt
@required_method('GET')
@verify_order
@verify_user
def order_detail(request, order_pk: int):
    """
    Recupera los detalles de un pedido específico.

    Este endpoint permite a un usuario autenticado obtener la información detallada de una orden,
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
    Crea una nueva orden de pedido con items detallados.

    Este endpoint permite a un usuario autenticado generar una orden,
    siempre que exista suficiente stock para los productos solicitados.
    Calcula el precio total y actualiza el stock de los productos.
    Crea OrderItems individuales para mantener el historial de precios.

    Decoradores aplicados:
        - csrf_exempt: Exime de la verificación CSRF.
        - required_method('POST'): Restringe el método HTTP a POST.
        - load_json_body: Carga el cuerpo de la solicitud como JSON.
        - verify_token: Verifica que el token de autenticación sea válido.

    :param request: Objeto de solicitud HTTP con los datos de productos.
    :return: JsonResponse con el ID de la orden creada o un mensaje de error.
    """
    from .models import OrderItem  # Import local para evitar circular imports
    
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
            # Si hay error, eliminar la orden creada para mantener consistencia
            order.delete()
            return JsonResponse({'error': f'Product with id {product_pk} not found'}, status=404)
        
        if product.stock < quantity:
            # Si hay error, eliminar la orden creada para mantener consistencia
            order.delete()
            return JsonResponse({'error': f'Insufficient stock for {product.name}'}, status=400)
        
        # Actualizar stock
        product.stock -= quantity
        product.save()
        
        # Crear OrderItem - el unit_price se asigna automáticamente
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity
        )
        
        # Calcular total
        total_price += product.price * Decimal(quantity)
    
    order.price = total_price
    order.save()

    return JsonResponse({'id': order.pk})
    """
    Crea una nueva orden de pedido con items detallados.

    Este endpoint permite a un usuario autenticado generar una orden,
    siempre que exista suficiente stock para los productos solicitados.
    Calcula el precio total y actualiza el stock de los productos.
    Crea OrderItems individuales para mantener el historial de precios.

    Decoradores aplicados:
        - csrf_exempt: Exime de la verificación CSRF.
        - required_method('POST'): Restringe el método HTTP a POST.
        - load_json_body: Carga el cuerpo de la solicitud como JSON.
        - verify_token: Verifica que el token de autenticación sea válido.

    :param request: Objeto de solicitud HTTP con los datos de productos.
    :return: JsonResponse con el ID de la orden creada o un mensaje de error.
    """
    from .models import OrderItem  # Import local para evitar circular imports
    
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
            # Si hay error, eliminar la orden creada para mantener consistencia
            order.delete()
            return JsonResponse({'error': f'Product with id {product_pk} not found'}, status=404)
        
        if product.stock < quantity:
            # Si hay error, eliminar la orden creada para mantener consistencia
            order.delete()
            return JsonResponse({'error': f'Insufficient stock for {product.name}'}, status=400)
        
        # Actualizar stock
        product.stock -= quantity
        product.save()
        
        # Crear OrderItem con el precio actual del producto
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=product.price  # Capturar precio al momento de la compra
        )
        
        # Calcular total
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
    Procesa el pago simulado de una orden.

    Cambia el estado de la orden a 'COMPLETED' si se valida correctamente la tarjeta.
    Solo se puede pagar una orden válida, pendiente y propiedad del usuario autenticado.
    
    NOTA: Este es un pago simulado, no se procesa ningún cobro real.

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
    :return: JsonResponse con un mensaje de confirmación y datos de la orden.
    """
    # Simular procesamiento de pago (sin transacción real)
    request.order.status = Order.Status.COMPLETED
    request.order.save()
    
    serializer = OrderSerializer(request.order, request=request)
    return JsonResponse({
        'message': 'Your order has been paid and completed successfully',
        'order': serializer.serialize()
    })


@csrf_exempt
@required_method('POST')
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
        - verify_token: Verifica el token JWT del usuario.
        - verify_order: Carga la orden si existe.
        - verify_user: Verifica que el usuario sea el dueño de la orden.
        - validate_status: Verifica que la orden no esté ya cancelada o completada.

    :param request: Objeto de solicitud HTTP.
    :param order_pk: ID de la orden a cancelar.
    :return: JsonResponse con un mensaje de éxito o de error si falla.
    """
    try:
        with transaction.atomic():
            # Restaurar stock de todos los items de la orden
            for item in request.order.items.all():
                product = Product.objects.select_for_update().get(pk=item.product.pk)
                product.stock += item.quantity
                product.save()
            
            # Cambiar estado de la orden
            request.order.status = Order.Status.CANCELLED
            request.order.save()
            
            serializer = OrderSerializer(request.order, request=request)
            return JsonResponse({
                'message': f'Order {order_pk} has been cancelled successfully',
                'order': serializer.serialize()
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@required_method('GET')
@verify_token
@verify_admin
def get_earnings(request):
    """
    Obtiene las ganancias diarias del mes actual para todas las órdenes completadas.

    Esta vista calcula las ganancias totales por día desde el primer hasta el último día
    del mes actual, considerando únicamente las órdenes con estado 'COMPLETED'. Retorna
    una respuesta JSON con dos listas: fechas y valores correspondientes a las ganancias de cada día.

    Parámetros
    ----------
    request : HttpRequest
        La solicitud HTTP entrante. Debe ser de tipo GET y debe incluir un token de autenticación válido.
        Solo accesible por usuarios con permisos de administrador.

    Retorna
    -------
    JsonResponse
        Un objeto JSON con dos claves:
            - 'labels': Lista de fechas (str) en formato 'YYYY-MM-DD'.
            - 'values': Lista de ganancias (float) correspondientes a cada día del mes actual.

    Ejemplo
    -------
    {
        "labels": ["2025-05-01", "2025-05-02", ..., "2025-05-31"],
        "values": [150.0, 200.0, ..., 175.5]
    }
    """
    now = timezone.now()
    first_day_of_month = now.replace(day=1)
    last_day_of_month = (first_day_of_month + timezone.timedelta(days=31)).replace(
        day=1
    ) - timezone.timedelta(days=1)

    total_earnings = []
    labels = []

    for day in range(1, last_day_of_month.day + 1):
        date = first_day_of_month.replace(day=day)
        orders = Order.objects.filter(
            created_at__date=date, 
            status=Order.Status.COMPLETED
        )
        earnings = sum(float(order.price) for order in orders if order.price)

        total_earnings.append(earnings)
        labels.append(date.strftime('%Y-%m-%d'))

    return JsonResponse({
        'labels': labels,
        'values': total_earnings,
    })


@csrf_exempt
@required_method('GET')
@verify_token
@verify_admin
def earnings_summary(request):
    """
    Obtiene un resumen de ganancias (diario, semanal, mensual).
    
    :param request: Objeto de solicitud HTTP.
    :return: JsonResponse con el resumen de ganancias.
    """
    summary = Order.earnings_summary()
    return JsonResponse({
        'daily_earnings': float(summary['daily']),
        'weekly_earnings': float(summary['weekly']),
        'monthly_earnings': float(summary['monthly']),
    })

@csrf_exempt
@required_method('POST')
@verify_token
@verify_admin
def delete_order(request, order_pk: int):
    """
    Elimina un evento existente.

    Solo un administrador autenticado puede eliminar eventos.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.
    event_pk : int
        ID del evento a eliminar.

    Returns
    -------
    JsonResponse
        Respuesta JSON con un mensaje de éxito.
    """
    order =Order.objects.get(pk=order_pk)
    order.delete()
    return JsonResponse({'msg': 'Order has been deleted'})

@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
@verify_order
@verify_user
@validate_status  # Solo permite agregar a órdenes PENDING
def add_product_to_order(request, order_pk: int):
    """
    Agrega un producto a una orden existente.

    Este endpoint permite agregar un producto adicional a una orden pendiente,
    validando stock y actualizando el precio total de la orden.

    Decoradores aplicados:
        - csrf_exempt: Exime de la verificación CSRF.
        - required_method('POST'): Restringe el método HTTP a POST.
        - load_json_body: Carga el cuerpo de la solicitud como JSON.
        - verify_token: Verifica que el token de autenticación sea válido.
        - verify_order: Carga la orden si existe.
        - verify_user: Verifica que el usuario sea el dueño de la orden.
        - validate_status: Verifica que la orden esté en estado 'PENDING'.

    :param request: Objeto de solicitud HTTP con los datos del producto.
    :param order_pk: ID de la orden a la que agregar el producto.
    :return: JsonResponse con confirmación o mensaje de error.
    """
    from .models import OrderItem
    from decimal import Decimal
    
    product_data = request.json_body
    product_id = product_data['product_id']
    quantity = product_data['quantity']
    
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': f'Product with id {product_id} not found'}, status=404)
    
    if product.stock < quantity:
        return JsonResponse({'error': f'Insufficient stock for {product.name}'}, status=400)
    
    # Verificar si el producto ya existe en la orden
    existing_item = OrderItem.objects.filter(order=request.order, product=product).first()
    
    if existing_item:
        # Si ya existe, actualizar la cantidad
        existing_item.quantity += quantity
        existing_item.save()
    else:
        # Si no existe, crear nuevo OrderItem
        OrderItem.objects.create(
            order=request.order,
            product=product,
            quantity=quantity
        )
    
    # Actualizar stock del producto
    product.stock -= quantity
    product.save()
    
    # Recalcular precio total de la orden
    total_price = sum(item.subtotal for item in request.order.items.all())
    request.order.price = total_price
    request.order.save()
    
    return JsonResponse({
        'msg': f'Product {product.name} added to order {order_pk}',
        'new_total': float(total_price)
    })