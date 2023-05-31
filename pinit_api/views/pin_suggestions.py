from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer
from ..doc.doc_pin_suggestions import SWAGGER_SCHEMAS


@swagger_auto_schema(**SWAGGER_SCHEMAS["GET /pin-suggestions/"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_pin_suggestions(request):
    all_pins = Pin.objects.all().order_by("-created_at")

    return Response()
