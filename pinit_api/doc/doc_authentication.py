from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


OBTAIN_TOKEN_SCHEMA = {
    "operation_id": "token/obtain/",
    "tags": ["Sign-up and authentication"],
    "responses": {
        200: inline_serializer(
            name="TokenObtainSuccessResponse",
            fields={
                "access_token": serializers.CharField(help_text="Access token"),
                "refresh_token": serializers.CharField(help_text="Refresh token"),
                "access_token_expiration_utc": serializers.CharField(
                    help_text="Access token expiration date (ISO 8601 format, UTC)"
                ),
            },
        ),
        401: inline_serializer(
            name="TokenObtainUnauthorizedResponse",
            fields={
                "errors": serializers.ListField(
                    child=inline_serializer(
                        name="TokenObtainUnauthorizedResponseErrors",
                        fields={
                            "code": serializers.ChoiceField(
                                choices=[
                                    ("invalid_email", "Invalid email"),
                                    ("invalid_password", "Invalid password"),
                                ],
                                help_text="Error code",
                            )
                        },
                    ),
                    help_text="List of errors",
                )
            },
        ),
    },
}

REFRESH_TOKEN_SCHEMA = {
    "operation_id": "token/refresh/",
    "tags": ["Sign-up and authentication"],
    "request": inline_serializer(
        name="TokenRefreshRequest",
        fields={"refresh_token": serializers.CharField(help_text="Refresh token")},
    ),
    "responses": {
        200: inline_serializer(
            name="TokenRefreshSuccessResponse",
            fields={
                "access_token": serializers.CharField(
                    help_text="Refreshed access token"
                ),
                "access_token_expiration_utc": serializers.CharField(
                    help_text="Refreshed access token expiration date (ISO 8601 format, UTC)"
                ),
            },
        ),
        401: inline_serializer(
            name="TokenRefreshUnauthorizedResponse",
            fields={
                "errors": serializers.ListField(
                    child=inline_serializer(
                        name="TokenRefreshUnauthorizedResponseErrors",
                        fields={
                            "code": serializers.ChoiceField(
                                choices=[
                                    ("invalid_refresh_token", "Invalid refresh token"),
                                ],
                                help_text="Error code",
                            )
                        },
                    ),
                    help_text="List of errors",
                )
            },
        ),
    },
}


SWAGGER_SCHEMAS = {
    "token/obtain/": OBTAIN_TOKEN_SCHEMA,
    "token/refresh/": REFRESH_TOKEN_SCHEMA,
}
