from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .constants import ERROR_CODE_INVALID_USERNAME, ERROR_CODE_INVALID_PASSWORD



class TokenObtainView(TokenObtainPairView):
    @swagger_auto_schema(
        operation_description="Takes sign-in credentials and returns a pair of access/refresh tokens if valid.",
    )

    def post(self, request):
        data = request.POST
        username = data.get("username")
        password = data.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse(
                {"errors": [{"code": ERROR_CODE_INVALID_USERNAME}]}, status=401
            )

        if not user.check_password(password):
            return JsonResponse(
                {"errors": [{"code": ERROR_CODE_INVALID_PASSWORD}]}, status=401
            )

        refresh_token = RefreshToken.for_user(user)

        return JsonResponse(
            {
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
            }
        )
