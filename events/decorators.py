from django.http import JsonResponse

from .models import Event


def verify_event(func):
    """
    Decorador que intenta recuperar un evento usando 'event_pk' desde los parámetros de la URL.

    Si el evento existe, se adjunta al objeto request como 'request.event'.
    Si no existe, devuelve una respuesta JSON con error 404 (No encontrado).

    Parameters
    ----------
    func : callable
        Vista a decorar.

    Returns
    -------
    callable
        Vista decorada que incluye la verificación de existencia del evento.
    """

    def wrapper(request, *args, **kwargs):
        try:
            event = Event.objects.get(id=kwargs['event_pk'])
            request.event = event
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Evento no encontrado'}, status=404)

        return func(request, *args, **kwargs)

    return wrapper
