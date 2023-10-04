from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


from ..models import Account
from ..serializers import AccountWithOwnerEmailReadSerializer
from ..doc.doc_accounts import SWAGGER_SCHEMAS


@extend_schema(**SWAGGER_SCHEMAS["accounts/"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_accounts(request):
    accounts = Account.objects.select_related("owner").filter(owner=request.user)

    serialized_accounts = AccountWithOwnerEmailReadSerializer(accounts, many=True)

    response_data = {"results": serialized_accounts.data}

    return Response(response_data)
