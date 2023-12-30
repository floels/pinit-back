from rest_framework import generics
from drf_spectacular.utils import extend_schema

from ..models import Account
from ..serializers import AccountWithPublicDetailsReadSerializer
from ..doc.doc_accounts import SWAGGER_SCHEMAS


class GetAccountDetailsView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountWithPublicDetailsReadSerializer
    lookup_field = "username"

    @extend_schema(**SWAGGER_SCHEMAS["accounts/<username>/"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
