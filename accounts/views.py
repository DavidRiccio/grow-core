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
    username = request.json_body['username']
    password = request.json_body['password']
    if user := authenticate(request, username=username, password=password):
        login(request, user)
        return JsonResponse({'msg': 'Usuario logeado', 'token': user.token.key})


@login_required
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

    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )

    user.set_password(password)

    user.save()

    return JsonResponse({'msg': f'se ha creado el usuario {user.username}'})
