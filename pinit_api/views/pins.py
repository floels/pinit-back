from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, views

from ..models import Pin, Board, PinInBoard
from ..serializers import PinWithAuthorReadSerializer
from ..utils.constants import (
    ERROR_CODE_PIN_NOT_FOUND,
    ERROR_CODE_BOARD_NOT_FOUND,
    ERROR_CODE_FORBIDDEN,
)


class GetPinDetailsView(generics.RetrieveAPIView):
    queryset = Pin.objects.all()
    serializer_class = PinWithAuthorReadSerializer
    lookup_field = "unique_id"


class SavePinView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pin_unique_id = request.data.get("pinID")
        board_unique_id = request.data.get("boardID")

        try:
            pin = Pin.objects.get(unique_id=pin_unique_id)
        except Pin.DoesNotExist:
            return Response(
                {"errors": [{"code": ERROR_CODE_PIN_NOT_FOUND}]},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            board = Board.objects.get(unique_id=board_unique_id)
        except Board.DoesNotExist:
            return Response(
                {"errors": [{"code": ERROR_CODE_BOARD_NOT_FOUND}]},
                status=status.HTTP_404_NOT_FOUND,
            )

        account = request.user.account

        if board.author != account:
            return Response(
                {"errors": [{"code": ERROR_CODE_FORBIDDEN}]},
                status=status.HTTP_403_FORBIDDEN,
            )

        response_body = {
            "pinID": pin_unique_id,
            "boardID": board_unique_id,
        }

        existing_pin_save = PinInBoard.objects.filter(pin=pin, board=board).first()

        if existing_pin_save:
            existing_pin_save.last_saved_at = timezone.now()
            existing_pin_save.save()

            return Response(
                response_body,
                status=status.HTTP_200_OK,
            )

        board.pins.add(pin)

        return Response(
            response_body,
            status=status.HTTP_201_CREATED,
        )
