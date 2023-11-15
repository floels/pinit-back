from rest_framework import generics
from drf_spectacular.utils import extend_schema

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer


@extend_schema(
    operation_id="pins/<unique_id>",
    tags=["Pins"],
    description="Returns the detailed information for pin with unique ID \<unique_id\>",
)
class GetPinDetailsView(generics.RetrieveAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinWithAuthorReadSerializer
    lookup_field = "unique_id"
