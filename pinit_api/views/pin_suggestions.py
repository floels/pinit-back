from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from drf_spectacular.utils import extend_schema

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer
from ..doc.doc_pins import SWAGGER_SCHEMAS


@extend_schema(**SWAGGER_SCHEMAS["pin-suggestions/"])
class GetPinSuggestionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pin.objects.all().order_by("-created_at")
    serializer_class = PinWithAuthorReadSerializer