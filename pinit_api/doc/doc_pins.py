SWAGGER_SCHEMAS = {
    "pin-suggestions/": {
        "operation_id": "pin-suggestions/",
        "tags": ["Pins"],
        "description": "Returns a list of pin suggestions for the user.",
    },
    "pins/<unique_id>/": {
        "operation_id": "pins/<unique_id>/",
        "tags": ["Pins"],
        "auth": [None],
        "description": "Returns the detailed information for pin with unique ID 'unique_id'",
    },
}
