# users/views.py
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer


def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, request=request)
    return serializer.json_response()


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    serializer = UserSerializer(user, request=request)
    return serializer.json_response()
