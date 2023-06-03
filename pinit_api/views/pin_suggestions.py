from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer
from ..doc.doc_pin_suggestions import SWAGGER_SCHEMAS


PAGE_SIZE = 100


class Pagination(PageNumberPagination):
    page_size = PAGE_SIZE


class GetPinSuggestionsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pin.objects.all().order_by("-created_at")
    serializer_class = PinWithAuthorReadSerializer
    pagination_class = Pagination

    @swagger_auto_schema(**SWAGGER_SCHEMAS["GET /pin-suggestions/"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
