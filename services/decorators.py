from django.http import JsonResponse

from .models import Service


def verify_service(func):
    """
    Verifica que el servicio especificado exista.

    Este decorador intenta obtener un servicio de la base de datos utilizando
    el ID proporcionado en los argumentos de la función. Si el servicio existe,
    se asigna al objeto de solicitud. Si no se encuentra el servicio, se devuelve
    un error 404.

    Parameters
    ----------
    func : callable
        La función a la que se aplica el decorador.

    Returns
    -------
    callable
        Función envuelta que verifica la existencia del servicio.
    """

    def wrapper(request, *args, **kwargs):
        try:
            service = Service.objects.get(id=kwargs['service_pk'])
            request.service = service
            return func(request, *args, **kwargs)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Servicio no encontrado'}, status=404)

    return wrapper
