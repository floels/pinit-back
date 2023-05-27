from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from ..models import User, Pin
from ..serializers import PinWithAuthorReadSerializer


class PinSuggestionsList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        dummy_user = User(
            email="john.doe@example.com",
            username="john.doe",
            first_name="John",
            last_name="Doe",
        )
        dummy_pin = Pin(
            title="Dummy Pin", image_url="https://some.url.com", author=dummy_user
        )

        serialized_pins = PinWithAuthorReadSerializer([dummy_pin], many=True)
        included_data = [PinWithAuthorReadSerializer().get_included(dummy_pin)]

        return Response({"data": serialized_pins.data, "included": included_data})
