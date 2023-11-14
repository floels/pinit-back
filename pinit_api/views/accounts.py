from rest_framework import generics

from ..models import Account
from ..serializers import AccountWithPublicDetailsReadSerializer
from ..utils.constants import ERROR_CODE_NOT_FOUND


class GetAccountDetailsView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountWithPublicDetailsReadSerializer
    lookup_field = "username"
