from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import required_method

from .models import Profile
from .serializers import ProfileSerializer


@login_required
@csrf_exempt
@required_method('GET')
def get_user_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)
    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()


@login_required
@csrf_exempt
@required_method('GET')
def get_barbers(request):
    barbers = Profile.objects.filter(role=Profile.Role.WORKER)
    serializer = ProfileSerializer(barbers, request=request)
    return serializer.json_response()
