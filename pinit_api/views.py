from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.http import require_POST
from .constants import ERROR_CODE_INVALID_USERNAME, ERROR_CODE_INVALID_PASSWORD

@require_POST
def obtain_token_pair(request):
    data = request.POST
    username = data.get('username')
    password = data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'errors': [{'code': ERROR_CODE_INVALID_USERNAME}]}, status=401)

    if not user.check_password(password):
        return JsonResponse({'errors': [{'code': ERROR_CODE_INVALID_PASSWORD}]}, status=401)
    
    refresh_token = RefreshToken.for_user(user)

    return JsonResponse({'access_token': str(refresh_token.access_token), 'refresh_token': str(refresh_token)})