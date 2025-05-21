from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import required_method, verify_admin, verify_token

from .models import Profile
from .serializers import ProfileSerializer


@login_required
@csrf_exempt
@required_method('GET')
def get_user_profile(request):
    """
    Devuelve el perfil del usuario autenticado.

    Este endpoint permite a un usuario autenticado obtener su perfil.
    Si el perfil no se encuentra, se devuelve un error 404.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    JsonResponse
        Respuesta JSON con los detalles del perfil del usuario o un error si no se encuentra.
    """
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=404)

    serializer = ProfileSerializer(profile, request=request)
    return serializer.json_response()


@csrf_exempt
@required_method('GET')
@verify_token
@verify_admin
def users_per_mounth(request):
    now = timezone.now()
    first_day_of_month = now.replace(day=1)
    last_day_of_month = (first_day_of_month + timezone.timedelta(days=31)).replace(
        day=1
    ) - timezone.timedelta(days=1)
    user_counts = []
    labels = []
    for day in range(1, last_day_of_month.day + 1):
        date = first_day_of_month.replace(day=day)
        count = Profile.objects.filter(created_at__date=date).count()
        user_counts.append(count)
        labels.append(date.strftime('%Y-%m-%d'))
    return JsonResponse(
        {
            'labels': labels,
            'values': user_counts,
        }
    )


@csrf_exempt
@required_method('GET')
@verify_token
def get_barbers(request):
    """
    Devuelve una lista de barberos.

    Este endpoint permite a un usuario autenticado obtener una lista de
    todos los barberos registrados en el sistema.

    Parameters
    ----------
    request : HttpRequest
        Objeto de solicitud HTTP.

    Returns
    -------
    JsonResponse
        Respuesta JSON con la lista de barberos.
    """
    barbers = Profile.objects.filter(role=Profile.Role.WORKER)
    serializer = ProfileSerializer(barbers, request=request)
    return serializer.json_response()
