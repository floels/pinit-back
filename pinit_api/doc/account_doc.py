from drf_yasg import openapi

SWAGGER_SCHEMAS = {
    "UserDetailsView": {
        "operation_summary": "Get a user's details",
        "operation_description": "**Requires authentication.** Returns the user's details: email, initial etc.",
        "tags": ["Account"],
        "method": "get",
        "security": [{"Bearer": []}],
        "responses": {
            200: openapi.Response(
                description="Successful request",
                schema=openapi.Schema(
                    type="object",
                    properties={
                        "email": openapi.Schema(
                            type="string",
                            format="email",
                            description="User's email address",
                        ),
                        "initial": openapi.Schema(
                            type="string", description="User's initial"
                        ),
                        "first_name": openapi.Schema(
                            type="string", description="User's first name"
                        ),
                        "last_name": openapi.Schema(
                            type="string", description="User's last name"
                        ),
                    },
                ),
                examples={
                    "application/json": {
                        "email": "john.doe@example.com",
                        "initial": "J",
                        "first_name": "John",
                        "last_name": "Doe",
                    }
                },
            ),
            401: openapi.Response(
                description="Failed authentication",
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
                                            "unauthorized",
                                        ],
                                    )
                                },
                            ),
                        )
                    },
                ),
                examples={"application/json": {"errors": [{"code": "unauthorized"}]}},
            ),
        },
    }
}
