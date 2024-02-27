from drf_spectacular.utils import inline_serializer, OpenApiExample

from ..serializers import AccountSimpleReadSerializer


SWAGGER_SCHEMAS = {
    "accounts/me/": {
        "operation_id": "accounts/me/",
        "description": "Returns the public details for the account owned by the authenticated user.",
        "tags": ["Accounts"],
        "responses": {
            200: inline_serializer(
                name="AccountsSuccessResponse",
                fields={"results": AccountSimpleReadSerializer(many=True)},
            ),
        },
        "examples": [
            OpenApiExample(
                "Successful Response",
                value={
                    "type": "personal",
                    "username": "johndoe",
                    "type": "personal",
                    "display_name": "John Doe",
                    "initial": "J",
                },
                response_only=True,
                media_type="application/json",
            )
        ],
    },
    "accounts/<username>/": {
        "operation_id": "accounts/<username>/",
        "tags": ["Accounts"],
        "auth": [None],
        "description": "Returns the public details for account with username 'username'.",
    },
}
