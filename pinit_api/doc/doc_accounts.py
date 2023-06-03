from drf_yasg import openapi

SUCCESSFUL_RESPONSE_SCHEMA = openapi.Response(
    description="Successful request",
    schema=openapi.Schema(
        type="object",
        properties={
            "results": openapi.Schema(
                type="array",
                items=openapi.Schema(
                    type="object",
                    properties={
                        "username": openapi.Schema(
                            type="string",
                            description="Account's username",
                        ),
                        "type": openapi.Schema(
                            type="string",
                            description="Type of account (personal / business)",
                        ),
                        "display_name": openapi.Schema(
                            type="openapi",
                            description="Account's display name",
                        ),
                        "initial": openapi.Schema(
                            type="string",
                            description="User's initial",
                        ),
                        "owner_email": openapi.Schema(
                            type="string",
                            format="email",
                            description="Account owner's email",
                        ),
                    },
                ),
            )
        },
    ),
    examples={
        "application/json": {
            "results": [
                {
                    "type": "accounts",
                    "username": "johndoe",
                    "type": "personal",
                    "display_name": "John Doe",
                    "initial": "J",
                    "owner_email": "john.doe@example.com",
                },
            ],
        },
    },
)

UNAUTHORIZED_RESPONSE_SCHEMA = openapi.Response(
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
)

SWAGGER_SCHEMAS = {
    "GET /accounts/": {
        "operation_summary": "Get all accounts owned by the user",
        "operation_description": "**Requires authentication.** Returns the list of accounts owned by the user.",
        "tags": ["Accounts"],
        "method": "get",
        "security": [{"Bearer": []}],
        "responses": {
            200: SUCCESSFUL_RESPONSE_SCHEMA,
            401: UNAUTHORIZED_RESPONSE_SCHEMA,
        },
    }
}
