from datetime import datetime, timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status

from ..models import User
from ..utils.constants import ERROR_CODE_UNAUTHORIZED


class AccountTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="john.doe@example.com",
            password="Pa$$wOrd",
            username="johndoe",
            initial="J",
            first_name="John",
            last_name="Doe",
        )

        self.client = APIClient()

    def test_user_details_happy_case(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/api/user-details/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["email"], self.user.email)
        self.assertEqual(response_data["username"], self.user.username)
        self.assertEqual(response_data["initial"], self.user.initial)
        self.assertEqual(response_data["first_name"], self.user.first_name)
        self.assertEqual(response_data["last_name"], self.user.last_name)

    def test_user_details_no_access_token(self):
        response = self.client.get("/api/user-details/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )

    def test_user_details_expired_access_token(self):
        # Create expired token for the test user
        access_token = AccessToken.for_user(self.user)
        access_token.set_exp(from_time=datetime.now() - timedelta(minutes=10))

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(access_token)}")

        response = self.client.get("/api/user-details/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )

    def test_user_details_invalid_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer invalid_token")

        response = self.client.get("/api/user-details/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )
