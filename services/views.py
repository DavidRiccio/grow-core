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


@login_required
@csrf_exempt
@required_method('GET')
def service_list(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, request=request)
    return serializer.json_response()


@login_required
@csrf_exempt
@required_method('GET')
@verify_service
def service_detail(request, service_pk):
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
    service = request.service
    service.delete()
    return JsonResponse({'msg': 'Service has been deleted'})
