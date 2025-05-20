from django.http import JsonResponse

from .models import Service


def verify_service(func):
    def wrapper(request, *args, **kwargs):
        try:
            service = Service.objects.get(id=kwargs['service_pk'])
            request.service = service
        except Service.DoesNotExists:
            return JsonResponse({'error', 'Service not found'}, status=404)
