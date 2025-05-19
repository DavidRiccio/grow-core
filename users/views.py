from django.contrib.auth.decorators import login_required

from .models import Profile
from .serializers import ProfileSerializer


@login_required
def get_user_profile(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()
