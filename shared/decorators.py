import json
import re

from django.http import JsonResponse

from users.models import Token


def verify_token(func):
    """
    Verifica el token de autenticación del usuario.

    Este decorador comprueba si el token de autenticación proporcionado en
    la cabecera 'Authorization' es válido. Si el token es válido, se
    asigna el usuario correspondiente a la solicitud. Si el token no es
    válido o no está registrado, se devuelve un error.

    :param func: La función a la que se aplica el decorador.
    :return: Función envuelta que verifica el token.
    """

    def wrapper(request, *args, **kwargs):
        UUID_PATTERN = re.compile(
            r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
        )
        bearer_auth = request.headers.get('Authorization')
        if m := re.fullmatch(UUID_PATTERN, bearer_auth):
            token_reg = m['token']
            try:
                token = Token.objects.get(key=token_reg)
                request.user = token.user
            except Token.DoesNotExist:
                return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
        else:
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)
        return func(request, *args, **kwargs)

    return wrapper


def required_method(method_type):
    """
    Verifica que el método de la solicitud sea el esperado.

    Este decorador comprueba si el método HTTP de la solicitud coincide
    con el tipo de método requerido. Si no coincide, se devuelve un error
    de método no permitido.

    :param method_type: El tipo de método HTTP requerido (por ejemplo, 'GET', 'POST').
    :param func: La función a la que se aplica el decorador.
    :return: Función envuelta que verifica el método.
    """

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != method_type:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def load_json_body(func):
    """
    Carga el cuerpo de la solicitud como JSON.

    Este decorador intenta cargar el cuerpo de la solicitud como un objeto
    JSON. Si el cuerpo está vacío o no es un JSON válido, se devuelve un
    error.

    :param func: La función a la que se aplica el decorador.
    :return: Función envuelta que carga el cuerpo JSON.
    """

    def wrapper(request, *args, **kwargs):
        try:
            if not request.body:
                return JsonResponse({'error': 'Missing request body'}, status=400)

            request.json_body = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)

        return func(request, *args, **kwargs)

    return wrapper


def required_fields(*fields, model):
    """
    Verifica que los campos requeridos estén presentes en el cuerpo de la solicitud.

    Este decorador comprueba si los campos requeridos están presentes en
    el cuerpo JSON de la solicitud. Si falta algún campo, se devuelve un
    error.

    :param fields: Los nombres de los campos requeridos.
    :param model: El modelo relacionado (no se utiliza en la lógica, pero se incluye para referencia).
    :param func: La función a la que se aplica el decorador.
    :return: Función envuelta que verifica los campos requeridos.
    """

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            json_body = json.loads(request.body)
            for field in fields:
                if field not in json_body:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def verify_admin(func):
    """
    Verifica que el usuario autenticado sea un administrador.

    Este decorador comprueba si el usuario autenticado tiene el rol de
    administrador. Si no es un administrador, se devuelve un error de
    acceso denegado.

    :param func: La función a la que se aplica el decorador.
    :return: Función envuelta que verifica el rol de administrador.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.profile.role == 'A':
                return func(request, *args, **kwargs)
        return JsonResponse({'error': 'The user must be an admin'}, status=403)

    return wrapper
