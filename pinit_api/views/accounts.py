from rest_framework import generics
from drf_spectacular.utils import extend_schema

from ..models import Account
from ..serializers import AccountWithPublicDetailsReadSerializer
from ..doc.doc_accounts import SWAGGER_SCHEMAS


@extend_schema(**SWAGGER_SCHEMAS["accounts/<username>/"])
class GetAccountDetailsView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountWithPublicDetailsReadSerializer
    lookup_field = "username"
