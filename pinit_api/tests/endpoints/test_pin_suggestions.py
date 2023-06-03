from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from pinit_api.models import Pin
from ..testing_utils import UserFactory, PinFactory, JWTAuthenticationMixin
from pinit_api.views.pin_suggestions import PAGE_SIZE

NUMBER_EXISTING_PINS = 150


class PinSuggestionsTests(APITestCase, JWTAuthenticationMixin):
    def setUp(self):
        self.pins = PinFactory.create_batch(NUMBER_EXISTING_PINS)

        self.client = APIClient()
        self.calling_user = UserFactory()
        self.authenticate_client(self.calling_user)

    def test_get_pin_suggestions_first_page(self):
        response = self.client.get("/api/pin-suggestions/", {"page": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["count"], NUMBER_EXISTING_PINS)

        first_response_item = response_data["results"][0]
        most_recent_pin = Pin.objects.latest("created_at")
        self.check_response_item_against_pin_object(
            first_response_item, most_recent_pin
        )

    def test_get_pin_suggestions_second_page(self):
        response = self.client.get("/api/pin-suggestions/", {"page": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["count"], NUMBER_EXISTING_PINS)

        first_response_item = response_data["results"][0]
        most_recent_pin_second_page = Pin.objects.order_by("-created_at")[PAGE_SIZE]
        self.check_response_item_against_pin_object(
            first_response_item, most_recent_pin_second_page
        )

    def check_response_item_against_pin_object(self, first_response_item, pin):
        self.assertEqual(first_response_item["id"], pin.id)
        self.assertEqual(first_response_item["image_url"], pin.image_url)
        self.assertEqual(first_response_item["title"], pin.title)
        self.assertEqual(
            first_response_item["description"],
            pin.description,
        )
        author_data = first_response_item["author"]
        self.assertEqual(author_data["username"], pin.author.username)
        self.assertEqual(author_data["display_name"], pin.author.get_display_name())
