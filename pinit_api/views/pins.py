from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, views

from ..models import Pin, Board, PinInBoard
from ..serializers import PinWithAuthorReadSerializer
from ..lib.constants import (
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

    def check_board_author(self, board, user):
        return board.author == user.account

    def update_last_pin_added_at(self, board, now):
        board.last_pin_added_at = now
        board.save()

    def update_or_create_pin_in_board(self, pin, board):
        now = timezone.now()

        self.update_last_pin_added_at(board, now)

        existing_pin_save = PinInBoard.objects.filter(pin=pin, board=board).first()

        if existing_pin_save:
            existing_pin_save.last_saved_at = now
            existing_pin_save.save()
            return True  # Indicates an update
        else:
            board.pins.add(pin)
            return False  # Indicates a creation

    def post(self, request):
        pin_unique_id = request.data.get("pin_id")
        board_unique_id = request.data.get("board_id")

        pin = Pin.objects.filter(unique_id=pin_unique_id).first()
        if not pin:
            return Response(
                {"errors": [{"code": ERROR_CODE_PIN_NOT_FOUND}]},
                status=status.HTTP_404_NOT_FOUND,
            )

        board = Board.objects.filter(unique_id=board_unique_id).first()
        if not board:
            return Response(
                {"errors": [{"code": ERROR_CODE_BOARD_NOT_FOUND}]},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not self.check_board_author(board, request.user):
            return Response(
                {"errors": [{"code": ERROR_CODE_FORBIDDEN}]},
                status=status.HTTP_403_FORBIDDEN,
            )

        response_body = {"pin_id": pin_unique_id, "board_id": board_unique_id}
        was_updated = self.update_or_create_pin_in_board(pin, board)

        return Response(
            response_body,
            status=status.HTTP_200_OK if was_updated else status.HTTP_201_CREATED,
        )
