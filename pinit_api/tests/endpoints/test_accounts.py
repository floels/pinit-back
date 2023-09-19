from datetime import datetime, timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status

from pinit_api.utils.constants import ERROR_CODE_UNAUTHORIZED
from ..testing_utils import AccountFactory


class AccountTests(APITestCase):
    def setUp(self):
        self.test_account = AccountFactory.create()

        self.test_user = self.test_account.owner

        # Create another user and account,
        # to check that it won't be returned for the calling user set above:
        _ = AccountFactory.create()

        self.client = APIClient()

    def tearDown(self):
        # Clear authentication headers:
        self.client.credentials()

    def test_get_accounts_happy_path(self):
        tokens_pair = RefreshToken.for_user(self.test_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        response_results = response_data["results"]

        self.assertEqual(len(response_results), 1)

        account = response_results[0]

        self.assertEqual(account["username"], self.test_account.username)
        self.assertEqual(account["type"], self.test_account.type)
        self.assertEqual(account["initial"], self.test_account.initial)
        self.assertEqual(account["display_name"], self.test_account.display_name)
        self.assertEqual(account["owner_email"], self.test_user.email)

    def test_get_accounts_no_access_token(self):
        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )

    def test_get_accounts_expired_access_token(self):
        # Create expired token for the test user
        access_token = AccessToken.for_user(self.test_user)
        access_token.set_exp(from_time=datetime.now() - timedelta(minutes=10))
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(access_token)}")

        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )

    def test_get_accounts_invalid_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")

        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )
