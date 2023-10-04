from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer


PAGE_SIZE = 50


class Pagination(PageNumberPagination):
    page_size = PAGE_SIZE


class GetPinSuggestionsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Pin.objects.all().order_by("-created_at")
    serializer_class = PinWithAuthorReadSerializer
    pagination_class = Pagination

    @extend_schema(
        operation_id="pin-suggestions/",
        tags=["Pins"],
        description="Returns a list of pin suggestions for the user.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
