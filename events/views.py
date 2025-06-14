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

from .decorators import verify_event
from .models import Event
from .serializers import EventSerializer


@csrf_exempt
@required_method('GET')
def event_list(request):
    """
    Devuelve una lista de todos los eventos en formato JSON.

    Este endpoint permite obtener todos los eventos registrados en la base de datos.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    JsonResponse
        Respuesta JSON con la lista de eventos serializados.
    """
    events = Event.objects.all()
    serializer = EventSerializer(events, request=request)
    return serializer.json_response()


@required_method('GET')
@verify_event
def event_detail(request, event_pk):
    """
    Devuelve los detalles de un evento específico.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.
    event_pk : int
        ID del evento a consultar.

    Returns
    -------
    JsonResponse
        Respuesta JSON con los detalles del evento.
    """
    event = request.event
    serializer = EventSerializer(event, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'date', 'time', 'location', model=Event)
@verify_token
@verify_admin
def add_event(request):
    """
    Agrega un nuevo evento.

    Solo un administrador autenticado puede crear eventos nuevos.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP que contiene los datos del evento.

    Returns
    -------
    JsonResponse
        Respuesta JSON con el ID del evento creado.
    """
    name = request.json_body['name']
    description = request.json_body['description']
    date = request.json_body['date']
    time = request.json_body['time']
    location = request.json_body['location']
    image_base64 = request.json_body.get('image')

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

    event = Event.objects.create(
        name=name,
        description=description,
        location=location,
        date=date,
        image=image_file,
        time=time,
    )

    return JsonResponse({'id': event.pk, 'msg': 'Servicio creado exitosamente'})


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'date', 'time', 'location', model=Event)
@verify_token
@verify_admin
@verify_event
def edit_event(request, event_pk: int):
    """
    Edita un evento existente.

    Un administrador autenticado puede modificar los datos de un evento.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP con los datos del evento.
    event_pk : int
        ID del evento a editar.

    Returns
    -------
    JsonResponse
        Respuesta JSON con un mensaje de confirmación.
    """
    event = request.event
    event.name = request.json_body['name']
    event.description = request.json_body['description']
    event.date = request.json_body['date']
    event.location = request.json_body['location']
    event.time = request.json_body['time']
    image_base64 = request.json_body.get('image')
    if image_base64:
        try:
            format_part, data_part = image_base64.split(',')
            file_format = format_part.split('/')[1].split(';')[0]

            image_data = base64.b64decode(data_part)

            filename = f'service_{uuid.uuid4().hex[:8]}.{file_format}'
            image_file = ContentFile(image_data, name=filename)
            event.image = image_file
        except Exception as e:
            return JsonResponse({'error': f'Error procesando la imagen: {str(e)}'}, status=400)

    event.save()
    return JsonResponse({'msg': 'Event has been edited'})


@csrf_exempt
@required_method('POST')
@verify_token
@verify_admin
@verify_event
def delete_event(request, event_pk: int):
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
    event = request.event
    event.delete()
    return JsonResponse({'msg': 'Event has been deleted'})
