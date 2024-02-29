from drf_spectacular.utils import OpenApiParameter
from pinit_api.serializers.pin_serializers import PinBasicReadSerializer

SWAGGER_SCHEMAS = {
    "create-pin/": {
        "operation_id": "create-pin/",
        "tags": ["Pins"],
        "description": "Creates a new pin.",
        "responses": {201: PinBasicReadSerializer},
    },
}
