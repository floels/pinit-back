from rest_framework import generics
from drf_spectacular.utils import extend_schema

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer
from ..doc.doc_pins import SWAGGER_SCHEMAS


@extend_schema(**SWAGGER_SCHEMAS["pins/<unique_id>/"])
class GetPinDetailsView(generics.RetrieveAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinWithAuthorReadSerializer
    lookup_field = "unique_id"
