from rest_framework_simplejwt.views import (
    TokenObtainPairView as SimpleJWTTokenObtainPairView,
    TokenRefreshView as SimpleJWTTokenRefreshView,
)
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from ..models import User
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from ..utils.constants import (
    ERROR_CODE_INVALID_EMAIL,
    ERROR_CODE_INVALID_PASSWORD,
    ERROR_CODE_INVALID_REFRESH_TOKEN,
    ERROR_CODE_MISSING_REFRESH_TOKEN,
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
                {"errors": [{"code": ERROR_CODE_INVALID_EMAIL}]},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return JsonResponse(
                {"errors": [{"code": ERROR_CODE_INVALID_PASSWORD}]},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh_token = RefreshToken.for_user(user)

        return JsonResponse(
            {
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
            }
        )


class TokenRefreshView(SimpleJWTTokenRefreshView):
    @swagger_auto_schema(**SWAGGER_SCHEMAS["TokenRefreshView"])
    def post(self, request):
        if "refresh_token" not in request.data:
            return JsonResponse(
                {"errors": [{"code": ERROR_CODE_MISSING_REFRESH_TOKEN}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data={"refresh": request.data["refresh_token"]}
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return JsonResponse(
                {"errors": [{"code": ERROR_CODE_INVALID_REFRESH_TOKEN}]},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = serializer.validated_data["access"]

        return JsonResponse({"access_token": access_token}, status=status.HTTP_200_OK)
