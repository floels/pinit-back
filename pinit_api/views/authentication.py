from rest_framework import generics
from ..serializers.authentication_serializers import UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView as SimpleJWTTokenObtainPairView,
    TokenRefreshView as SimpleJWTTokenRefreshView,
)
from rest_framework_simplejwt.exceptions import InvalidToken
from ..models import User
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from ..constants import (
    ERROR_CODE_INVALID_EMAIL,
    ERROR_CODE_INVALID_PASSWORD,
    ERROR_CODE_INVALID_REFRESH_TOKEN,
)
from ..doc.authentication_doc import SWAGGER_SCHEMAS


class TokenObtainPairView(SimpleJWTTokenObtainPairView):
    @swagger_auto_schema(**SWAGGER_SCHEMAS["TokenObtainPairView"])
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse(
                {"errors": [{"code": ERROR_CODE_INVALID_EMAIL}]}, status=401
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
    def handle_exception(self, exception):
        if isinstance(exception, InvalidToken):
            return JsonResponse(
                {"errors": [{"code": ERROR_CODE_INVALID_REFRESH_TOKEN}]}, status=400
            )

        return super().handle_exception(exception)

    @swagger_auto_schema(**SWAGGER_SCHEMAS["TokenRefreshView"])
    def post(self, request):
        return super().post(request)
