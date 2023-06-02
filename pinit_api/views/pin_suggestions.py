from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from drf_yasg.utils import swagger_auto_schema

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer
from ..doc.doc_pin_suggestions import SWAGGER_SCHEMAS


@swagger_auto_schema(**SWAGGER_SCHEMAS["GET /pin-suggestions/"])
class GetPinSuggestionsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pin.objects.all().order_by("-created_at")
    serializer_class = PinWithAuthorReadSerializer
