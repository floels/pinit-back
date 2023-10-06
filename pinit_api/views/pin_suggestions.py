from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer


class GetPinSuggestionsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pin.objects.all().order_by("-created_at")
    serializer_class = PinWithAuthorReadSerializer

    @extend_schema(
        operation_id="pin-suggestions/",
        tags=["Pins"],
        description="Returns a list of pin suggestions for the user.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
