from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response  # TODO: delete

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer
from ..doc.doc_pins import SWAGGER_SCHEMAS


class GetPinSuggestionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pin.objects.all().order_by("-created_at")
    serializer_class = PinWithAuthorReadSerializer

    @extend_schema(**SWAGGER_SCHEMAS["pin-suggestions/"])
    def get(self, request, *args, **kwargs):
        # return Response(
        #     {
        #         "message": "This endpoint is not implemented yet.",
        #     },
        #     status=401,
        # )
        return super().get(request, *args, **kwargs)
