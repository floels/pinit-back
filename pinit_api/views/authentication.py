import pytz
from datetime import datetime
from rest_framework_simplejwt.views import (
    TokenObtainPairView as SimpleJWTTokenObtainPairView,
    TokenRefreshView as SimpleJWTTokenRefreshView,
)
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from ..models import User
from ..utils.constants import (
    ERROR_CODE_INVALID_EMAIL,
    ERROR_CODE_INVALID_PASSWORD,
)
from ..doc.doc_authentication import SWAGGER_SCHEMAS

ERROR_CODE_INVALID_REFRESH_TOKEN = "invalid_refresh_token"
ERROR_CODE_MISSING_REFRESH_TOKEN = "missing_refresh_token"


class TokenObtainPairView(SimpleJWTTokenObtainPairView):
    @extend_schema(**SWAGGER_SCHEMAS["token/obtain/"])
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"errors": [{"code": ERROR_CODE_INVALID_EMAIL}]},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {"errors": [{"code": ERROR_CODE_INVALID_PASSWORD}]},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh_token = RefreshToken.for_user(user)

        access_token = refresh_token.access_token

        access_token_expiration_utc = datetime.fromtimestamp(
            access_token["exp"], tz=pytz.UTC
        )

        return Response(
            {
                "access_token": str(access_token),
                "access_token_expiration_utc": access_token_expiration_utc.isoformat(),
                "refresh_token": str(refresh_token),
            }
        )


class TokenRefreshView(SimpleJWTTokenRefreshView):
    @extend_schema(**SWAGGER_SCHEMAS["token/refresh/"])
    def post(self, request):
        if "refresh_token" not in request.data:
            return Response(
                {"errors": [{"code": ERROR_CODE_MISSING_REFRESH_TOKEN}]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data={"refresh": request.data["refresh_token"]}
        )

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError:
            return Response(
                {"errors": [{"code": ERROR_CODE_INVALID_REFRESH_TOKEN}]},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = serializer.validated_data["access"]

        return Response({"access_token": access_token}, status=status.HTTP_200_OK)
