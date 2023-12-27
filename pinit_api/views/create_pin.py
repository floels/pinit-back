from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_pin(request):
    return Response({"pin_id": "01234567789012345"}, status=status.HTTP_201_CREATED)
