from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from ..testing_utils import UserFactory, PinFactory
from pinit_api.views.search import ERROR_CODE_MISSING_SEARCH_PARAMETER


class SearchTests(APITestCase):
    def setUp(self):
        self.test_user = UserFactory.create()

        # Create authenticated client:
        self.client = APIClient()
        tokens_pair = RefreshToken.for_user(self.test_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # We will test a search autocomplete on "beach":
        self.pin_1 = PinFactory.create(
            title="My beacheresque view of a beachy beach",
            description="Isn't that beachiful-",
        )
        self.pin_2 = PinFactory.create(
            title="Isn't Beacho a beaufitul name for a boy?",
            description="And Beacha? Yes, beacha if it's a girl.",
        )
        self.pin_3 = PinFactory.create(
            title="Beautiful beach",
            description="I want to go to the beach.",
        )

    def test_search_autocomplete_happy_path(self):
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
        response = self.client.get("/api/search/autocomplete/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_MISSING_SEARCH_PARAMETER}],
        )

    def test_search_pins_happy_path(self):
        response = self.client.get("/api/search/?q=beach")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        response_results = response_data["results"]

        expected_results = [
            {
                "id": self.pin_3.id,
                "title": self.pin_3.title,
                "description": self.pin_3.description,
                "image_url": self.pin_3.image_url,
                "author": {
                    "username": self.pin_3.author.username,
                    "display_name": self.pin_3.author.display_name,
                },
            },
            {
                "id": self.pin_1.id,
                "title": self.pin_1.title,
                "description": self.pin_1.description,
                "image_url": self.pin_1.image_url,
                "author": {
                    "username": self.pin_1.author.username,
                    "display_name": self.pin_1.author.display_name,
                },
            },
        ]

        self.assertListEqual(response_results, expected_results)

    def test_search_pins_no_result(self):
        response = self.client.get("/api/search/?q=horse")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        response_results = response_data["results"]

        self.assertListEqual(response_results, [])

    def test_search_pins_missing_search_param(self):
        response = self.client.get("/api/search/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_MISSING_SEARCH_PARAMETER}],
        )
