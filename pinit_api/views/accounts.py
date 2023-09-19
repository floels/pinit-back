from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from ..models import Account
from ..doc.doc_accounts import SWAGGER_SCHEMAS
from ..serializers import AccountWithOwnerEmailReadSerializer


@swagger_auto_schema(**SWAGGER_SCHEMAS["GET /accounts/"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_accounts(request):
    accounts = Account.objects.select_related("owner").filter(owner=request.user)

    serialized_accounts = AccountWithOwnerEmailReadSerializer(accounts, many=True)

    response_data = {"results": serialized_accounts.data}

    return Response(response_data)
