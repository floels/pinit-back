from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from ..serializers.user_serializers import UserReadSerializer
from ..doc.account_doc import SWAGGER_SCHEMAS


@swagger_auto_schema(**SWAGGER_SCHEMAS["UserDetailsView"])
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    user = request.user
    serializer = UserReadSerializer(user)
    return Response(serializer.data)
