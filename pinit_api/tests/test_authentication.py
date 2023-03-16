from django.test import TestCase
from django.contrib.auth.models import User
from pinit_api.constants import ERROR_CODE_INVALID_USERNAME, ERROR_CODE_INVALID_PASSWORD


class AuthenticationTests(TestCase):
    def setUp(self):
        # Create the user who will authenticate:
        self.user_username = "myuser@example.com"
        self.user_password = "mypassword"

        self.user = User.objects.create_user(
            username=self.user_username,
            email=self.user_username,
            password=self.user_password,
        )

    def test_obtain_refresh_jw_token_happy_path(self):
        """
        Ensure we can obtain and refresh a JWT when providing valid credentials.
        """
        data = {"username": self.user_username, "password": self.user_password}
        response_obtain = self.client.post("/api/token/", data, format="json")

        self.assertEqual(response_obtain.status_code, 200)
        access_token = response_obtain.json()["access"]
        assert bool(access_token)

        # Refresh the access token:
        refresh_token = response_obtain.json()["refresh"]
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
        data_wrong_username = {"username": "wrong_username", "password": "somePa$$word"}
        response_wrong_username = self.client.post(
            "/api/token/", data_wrong_username, format="json"
        )

        self.assertEqual(response_wrong_username.status_code, 401)
        self.assertEqual(
            response_wrong_username.json()["errors"],
            [{"code": ERROR_CODE_INVALID_USERNAME}],
        )

        data_wrong_password = {
            "username": self.user_username,
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
