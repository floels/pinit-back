import pytz
from datetime import datetime
from rest_framework_simplejwt.views import (
    TokenObtainPairView as SimpleJWTTokenObtainPairView,
    TokenViewBase,
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


# This view is taking inspiration from:
# https://github.com/jazzband/djangorestframework-simplejwt/blob/master/rest_framework_simplejwt/views.py#L63-L69
class TokenRefreshView(TokenViewBase):
    _serializer_class = (
        "pinit_api.serializers.token_serializers.CustomTokenRefreshSerializer"
    )

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

        access_token = serializer.validated_data["access_token"]

        access_token_exp = serializer.validated_data["access_token_exp"]

        access_token_expiration_utc = datetime.fromtimestamp(
            access_token_exp, tz=pytz.UTC
        )

        return Response(
            {
                "access_token": access_token,
                "access_token_expiration_utc": access_token_expiration_utc.isoformat(),
            }
        )
