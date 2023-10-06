from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from ..testing_utils import UserFactory, PinFactory
from pinit_api.views.search import ERROR_CODE_MISSING_SEARCH_PARAMETER


class SearchTests(APITestCase):
    def setUp(self):
        self.test_user = UserFactory.create()

        self.client = APIClient()

        # We will test a search autocomplete on "beach":
        PinFactory.create(
            title="My beacheresque view of a beachy beach",
            description="Isn't that beachiful-",
        )
        PinFactory.create(
            title="Isn't Beacho a beaufitul name for a boy?",
            description="And Beacha? Yes, beacha if it's a girl.",
        )
        PinFactory.create(
            title="Beautiful beach",
            description="I want to go to the beach.",
        )

    def tearDown(self):
        # Clear authentication headers:
        self.client.credentials()

    def test_search_autocomplete_happy_path(self):
        tokens_pair = RefreshToken.for_user(self.test_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/api/search/autocomplete/?search=beach")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        response_results = response_data["results"]

        # "beach" occurs three times so it should appear first in the list.
        # Then, "beacha" which occurs twice.
        # Then, all others, which occur once, ranked by alphabetical order.
        self.assertListEqual(
            response_results,
            ["beach", "beacha", "beacheresque", "beachiful", "beacho", "beachy"],
        )

    def test_search_autocomplete_missing_search_param(self):
        tokens_pair = RefreshToken.for_user(self.test_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.get("/api/search/autocomplete/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_MISSING_SEARCH_PARAMETER}],
        )
