from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, views

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer
from ..doc.doc_pins import SWAGGER_SCHEMAS


class GetPinDetailsView(generics.RetrieveAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinWithAuthorReadSerializer
    lookup_field = "unique_id"

    @extend_schema(**SWAGGER_SCHEMAS["pins/<unique_id>/"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SavePinView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, unique_id, *args, **kwargs):
        try:
            pin = Pin.objects.get(unique_id=unique_id)
        except Pin.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        account = request.user.account

        pin_already_saved = pin in account.saved_pins.all()

        if pin_already_saved:
            return Response(status=status.HTTP_200_OK)

        account.saved_pins.add(pin)

        return Response(status=status.HTTP_201_CREATED)
