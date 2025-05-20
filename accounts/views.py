from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import (
    load_json_body,
    required_method,
)


@csrf_exempt
@required_method('POST')
@load_json_body
def user_login(request):
    """
    Inicia sesión de un usuario.

    Este endpoint permite a un usuario autenticarse proporcionando su nombre de usuario
    y contraseña. Si las credenciales son correctas, se inicia la sesión y se devuelve
    un token de autenticación.

    :param request: Objeto de solicitud HTTP que contiene las credenciales del usuario.
    :return: JsonResponse con un mensaje de éxito y el token de autenticación.
    """
    username = request.json_body['username']
    password = request.json_body['password']
    if user := authenticate(request, username=username, password=password):
        login(request, user)
        return JsonResponse({'msg': 'Usuario logeado', 'token': user.token.key})


@login_required
def user_logout(request):
    """
    Cierra la sesión de un usuario.

    Este endpoint permite a un usuario autenticado cerrar su sesión.
    Se elimina la sesión activa y se devuelve un mensaje de éxito.

    :param request: Objeto de solicitud HTTP.
    :return: JsonResponse con un mensaje de éxito.
    """
    logout(request)
    return JsonResponse({'msg': 'Sesion Cerrada'})


@csrf_exempt
@required_method('POST')
@load_json_body
def user_signup(request):
    """
    Registra un nuevo usuario.

    Este endpoint permite crear un nuevo usuario proporcionando su nombre de usuario,
    contraseña, nombre, apellido y correo electrónico. El usuario se guarda en la base de datos.

    :param request: Objeto de solicitud HTTP que contiene los datos del nuevo usuario.
    :return: JsonResponse con un mensaje de éxito indicando que el usuario ha sido creado.
    """
    username = request.json_body['username']
    password = request.json_body['password']
    first_name = request.json_body['first_name']
    last_name = request.json_body['last_name']
    email = request.json_body['email']

    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    user.set_password(password)

    user.save()

    return JsonResponse({'msg': f'se ha creado el usuario {user.username}'})
