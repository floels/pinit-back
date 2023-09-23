from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from unittest.mock import patch, Mock

from ..testing_utils import UserFactory
from pinit_api.utils.constants import ERROR_CODE_UNAUTHORIZED
from pinit_api.views.search import ERROR_CODE_MISSING_SEARCH_PARAMETER


class SearchTests(APITestCase):
    def setUp(self):
        self.test_user = UserFactory.create()

        self.client = APIClient()

    def tearDown(self):
        # Clear authentication headers:
        self.client.credentials()

    def test_search_autocomplete_happy_path(self):
        mock_response_google = Mock()

        mock_response_google_results = ["food", "food snapchat", "food recipes"]

        mock_response_google.json.return_value = [
            "food",
            mock_response_google_results,
        ]

        with patch("requests.get", return_value=mock_response_google):
            tokens_pair = RefreshToken.for_user(self.test_user)
            access_token = str(tokens_pair.access_token)
            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

            response = self.client.get("/api/search/autocomplete/?search=food")

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_data = response.json()

            response_results = response_data["results"]

            self.assertListEqual(response_results, mock_response_google_results)

    def test_get_accounts_no_access_token(self):
        response = self.client.get("/api/search/autocomplete/?search=food")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_UNAUTHORIZED}],
        )

    def test_get_accounts_missing_search_param(self):
        tokens_pair = RefreshToken.for_user(self.test_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/api/search/autocomplete/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_MISSING_SEARCH_PARAMETER}],
        )
