from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from drf_spectacular.utils import extend_schema
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from ..doc.doc_search import SWAGGER_SCHEMAS
from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer


ERROR_CODE_MISSING_SEARCH_PARAMETER = "missing_search_parameter"
NUMBER_SUGGESTIONS_RETURNED = 12

# This query will return an intermediary table containing a single column (`word`)
# and one row per word found in all pins' title and description,
# by leveraging the regexp_split_to_table PostgreSQL function.
# We split the text by: space, period, comma, hyphen, colon, slash and question mark.
SQL_QUERY_SELECT_ALL_WORDS_PINS_TITLE_DESCRIPTION = """
SELECT regexp_split_to_table(lower(title), '[\\s.,-:/?]+') AS word
FROM pinit_api_pin
UNION ALL
SELECT regexp_split_to_table(lower(description), '[\\s.,-:/?]+') AS word
FROM pinit_api_pin
"""

# This query will select the N words which appear most frequently in the
# intermediary table above and which are 'LIKE' the pattern provided as parameter (`%s`).
# This pattern will be `{prefix}%`, where `prefix` is the term we want to auto-complete,
# and `%` is the usual SQL wildcard for `LIKE` statements.
SQL_QUERY_GET_AUTOCOMPLETE_SUGGESTIONS = f"""
SELECT word
FROM (
{SQL_QUERY_SELECT_ALL_WORDS_PINS_TITLE_DESCRIPTION}
) t
WHERE word LIKE %s
GROUP BY word
ORDER BY COUNT(*) DESC, word
LIMIT {NUMBER_SUGGESTIONS_RETURNED};
"""


@extend_schema(**SWAGGER_SCHEMAS["search/autocomplete/"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def autocomplete_search(request):
    search_term = request.GET.get("search", None)

    if not search_term:
        return Response(
            {"errors": [{"code": ERROR_CODE_MISSING_SEARCH_PARAMETER}]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    sanitized_search_term = "".join(char for char in search_term if char.isalnum())

    with connection.cursor() as cursor:
        cursor.execute(
            SQL_QUERY_GET_AUTOCOMPLETE_SUGGESTIONS, [f"{sanitized_search_term}%"]
        )

        # cursor.fetchall() returns a list of lists, so we need to flatten it:
        suggestions = [item[0] for item in cursor.fetchall()]

    response_data = {"results": suggestions}

    return Response(response_data)


@extend_schema(**SWAGGER_SCHEMAS["search/"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_pins(request):
    search_term = request.GET.get("q", None)

    if not search_term:
        return Response(
            {"errors": [{"code": ERROR_CODE_MISSING_SEARCH_PARAMETER}]},
            status=status.HTTP_400_BAD_REQUEST,
        )

    shortened_search_term = search_term[:140]

    search_vector = SearchVector("title", weight="A") + SearchVector(
        "description", weight="B"
    )
    search_query = SearchQuery(shortened_search_term)

    all_pins_annotated = Pin.objects.annotate(
        search=search_vector, rank=SearchRank(search_vector, search_query)
    )

    matched_pins = all_pins_annotated.filter(search=search_query)

    search_results = matched_pins.order_by("-rank", "-created_at")

    paginator = PageNumberPagination()
    paginated_results = paginator.paginate_queryset(search_results, request)

    serializer = PinWithAuthorReadSerializer(paginated_results, many=True)

    return paginator.get_paginated_response(serializer.data)
