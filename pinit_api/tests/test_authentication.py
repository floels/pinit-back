from django.test import TestCase
from rest_framework import status
from ..models import User
from ..utils.constants import (
    ERROR_CODE_INVALID_EMAIL,
    ERROR_CODE_INVALID_PASSWORD,
    ERROR_CODE_INVALID_REFRESH_TOKEN,
)


class AuthenticationTests(TestCase):
    def setUp(self):
        self.existing_user_email = "existing.user@example.com"
        self.existing_user_password = "Pa$$wOrd_existing_user"

        self.user = User.objects.create_user(
            email=self.existing_user_email,
            password=self.existing_user_password,
        )

    def test_obtain_and_refresh_token_happy_case(self):
        """
        Ensure we can obtain and refresh a JWT when providing valid credentials.
        """
        data = {
            "email": self.existing_user_email,
            "password": self.existing_user_password,
        }
        response_obtain = self.client.post("/api/token/", data, format="json")

        self.assertEqual(response_obtain.status_code, status.HTTP_200_OK)
        response_obtain_data = response_obtain.json()
        access_token = response_obtain_data["access_token"]
        assert bool(access_token)

        # Refresh the access token:
        refresh_token = response_obtain_data["refresh_token"]
        response_refresh = self.client.post(
            "/api/token/refresh/", {"refresh_token": refresh_token}, format="json"
        )

        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        refreshed_access_token = response_refresh.json()["access_token"]
        assert bool(refreshed_access_token)

    def test_obtain_token_wrong_credentials(self):
        data_wrong_email = {"email": "wrong_email", "password": "somePa$$word"}
        response_wrong_email = self.client.post(
            "/api/token/", data_wrong_email, format="json"
        )

        self.assertEqual(response_wrong_email.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response_wrong_email.json()["errors"],
            [{"code": ERROR_CODE_INVALID_EMAIL}],
        )

        data_wrong_password = {
            "email": self.existing_user_email,
            "password": "somePa$$word",
        }
        response_wrong_password = self.client.post(
            "/api/token/", data_wrong_password, format="json"
        )

        self.assertEqual(
            response_wrong_password.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            response_wrong_password.json()["errors"],
            [{"code": ERROR_CODE_INVALID_PASSWORD}],
        )

    def test_refresh_token_wrong_refresh_token(self):
        response = self.client.post(
            "/api/token/refresh/",
            {"refresh_token": "wrong.refreshToken"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_INVALID_REFRESH_TOKEN}],
        )
