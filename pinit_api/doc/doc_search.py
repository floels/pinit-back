from drf_yasg import openapi

SUCCESSFUL_RESPONSE_SCHEMA = openapi.Response(
    description="Successful request",
    schema=openapi.Schema(
        type="object",
        properties={
            "results": openapi.Schema(
                type="array",
                items=openapi.Schema(
                    type="string",
                    description="Autocomplete suggestion",
                ),
            )
        },
    ),
    examples={
        "application/json": {
            "results": [
                "autocomplete suggestion 1",
                "autocomplete suggestion 2",
                "autocomplete suggestion 3",
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
    "GET /search/autocomplete/": {
        "operation_summary": "Get search autocomplete suggestions",
        "operation_description": "**Requires authentication.** Returns a list of search autocomplete suggestions for the search term provided as parameter.",
        "tags": ["Search"],
        "method": "get",
        "security": [{"Bearer": []}],
        "responses": {
            200: SUCCESSFUL_RESPONSE_SCHEMA,
            401: UNAUTHORIZED_RESPONSE_SCHEMA,
        },
        "parameters": [
            openapi.Parameter(
                name="search",
                in_="query",
                description="Search term to autocomplete",
                type="string",
            )
        ],
    }
}
