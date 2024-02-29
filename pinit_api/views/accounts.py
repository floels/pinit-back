from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from ..models import Account
from ..serializers import AccountWithPublicDetailsReadSerializer


class GetAccountDetailsView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountWithPublicDetailsReadSerializer
    lookup_field = "username"


class GetMyAccountDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountWithPublicDetailsReadSerializer

    def get_object(self):
        return self.request.user.account
