from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


SWAGGER_SCHEMAS = {
    "signup/": {
        "operation_id": "signup/",
        "tags": ["Sign-up and authentication"],
        "auth": [None],
        "request": inline_serializer(
            name="SignupRequest",
            fields={
                "email": serializers.EmailField(help_text="Email"),
                "password": serializers.CharField(help_text="Password"),
                "birthdate": serializers.DateField(help_text="Birth date"),
            },
        ),
        "responses": {
            200: inline_serializer(
                name="SignupSuccessResponse",
                fields={
                    "access_token": serializers.CharField(help_text="Access token"),
                    "refresh_token": serializers.CharField(help_text="Refresh token"),
                },
            ),
            401: inline_serializer(
                name="SignupUnauthorizedResponse",
                fields={
                    "errors": serializers.ListField(
                        child=inline_serializer(
                            name="SignupUnauthorizedResponseErrors",
                            fields={
                                "code": serializers.ChoiceField(
                                    choices=[
                                        (
                                            "invalid_email",
                                            "Invalid email",
                                        ),
                                        (
                                            "invalid_password",
                                            "Invalid password",
                                        ),
                                        (
                                            "invalid_birthdate",
                                            "Invalid birth date",
                                        ),
                                        (
                                            "email_already_signed_up",
                                            "Email already signed up",
                                        ),
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
    },
}
