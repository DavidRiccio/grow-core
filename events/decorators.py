from django.http import JsonResponse

from .models import Event


def verify_event(func):
    def wrapper(request, *args, **kwargs):
        try:
            event = Event.objects.get(id=kwargs['event_pk'])
            request.event = event
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)

        return func(request, *args, **kwargs)

    return wrapper
