from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ..models import User

class AccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="john.doe@example.com",
            password="Pa$$wOrd",
            initial="J",
            first_name="John",
            last_name="Doe"
        )

        self.client=APIClient()

    def test_user_details_happy_case(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get("/api/user-details/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["email"], self.user.email)
        self.assertEqual(response_data["initial"], self.user.initial)
        self.assertEqual(response_data["first_name"], self.user.first_name)
        self.assertEqual(response_data["last_name"], self.user.last_name)

    def test_user_unauthenticated(self):
        response = self.client.get("/api/user-details/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
