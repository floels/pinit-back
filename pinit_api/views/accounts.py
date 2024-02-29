from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response

from ..models import Account, Board
from ..serializers.account_serializers import AccountWithPublicDetailsReadSerializer
from ..serializers.board_serializers import BoardSerializer


class GetAccountPublicDetailsView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountWithPublicDetailsReadSerializer
    lookup_field = "username"


class GetMyAccountDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountWithPublicDetailsReadSerializer

    def get(self, request):
        account = request.user.account
        account_serializer = self.get_serializer(account)

        boards = Board.objects.filter(author=account).order_by("-last_pin_added_at")
        boards_serializer = BoardSerializer(boards, many=True)

        response_data = account_serializer.data
        response_data["boards"] = boards_serializer.data

        return Response(response_data)
