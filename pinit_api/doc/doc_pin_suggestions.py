from drf_yasg import openapi

SWAGGER_SCHEMAS = {
    "GET /pin-suggestions/": {
        "operation_summary": "Get all pins",
        "operation_description": "**Requires authentication.** Returns all pins in database, sorted by decreasing creation date, along with information on the author account.",
        "tags": ["Pins"],
        "security": [{"Bearer": []}],
    }
}
