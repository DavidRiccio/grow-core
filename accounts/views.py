from django.contrib.auth import authenticate, login, logout
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
    username = request.json_body['username']
    password = request.json_body['password']
    if user := authenticate(request, username=username, password=password):
        login(request, user)
        return JsonResponse({'msg': 'Usuario logeado', 'Token': user.token.key})


def user_logout(request):
    logout(request)
    return JsonResponse({'msg': 'Sesion Cerrada'})


@csrf_exempt
@required_method('POST')
@load_json_body
def user_signup(request):
    username = request.json_body['username']
    password = request.json_body['password']
    first_name = request.json_body['first_name']
    last_name = request.json_body['last_name']
    email = request.json_body['email']

    # Crea el usuario
    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    # Establece la contraseña (esto la hashea)
    user.set_password(password)

    # Guarda el usuario en la base de datos
    user.save()

    return JsonResponse({'msg': f'se ha creado el usuario {user.username}'})
