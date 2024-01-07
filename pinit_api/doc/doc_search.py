from drf_spectacular.utils import inline_serializer, OpenApiParameter
from pinit_api.serializers import PinWithAuthorReadSerializer


SWAGGER_SCHEMAS = {
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
