import base64
import uuid

from django.core.files.base import ContentFile
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

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    JsonResponse
        Respuesta JSON con la lista de servicios.
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

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.
    service_pk : int
        ID del servicio.

    Returns
    -------
    JsonResponse
        Respuesta JSON con los detalles del servicio.
    """
    serializer = ServiceSerializer(request.service, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
@verify_admin
def add_service(request):
    """
    Agrega un nuevo servicio usando JSON con imágenes en base64.
    """
    try:
        name = request.json_body.get('name')
        description = request.json_body.get('description')
        price = request.json_body.get('price')
        duration = request.json_body.get('duration')
        image_base64 = request.json_body.get('image')

        if not all([name, description, price, duration]):
            return JsonResponse(
                {'error': 'Todos los campos son requeridos: name, description, price, duration'},
                status=400,
            )

        duration = Service.convert_duration_string(duration)

        image_file = None
        if image_base64:
            try:
                format_part, data_part = image_base64.split(',')
                file_format = format_part.split('/')[1].split(';')[0]

                image_data = base64.b64decode(data_part)

                filename = f'service_{uuid.uuid4().hex[:8]}.{file_format}'
                image_file = ContentFile(image_data, name=filename)

            except Exception as e:
                return JsonResponse({'error': f'Error procesando la imagen: {str(e)}'}, status=400)

        service = Service.objects.create(
            name=name, description=description, price=price, duration=duration, image=image_file
        )

        return JsonResponse({'id': service.pk, 'msg': 'Servicio creado exitosamente'})

    except Exception as e:
        return JsonResponse({'error': f'Error al crear el servicio: {str(e)}'}, status=500)


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

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP que contiene los datos del servicio.
    service_pk : int
        ID del servicio a editar.

    Returns
    -------
    JsonResponse
        Respuesta JSON con un mensaje de éxito.
    """
    service = request.service
    service.name = request.json_body['name']
    service.description = request.json_body['description']
    service.price = request.json_body['price']
    duration = request.json_body['duration']
    service.duration = Service.convert_duration_string(duration)
    image_base64 = request.json_body.get('image')
    if image_base64:
        try:
            format_part, data_part = image_base64.split(',')
            file_format = format_part.split('/')[1].split(';')[0]

            image_data = base64.b64decode(data_part)

            filename = f'service_{uuid.uuid4().hex[:8]}.{file_format}'
            image_file = ContentFile(image_data, name=filename)
            service.image = image_file
        except Exception as e:
            return JsonResponse({'error': f'Error procesando la imagen: {str(e)}'}, status=400)

    service.save()
    return JsonResponse({'msg': 'El servicio ha sido editado'})


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

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.
    service_pk : int
        ID del servicio a eliminar.

    Returns
    -------
    JsonResponse
        Respuesta JSON con un mensaje de éxito.
    """
    service = request.service
    service.delete()
    return JsonResponse({'msg': 'El servicio ha sido eliminado'})
