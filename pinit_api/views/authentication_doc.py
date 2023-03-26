from drf_yasg import openapi

SWAGGER_SCHEMAS = {
    "TokenObtainPairView": {
        "operation_description": "Takes sign-in credentials and returns a pair of access and refresh token if credentials are valid.",
        "tags": ["Signup and authentication"],
        "request_body": openapi.Schema(
            type="object",
            properties={
                "email": openapi.Schema(type="string", format="email"),
                "password": openapi.Schema(type="string", format="password"),
            },
            required=["email", "password"],
            example={
                "email": "john.doe@example.com",
                "password": "J0hnDO€sPA$$W0RD",
            },
        ),
        "responses": {
            200: openapi.Response(
                description="Successful sign-in",
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
            401: openapi.Response(
                description="Invalid email or password",
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
                                        enum=["invalid_email", "invalid_password"],
                                    )
                                },
                            ),
                        )
                    },
                ),
                examples={"application/json": {"errors": [{"code": "invalid_email"}]}},
            ),
        },
    },
    "TokenRefreshView": {
        "operation_summary": "token_refresh",
        "tags": ["Signup and authentication"],
        "request_body": openapi.Schema(
            type="object",
            properties={
                "refresh": openapi.Schema(type="string"),
            },
            required=["refresh"],
            example={
                "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3OTA4MDYwMCwiaWF0IjoxNjc4OTk0MjAwLCJqdGkiOiJlYTcyNTFjNzRmODU0YWFhYmFkNTI5MDBmMTBhOTQ2YiIsInVzZXJfaWQiOjF9.UgC1da2o4bt_K3tqEIQrRwkRx6au1TCK8ftosYJB_cw",
            },
        ),
        "responses": {
            200: openapi.Response(
                description="Successful refresh",
                schema=openapi.Schema(
                    type="object",
                    properties={
                        "access": openapi.Schema(
                            type="string", description="Access token", min_length=1
                        ),
                    },
                ),
                examples={
                    "application/json": {
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4OTk0NTAwLCJpYXQiOjE2Nzg5OT",
                    }
                },
            ),
            401: openapi.Response(description="Invalid refresh token"),
        },
    },
    "SignupView": {
        "operation_description": "Takes sign-up data and returns a pair of access and refresh token if sign-up was successful.",
        "tags": ["Signup and authentication"],
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
            401: openapi.Response(
                description="Invalid username or password",
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
                                        enum=["invalid_username", "invalid_password"],
                                    )
                                },
                            ),
                        )
                    },
                ),
                examples={
                    "application/json": {"errors": [{"code": "invalid_username"}]}
                },
            ),
        },
    },
}
