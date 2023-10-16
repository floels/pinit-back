from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.conf import settings

from ..testing_utils import UserFactory, PinFactory
from pinit_api.views.search import ERROR_CODE_MISSING_SEARCH_PARAMETER
from pinit_api.models import Pin

NUMBER_PINS_MATCHING_SEARCH_TITLE = 75
NUMBER_PINS_MATCHING_SEARCH_DESCRIPTION = 75

PAGINATION_PAGE_SIZE = settings.REST_FRAMEWORK["PAGE_SIZE"]


class SearchTests(APITestCase):
    def setUp(self):
        self.test_user = UserFactory.create()

        # Create authenticated client:
        self.client = APIClient()
        tokens_pair = RefreshToken.for_user(self.test_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

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

        # We will search for pins containing "sunset":
        PinFactory.create_batch(
            NUMBER_PINS_MATCHING_SEARCH_TITLE, title="Beautiful sunset", description=""
        )
        PinFactory.create_batch(
            NUMBER_PINS_MATCHING_SEARCH_DESCRIPTION,
            description="That's a beautiful sunset.",
        )

    def test_search_autocomplete_happy_path(self):
        response = self.client.get("/api/search/autocomplete/", {"search": "beach"})

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

    def test_search_pins_happy_path_first_page(self):
        response = self.client.get("/api/search/", {"q": "sunset", "page": "1"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(
            response_data["count"],
            NUMBER_PINS_MATCHING_SEARCH_TITLE + NUMBER_PINS_MATCHING_SEARCH_DESCRIPTION,
        )

        first_result = response_data["results"][0]

        self.assertEqual(first_result["title"], "Beautiful sunset")
        self.assertEqual(first_result["description"], "")
        self.assertTrue(first_result["image_url"])
        self.assertTrue(first_result["author"]["username"])
        self.assertTrue(first_result["author"]["display_name"])

        last_result = response_data["results"][PAGINATION_PAGE_SIZE - 1]

        self.assertEqual(last_result["title"], "Beautiful sunset")

        # Check that results are ordered by decreasing creation date:
        pin_first_result = Pin.objects.get(unique_id=first_result["unique_id"])
        pin_last_result = Pin.objects.get(unique_id=last_result["unique_id"])

        self.assertGreater(pin_first_result.created_at, pin_last_result.created_at)

    def test_search_pins_happy_path_second_page(self):
        response = self.client.get("/api/search/", {"q": "sunset", "page": "2"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        first_result = response_data["results"][0]

        self.assertEqual(first_result["title"], "Beautiful sunset")

        last_result = response_data["results"][PAGINATION_PAGE_SIZE - 1]

        self.assertEqual(last_result["description"], "That's a beautiful sunset.")

    def test_search_pins_no_result(self):
        response = self.client.get("/api/search/", {"q": "horse"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["count"], 0)

        self.assertListEqual(response_data["results"], [])

    def test_search_pins_missing_search_param(self):
        response = self.client.get("/api/search/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_MISSING_SEARCH_PARAMETER}],
        )
