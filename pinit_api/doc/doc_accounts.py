from drf_spectacular.utils import inline_serializer, OpenApiExample

from ..serializers import AccountWithOwnerEmailReadSerializer


SWAGGER_SCHEMAS = {
    "owned-accounts/": {
        "operation_id": "owned-accounts/",
        "description": "Returns all accounts owned by the user.",
        "tags": ["Accounts"],
        "responses": {
            200: inline_serializer(
                name="AccountsSuccessResponse",
                fields={"results": AccountWithOwnerEmailReadSerializer(many=True)},
            ),
        },
        "examples": [
            OpenApiExample(
                "Successful Response",
                value={
                    "results": [
                        {
                            "type": "accounts",
                            "username": "johndoe",
                            "type": "personal",
                            "display_name": "John Doe",
                            "initial": "J",
                            "owner_email": "john.doe@example.com",
                        }
                    ]
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
        "description": "Returns the public details for account with username \<username\>.",
    },
}
