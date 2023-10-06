from drf_spectacular.utils import inline_serializer, OpenApiParameter, OpenApiExample
from rest_framework import serializers


SWAGGER_SCHEMAS = {
    "search/autocomplete/": {
        "operation_id": "search/autocomplete/",
        "description": "Takes a search term and returns a list of search autocomplete suggestions for this term.",
        "tags": ["Search"],
        "parameters": [
            OpenApiParameter(
                name="search",
                description="Search term",
                required=True,
            )
        ],
        "responses": {
            200: inline_serializer(
                name="SearchAutocompleteSuccessfulResponse",
                fields={
                    "results": serializers.ListField(
                        child=serializers.CharField(
                            help_text="Autocomplete suggestion"
                        ),
                        help_text="List of autocomplete suggestions",
                    )
                },
            )
        },
    },
    "search/": {
        "operation_id": "search/",
        "description": "Takes a search term and returns a list of relevant pins.",
        "tags": ["Search"],
        "parameters": [
            OpenApiParameter(
                name="q",
                description="Search term",
                required=True,
            )
        ],
        "responses": {
            200: inline_serializer(
                name="SearchPinsSuccessfulResponse",
                fields={
                    "results": serializers.ListField(
                        help_text="List of relevant pins",
                    )
                },
            )
        },
        "examples": [
            OpenApiExample(
                "Successful Response",
                value={
                    "results": [
                        {
                            "id": "999999999999999999",
                            "title": "Beautiful beach",
                            "description": "How beautiful is that?",
                            "image_url": "https://s.pinimg.com/...",
                            "author": {
                                "username": "johndoe",
                                "display_name": "John Doe",
                            },
                        },
                    ]
                },
                response_only=True,
                media_type="application/json",
            )
        ],
    },
}
