from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.conf import settings

from pinit_api.models import Pin
from ..testing_utils import UserFactory, PinFactory, JWTAuthenticationMixin

NUMBER_EXISTING_PINS = 150
PAGINATION_PAGE_SIZE = settings.REST_FRAMEWORK["PAGE_SIZE"]


class GetPinSuggestionsTests(APITestCase, JWTAuthenticationMixin):
    def setUp(self):
        self.pins = PinFactory.create_batch(NUMBER_EXISTING_PINS)

        self.client = APIClient()
        self.calling_user = UserFactory()
        self.authenticate_client(self.calling_user)

    def test_get_pin_suggestions_first_page(self):
        response = self.client.get("/api/pins/suggestions/", {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["count"], NUMBER_EXISTING_PINS)

        first_response_item = response_data["results"][0]
        most_recent_pin = Pin.objects.latest("created_at")
        self.check_response_item_against_pin_object(
            first_response_item, most_recent_pin
        )

    def test_get_pin_suggestions_second_page(self):
        response = self.client.get("/api/pins/suggestions/", {"page": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["count"], NUMBER_EXISTING_PINS)

        first_response_item = response_data["results"][0]
        most_recent_pin_second_page = Pin.objects.order_by("-created_at")[
            PAGINATION_PAGE_SIZE
        ]
        self.check_response_item_against_pin_object(
            first_response_item, most_recent_pin_second_page
        )

    def check_response_item_against_pin_object(self, first_response_item, pin):
        self.assertEqual(first_response_item["unique_id"], pin.unique_id)
        self.assertEqual(first_response_item["image_url"], pin.image_url)
        self.assertEqual(first_response_item["title"], pin.title)
        self.assertEqual(
            first_response_item["description"],
            pin.description,
        )
        author_data = first_response_item["author"]
        self.assertEqual(author_data["username"], pin.author.username)
        self.assertEqual(author_data["display_name"], pin.author.display_name)


class GetPinDetailsTests(APITestCase):
    def setUp(self):
        self.pins = PinFactory.create_batch(NUMBER_EXISTING_PINS)

        self.client = APIClient()

    def test_get_pin_details_happy_path(self):
        first_pin = self.pins[0]

        response = self.client.get(f"/api/pins/{first_pin.unique_id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["unique_id"], first_pin.unique_id)
        self.assertEqual(response_data["image_url"], first_pin.image_url)
        self.assertEqual(response_data["title"], first_pin.title)
        self.assertEqual(response_data["author"]["username"], first_pin.author.username)
        self.assertEqual(
            response_data["author"]["display_name"], first_pin.author.display_name
        )

    def test_get_pin_details_not_exists(self):
        tentative_non_existing_unique_id = 100_000_000_000_000_000

        while Pin.objects.filter(unique_id=tentative_non_existing_unique_id).exists():
            tentative_non_existing_unique_id += 1

        non_existing_unique_id = tentative_non_existing_unique_id

        response = self.client.get(f"/api/pins/{non_existing_unique_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
