from drf_yasg import openapi

PIN_WITH_AUTHOR_SCHEMA = openapi.Schema(
    type="object",
    properties={
        "id": openapi.Schema(type="integer"),
        "image_url": openapi.Schema(type="string"),
        "title": openapi.Schema(type="string"),
        "description": openapi.Schema(type="string"),
        "author": openapi.Schema(
            type="object",
            properties={
                "username": openapi.Schema(type="string"),
                "display_name": openapi.Schema(type="string"),
            },
        ),
    },
)

SUCCESSFUL_RESPONSE_SCHEMA = openapi.Response(
    description="Successful response",
    schema=openapi.Schema(
        type="object",
        properties={
            "count": openapi.Schema(type="integer", description="Total count of pins"),
            "next": openapi.Schema(type="string", description="URL of the next page"),
            "previous": openapi.Schema(
                type="string", description="URL of the previous page"
            ),
            "results": openapi.Schema(
                type="array",
                items=PIN_WITH_AUTHOR_SCHEMA,
                description="Array of pins data",
            ),
        },
    ),
    examples={
        "application/json": {
            "count": 100,
            "next": "http://base.url/api/pin-suggestions/?page=3",
            "previous": "http://base.url/api/pin-suggestions/?page=1",
            "results": [
                {
                    "id": 1,
                    "image_url": "http://example.com/media/images/pin1.png",
                    "title": "Pin 1",
                    "description": "This is pin 1",
                    "author": {"username": "johndoe", "display_name": "John Doe"},
                },
            ],
        }
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
    "GET /pin-suggestions/": {
        "operation_summary": "Get pin suggestions",
        "operation_description": "**Requires authentication.** Returns pin suggestions for the user (current implementation: returns all pins in database, sorted by decreasing creation date).",
        "tags": ["Pins"],
        "security": [{"Bearer": []}],
        "responses": {
            200: SUCCESSFUL_RESPONSE_SCHEMA,
            401: UNAUTHORIZED_RESPONSE_SCHEMA,
        },
        "parameters": [
            # Known issue: this won't be displayed properly in the Redoc documentation
            openapi.Parameter(
                name="page",
                in_="query",
                description="Page number",
                type="integer",
                required=False,
            )
        ],
    }
}
