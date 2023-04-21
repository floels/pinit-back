from drf_yasg import openapi

SWAGGER_SCHEMAS = {
    "SignupView": {
        "operation_summary": "Sign up",
        "operation_description": "Takes sign-up data and returns a pair of access and refresh token if sign-up was successful.",
        "tags": ["Sign-up and authentication"],
        "request_body": openapi.Schema(
            type="object",
            properties={
                "email": openapi.Schema(type="string", format="email"),
                "password": openapi.Schema(type="string", format="password"),
                "birthdate": openapi.Schema(type="string", format="date"),
            },
            required=["email", "password", "birthdate"],
            example={
                "email": "john.doe@example.com",
                "password": "J0hnDO€sPA$$W0RD",
                "birthdate": "1970-01-01",
            },
        ),
        "responses": {
            200: openapi.Response(
                description="Successful signup",
                schema=openapi.Schema(
                    type="object",
                    properties={
                        "access": openapi.Schema(
                            type="string", description="Access token", min_length=1
                        ),
                        "refresh": openapi.Schema(
                            type="string", description="Refresh token", min_length=1
                        ),
                    },
                ),
                examples={
                    "application/json": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4OTk0NTAwLCJpYXQiOjE2Nzg5OT",
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3OTA4MDYwMCwiaWF0IjoxNjc4OTk0MjAwLCJqdGkiOiJlYTcyNTFjNzRmODU0YWFhYmFkNTI5MDBmMTBhOTQ2YiIsInVzZXJfaWQiOjF9.UgC1da2o4bt_K3tqEIQrRwkRx6au1TCK8ftosYJB_cw",
                    }
                },
            ),
            400: openapi.Response(
                description="Invalid signup data",
                schema=openapi.Schema(
                    type="object",
                    properties={
                        "errors": openapi.Schema(
                            type="array",
                            items=openapi.Schema(
                                type="object",
                                properties={
                                    "code": openapi.Schema(
                                        type="string",
                                        description="Error code",
                                        min_length=1,
                                        enum=[
                                            "invalid_email",
                                            "invalid_password",
                                            "invalid_birthdate",
                                            "email_already_signed_up",
                                        ],
                                    )
                                },
                            ),
                        )
                    },
                ),
                examples={
                    "application/json": {
                        "errors": [{"code": "email_already_signed_up"}]
                    }
                },
            ),
        },
    },
}
