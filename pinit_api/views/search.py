import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from ..doc.doc_search import SWAGGER_SCHEMAS


GOOGLE_AUTOCOMPLETE_URL = (
    "http://suggestqueries.google.com/complete/search?client=firefox&q={}"
)
ERROR_CODE_MISSING_SEARCH_PARAMETER = "missing_search_parameter"
NUMBER_SUGGESTIONS_RETURNED = 12


@extend_schema(**SWAGGER_SCHEMAS["search/autocomplete/"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def autcomplete_search(request):
    search_term = request.GET.get("search", None)

    if not search_term:
        return Response(
            {"errors": [{"code": ERROR_CODE_MISSING_SEARCH_PARAMETER}]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    encoded_search_term = requests.utils.quote(search_term)

    response_google = requests.get(GOOGLE_AUTOCOMPLETE_URL.format(encoded_search_term))

    response_google_data = response_google.json()

    # If `encoded_search_term` is "food" for instance, the response from the Google endpoint will be:
    # [
    #    "food",
    #    ["food near me","food fontainebleau","food avon",...], <- what we want
    #    [],
    #    {"google:suggestsubtypes":[...]}
    # ]
    results = (
        response_google_data[1][:NUMBER_SUGGESTIONS_RETURNED]
        if response_google_data
        else []
    )

    response_data = {"results": results}

    return Response(response_data)
