from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ..testing_utils import AccountFactory


class CreatePinTests(APITestCase):
    def setUp(self):
        self.test_account = AccountFactory()

        self.test_user = self.test_account.owner

        self.client = APIClient()
        tokens_pair = RefreshToken.for_user(self.test_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_create_pin_happy_path(self):
        response = self.client.post("/api/create-pin/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
