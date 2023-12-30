from drf_spectacular.utils import OpenApiParameter
from pinit_api.serializers.pin_serializers import PinBasicReadSerializer

SWAGGER_SCHEMAS = {
    "create-pin/": {
        "operation_id": "create-pin/",
        "tags": ["Pins"],
        "description": "Creates a new pin.",
        "parameters": [
            OpenApiParameter(
                name="X-Username",
                location=OpenApiParameter.HEADER,
                required=True,
                description="Account username",
            )
        ],
        "responses": {201: PinBasicReadSerializer},
    },
}
