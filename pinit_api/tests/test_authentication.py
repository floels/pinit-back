from django.test import TestCase
from ..models import User
from ..constants import ERROR_CODE_INVALID_EMAIL, ERROR_CODE_INVALID_PASSWORD


class AuthenticationTests(TestCase):
    def setUp(self):
        # Create an existing user:
        self.existing_user_email = "existing.user@example.com"
        self.existing_user_password = "Pa$$wOrd_existing_user"

        self.user = User.objects.create_user(
            email=self.existing_user_email,
            password=self.existing_user_password,
        )

    def test_signup_happy_case(self):
        """
        Ensure we can sign up when providing valid data.
        """
        data = {
            "email": "new.user@example.com",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-01-01",
        }
        response = self.client.post("/api/signup/", data, format="json")

        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        access_token = response_data["access"]
        assert bool(access_token)
        refresh_token = response_data["refresh"]
        assert bool(refresh_token)

    def test_obtain_refresh_jw_token_happy_case(self):
        """
        Ensure we can obtain and refresh a JWT when providing valid credentials.
        """
        data = {
            "email": self.existing_user_email,
            "password": self.existing_user_password,
        }
        response_obtain = self.client.post("/api/token/", data, format="json")

        self.assertEqual(response_obtain.status_code, 200)
        response_obtain_data = response_obtain.json()
        access_token = response_obtain_data["access"]
        assert bool(access_token)

        # Refresh the access token:
        refresh_token = response_obtain_data["refresh"]
        response_refresh = self.client.post(
            "/api/token/refresh/", {"refresh": refresh_token}, format="json"
        )

        self.assertEqual(response_refresh.status_code, 200)
        refreshed_access_token = response_refresh.json()["access"]
        assert bool(refreshed_access_token)

    def test_obtain_jw_token_wrong_credentials(self):
        """
        Ensure we don't obtain a JWT when providing invalid credentials.
        """
        data_wrong_email = {"email": "wrong_email", "password": "somePa$$word"}
        response_wrong_email = self.client.post(
            "/api/token/", data_wrong_email, format="json"
        )

        self.assertEqual(response_wrong_email.status_code, 401)
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

        self.assertEqual(response_wrong_password.status_code, 401)
        self.assertEqual(
            response_wrong_password.json()["errors"],
            [{"code": ERROR_CODE_INVALID_PASSWORD}],
        )

    def test_refresh_jw_token_wrong_refresh(self):
        """
        Ensure we don't obtain a refreshed JWT when providing a wrong refresh token.
        """
        response = self.client.post(
            "/api/token/refresh/", {"refresh": "wrong.refreshToken"}, format="json"
        )

        self.assertEqual(response.status_code, 401)
