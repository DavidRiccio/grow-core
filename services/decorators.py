from django.http import JsonResponse

from .models import Service


def verify_service(func):
    def wrapper(request, *args, **kwargs):
        try:
            service = Service.objects.get(id=kwargs['service_pk'])
            request.service = service
            return func(request, *args, **kwargs)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Service not found'}, status=404)

    return wrapper
