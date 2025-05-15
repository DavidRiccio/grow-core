import re

from django.http import JsonResponse

from users.models import Token


def required_method(method_type):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != method_type:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def verify_token(func):
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
