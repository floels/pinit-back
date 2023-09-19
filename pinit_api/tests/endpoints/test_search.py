from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from ..testing_utils import UserFactory
from pinit_api.utils.constants import ERROR_CODE_UNAUTHORIZED


class SearchTests(APITestCase):
    def setUp(self):
        self.test_user = UserFactory.create()

        self.client = APIClient()

    def tearDown(self):
        # Clear authentication headers:
        self.client.credentials()

    def test_search_autocomplete_happy_path(self):
        tokens_pair = RefreshToken.for_user(self.test_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/api/accounts/?search=food")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        response_results = response_data["results"]

        self.assertGreaterEqual(len(response_results), 1)

    def test_get_accounts_no_access_token(self):
        response = self.client.get("/api/search/autocomplete")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )
