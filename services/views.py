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

from .models import Service
from .serializers import ServiceSerializer


def service_list(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, request=request)
    return serializer.json_response()


def service_detail(request, service_pk):
    try:
        service = Service.objects.get(id=service_pk)
        serializer = ServiceSerializer(service, request=request)
        return serializer.json_response()
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)


@csrf_exempt
@required_method('POST')
@load_json_body
@required_fields('name', 'description', 'price', 'duration', model=Service)
@verify_token
@verify_admin
def add_service(request):
    name = request.json_body['name']
    description = request.json_body['description']
    price = request.json_body['price']
    duration = request.json_body['duration']
    duration = Service.convert_duration_string(duration)

    service = Service.objects.create(
        name=name, description=description, price=price, duration=duration
    )
    return JsonResponse({'id': service.pk})


@csrf_exempt
@required_method('POST')
@load_json_body
@verify_token
@verify_admin
def edit_service(request, service_pk: int):
    service = Service.objects.get(pk=service_pk)
    if request.json_body['name']:
        service.name = request.json_body['name']
    if request.json_body['description']:
        service.description = request.json_body['description']
    if request.json_body['price']:
        service.price = request.json_body['price']
    if request.json_body['duration']:
        duration = request.json_body['duration']
        service.duration = Service.convert_duration_string(duration)
    service.save()
    return JsonResponse({'msg': 'Service has been edited'})


@csrf_exempt
@required_method('POST')
@verify_token
@verify_admin
def delete_service(request, service_pk: int):
    service = Service.objects.get(pk=service_pk)
    service.delete()
    return JsonResponse({'msg': 'Service has been deleted'})
