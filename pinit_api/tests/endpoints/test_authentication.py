from datetime import datetime, timezone
from django.test import TestCase
from django.utils.dateparse import parse_datetime
from django.conf import settings
from rest_framework import status
from pinit_api.models import User
from pinit_api.lib.constants import (
    ERROR_CODE_INVALID_EMAIL,
    ERROR_CODE_INVALID_PASSWORD,
)
from pinit_api.views.authentication import (
    ERROR_CODE_INVALID_REFRESH_TOKEN,
    ERROR_CODE_MISSING_REFRESH_TOKEN,
)


class AuthenticationTests(TestCase):
    def setUp(self):
        self.existing_user_email = "existing.user@example.com"
        self.existing_user_password = "Pa$$wOrd_existing_user"

        self.user = User.objects.create_user(
            email=self.existing_user_email,
            password=self.existing_user_password,
        )

    def test_obtain_token_happy_path(self):
        request_payload = {
            "email": self.existing_user_email,
            "password": self.existing_user_password,
        }

        response = self.client.post(
            "/api/token/obtain/", request_payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        access_token = response_data["access_token"]
        assert bool(access_token)

        # Check that access token expiration date is set as expected:
        access_token_expiration_utc = parse_datetime(
            response_data["access_token_expiration_utc"]
        )
        now_utc = datetime.now(timezone.utc)
        expected_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        expected_access_token_expiration_utc = now_utc + expected_lifetime

        delta_actual_predicted_expiration_seconds = abs(
            (
                (access_token_expiration_utc - expected_access_token_expiration_utc)
            ).total_seconds()
        )
        tolerance_seconds = 60
        self.assertLess(delta_actual_predicted_expiration_seconds, tolerance_seconds)

        # NB: we'll test the presence and validity of the refresh token via the following test

    def test_obtain_and_refresh_token_happy_path(self):
        request_payload_obtain = {
            "email": self.existing_user_email,
            "password": self.existing_user_password,
        }

        response_obtain = self.client.post(
            "/api/token/obtain/", request_payload_obtain, format="json"
        )

        response_data_obtain = response_obtain.json()

        refresh_token = response_data_obtain["refresh_token"]

        response_refresh = self.client.post(
            "/api/token/refresh/", {"refresh_token": refresh_token}, format="json"
        )

        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)

        response_data_refresh = response_refresh.json()

        refreshed_access_token = response_data_refresh["access_token"]
        assert bool(refreshed_access_token)

        refreshed_access_expiration_date = response_data_refresh[
            "access_token_expiration_utc"
        ]
        assert bool(refreshed_access_expiration_date)

    def test_obtain_token_wrong_email(self):
        request_payload = {"email": "wrong_email", "password": "somePa$$word"}

        response = self.client.post(
            "/api/token/obtain/", request_payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_INVALID_EMAIL}],
        )

    def test_obtain_token_wrong_password(self):
        request_payload = {
            "email": self.existing_user_email,
            "password": "somePa$$word",
        }

        response = self.client.post(
            "/api/token/obtain/", request_payload, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_INVALID_PASSWORD}],
        )

    def test_refresh_token_wrong_refresh_token(self):
        response = self.client.post(
            "/api/token/refresh/",
            {"refresh_token": "wrong.refresh.token"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_INVALID_REFRESH_TOKEN}],
        )

    def test_refresh_token_missing_refresh_token(self):
        response = self.client.post(
            "/api/token/refresh/",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_MISSING_REFRESH_TOKEN}],
        )
