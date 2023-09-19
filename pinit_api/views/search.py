from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from ..doc.doc_search import SWAGGER_SCHEMAS


@swagger_auto_schema(**SWAGGER_SCHEMAS["GET /search/autocomplete/"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def autcomplete_search(request):
    response_data = {"results": []}

    return Response(response_data)
