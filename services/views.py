# Create your views here.
from django.http import JsonResponse

from .models import Service
from .serializers import ServiceSerializer


def service_list(request):
    services = Service.objects.all()
    serializer = ServiceSerializer(services, request=request)
    return serializer.json_response()


def service_detail(request, service_id):
    try:
        service = Service.objects.get(id=service_id)
        serializer = ServiceSerializer(service, request=request)
        return serializer.json_response()
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)
