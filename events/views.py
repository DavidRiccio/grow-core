# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import (
    load_json_body,
    required_fields,
    required_method,
    verify_admin,
    verify_token,
)

from .models import Event
from .serializers import EventSerializer


def event_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, request=request)
    return serializer.json_response()


def event_detail(request, event_pk):
    event = Event.objects.get(pk=event_pk)
    serializer = EventSerializer(event, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'date', 'time', 'location', model=Event)
@verify_token
def add_event(request):
    name = request.json_body['name']
    description = request.json_body['description']
    date = request.json_body['date']
    time = request.json_body['time']
    location = request.json_body['location']

    event = Event.objects.create(
        name=name, description=description, date=date, location=location, time=time
    )
    return JsonResponse({'id': event.pk})


@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
@verify_admin
def edit_event(request, event_pk: int):
    event = Event.objects.get(pk=event_pk)
    if request.json_body['name']:
        event.name = request.json_body['name']
    if request.json_body['description']:
        event.description = request.json_body['description']
    if request.json_body['date']:
        event.date = request.json_body['date']
    if request.json_body['location']:
        event.location = request.json_body['location']
    if request.json_body['time']:
        event.time = request.json_body['time']
    event.save()
    return JsonResponse({'msg': 'Event has been edited'})


@csrf_exempt
@required_method('POST')
@verify_token
@verify_admin
def delete_event(request, event_pk: int):
    event = Event.objects.get(pk=event_pk)
    event.delete()
    return JsonResponse({'msg': 'Event has been deleted'})
