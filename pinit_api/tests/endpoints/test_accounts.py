from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from pinit_api.utils.constants import ERROR_CODE_NOT_FOUND
from ..testing_utils import AccountFactory


class GetAccountDetailsTests(APITestCase):
    def setUp(self):
        self.account = AccountFactory()

        self.client = APIClient()

    def test_get_account_details_happy_path(self):
        response = self.client.get(f"/api/accounts/{self.account.username}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["username"], self.account.username)
        self.assertEqual(response_data["type"], self.account.type)
        self.assertEqual(response_data["display_name"], self.account.display_name)

        self.assertIn("profile_picture_url", response_data)
        self.assertIn("background_picture_url", response_data)
        self.assertIn("description", response_data)

    def test_get_account_details_not_found(self):
        response = self.client.get("/api/account/non_existing_username/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
