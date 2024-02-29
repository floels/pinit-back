from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, views

from ..models import Pin
from ..serializers import PinWithAuthorReadSerializer, PinBasicReadSerializer
from ..utils.constants import ERROR_CODE_NOT_FOUND


class GetPinDetailsView(generics.RetrieveAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinWithAuthorReadSerializer
    lookup_field = "unique_id"


class SavePinView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, unique_id, *args, **kwargs):
        try:
            pin = Pin.objects.get(unique_id=unique_id)
        except Pin.DoesNotExist:
            return Response(
                {"errors": [{"code": ERROR_CODE_NOT_FOUND}]},
                status=status.HTTP_404_NOT_FOUND,
            )

        pin_serializer = PinBasicReadSerializer(pin)
        account = request.user.account

        response_body = {
            "pin": pin_serializer.data,
            "account": account.username,
        }

        pin_already_saved = pin in account.saved_pins.all()

        if pin_already_saved:
            return Response(
                response_body,
                status=status.HTTP_200_OK,
            )

        account.saved_pins.add(pin)

        return Response(
            response_body,
            status=status.HTTP_201_CREATED,
        )
