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

from .decorators import verify_service
from .models import Service
from .serializers import ServiceSerializer


@csrf_exempt
@required_method('GET')
def service_list(request):
    """
    Devuelve una lista de todos los servicios en formato JSON.

    Este endpoint permite obtener todos los servicios registrados en la base de datos.
    Los servicios se serializan y se devuelven en una respuesta JSON.

    :param request: Objeto de solicitud HTTP.
    :return: JsonResponse con la lista de servicios.
    """
    services = Service.objects.all()
    serializer = ServiceSerializer(services, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
@verify_service
def service_detail(request, service_pk):
    """
    Devuelve los detalles de un servicio específico.

    Este endpoint permite obtener los detalles de un servicio utilizando su ID.
    Solo se puede acceder a este endpoint si el servicio existe.

    :param request: Objeto de solicitud HTTP.
    :param service_pk: ID del servicio.
    :return: JsonResponse con los detalles del servicio.
    """
    serializer = ServiceSerializer(request.service, request=request)
    return serializer.json_response()


@login_required
@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'price', 'duration', model=Service)
@verify_token
@verify_admin
def add_service(request):
    """
    Agrega un nuevo servicio.

    Este endpoint permite a un administrador autenticado crear un nuevo servicio
    proporcionando el nombre, descripción, precio y duración del servicio.

    :param request: Objeto de solicitud HTTP que contiene los datos del nuevo servicio.
    :return: JsonResponse con el ID del nuevo servicio creado.
    """
    name = request.json_body['name']
    description = request.json_body['description']
    price = request.json_body['price']
    duration = request.json_body['duration']
    duration = Service.convert_duration_string(duration)

    service = Service.objects.create(
        name=name, description=description, price=price, duration=duration
    )
    return JsonResponse({'id': service.pk})


@login_required
@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'price', 'duration', model=Service)
@verify_token
@verify_admin
@verify_service
def edit_service(request, service_pk: int):
    """
    Edita un servicio existente.

    Este endpoint permite a un administrador autenticado editar un servicio
    existente proporcionando los nuevos datos del servicio.

    :param request: Objeto de solicitud HTTP que contiene los datos del servicio.
    :param service_pk: ID del servicio a editar.
    :return: JsonResponse con un mensaje de éxito.
    """
    service = request.service
    service.name = request.json_body['name']
    service.description = request.json_body['description']
    service.price = request.json_body['price']
    duration = request.json_body['duration']
    service.duration = Service.convert_duration_string(duration)
    service.save()
    return JsonResponse({'msg': 'Service has been edited'})


@csrf_exempt
@required_method('POST')
@verify_token
@verify_admin
@verify_service
def delete_service(request, service_pk: int):
    """
    Elimina un servicio existente.

    Este endpoint permite a un administrador autenticado eliminar un servicio
    específico utilizando su ID.

    :param request: Objeto de solicitud HTTP.
    :param service_pk: ID del servicio a eliminar.
    :return: JsonResponse con un mensaje de éxito.
    """
    service = request.service
    service.delete()
    return JsonResponse({'msg': 'Service has been deleted'})
