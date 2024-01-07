from drf_spectacular.utils import inline_serializer, OpenApiParameter
from rest_framework import serializers


SWAGGER_SCHEMAS = {
    "search-suggestions/": {
        "operation_id": "search-suggestions/",
        "description": "Takes a search term and returns a list of autocomplete suggestions for this term.",
        "tags": ["Search"],
        "auth": [None],
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
                        child=serializers.CharField(help_text="Search suggestion"),
                        help_text="List of search suggestions",
                    )
                },
            )
        },
    },
}
