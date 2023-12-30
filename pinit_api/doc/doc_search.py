from drf_spectacular.utils import inline_serializer, OpenApiParameter
from rest_framework import serializers
from pinit_api.serializers import PinWithAuthorReadSerializer


SWAGGER_SCHEMAS = {
    "search/autocomplete/": {
        "operation_id": "search/autocomplete/",
        "description": "Takes a search term and returns a list of search autocomplete suggestions for this term.",
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
        "auth": [None],
        "parameters": [
            OpenApiParameter(
                name="q",
                description="Search term",
                required=True,
            )
        ],
        "responses": {
            200: inline_serializer(
                name="SearchSuccessResponse",
                fields={"results": PinWithAuthorReadSerializer(many=True)},
            ),
        },
    },
}
