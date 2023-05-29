from datetime import datetime, timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status

from pinit_api.models import User, Account
from pinit_api.utils.constants import ERROR_CODE_UNAUTHORIZED


class AccountTests(APITestCase):
    def setUp(self):
        self.calling_user = User.objects.create_user(
            email="john.doe@example.com",
            password="Pa$$wOrd",
        )

        self.account = Account.objects.create(
            username="johndoe",
            type="personal",
            first_name="John",
            last_name="Doe",
            initial="J",
            owner=self.calling_user,
        )

        # Create another user and account,
        # to check that it won't be returned for the calling user set above
        other_user = User.objects.create_user(
            email="jane.doe@example.com",
            password="Pa$$wOrd",
        )
        Account.objects.create(
            username="janedoe",
            type="personal",
            first_name="Jane",
            last_name="Doe",
            initial="J",
            owner=other_user,
        )

        self.client = APIClient()

    def test_get_accounts_happy_case(self):
        tokens_pair = RefreshToken.for_user(self.calling_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()["data"]

        self.assertEqual(len(response_data), 1)

        account = response_data[0]
        self.assertEqual(account["type"], "accounts")
        self.assertEqual(account["id"], self.account.username)

        account_attributes = account["attributes"]

        self.assertEqual(account_attributes["username"], "johndoe")
        self.assertEqual(account_attributes["type"], "personal")
        self.assertEqual(account_attributes["initial"], "J")
        self.assertEqual(account_attributes["display_name"], "John Doe")
        self.assertEqual(account_attributes["owner_email"], "john.doe@example.com")

    def test_get_accounts_no_access_token(self):
        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )

    def test_get_accounts_expired_access_token(self):
        # Create expired token for the test user
        access_token = AccessToken.for_user(self.calling_user)
        access_token.set_exp(from_time=datetime.now() - timedelta(minutes=10))

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(access_token)}")

        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )

    def test_get_accounts_invalid_access_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer invalid_token")

        response = self.client.get("/api/accounts/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )
