from rest_framework_simplejwt.views import (
    TokenObtainPairView as SimpleJWTTokenObtainPairView,
    TokenRefreshView as SimpleJWTTokenRefreshView,
)
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from ..constants import ERROR_CODE_INVALID_USERNAME, ERROR_CODE_INVALID_PASSWORD
from .authentication_doc import SWAGGER_SCHEMAS


class TokenObtainPairView(SimpleJWTTokenObtainPairView):
    @swagger_auto_schema(**SWAGGER_SCHEMAS["TokenObtainPairView"])
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
                "access": str(refresh_token.access_token),
                "refresh": str(refresh_token),
            }
        )


class TokenRefreshView(SimpleJWTTokenRefreshView):
    @swagger_auto_schema(**SWAGGER_SCHEMAS["TokenRefreshView"])
    def post(self, request):
        return super().post(request)
