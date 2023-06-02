from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from pinit_api.models import Pin
from ..testing_utils import UserFactory, PinFactory, JWTAuthenticationMixin

NUMBER_EXISTING_PINS = 3


class PinSuggestionsTests(APITestCase, JWTAuthenticationMixin):
    def setUp(self):
        self.pins = PinFactory.create_batch(NUMBER_EXISTING_PINS)

        self.most_recent_pin = Pin.objects.latest("created_at")
        self.most_recent_pin_author = self.most_recent_pin.author
        self.most_recent_pin_author_display_name = f"{self.most_recent_pin_author.first_name} {self.most_recent_pin_author.last_name}"

        self.client = APIClient()
        self.calling_user = UserFactory()
        self.authenticate_client(self.calling_user)

    def test_get_pin_suggestions_happy_case(self):
        response = self.client.get("/api/pin-suggestions/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(len(response_data), NUMBER_EXISTING_PINS)

        first_result = response_data[0]
        self.check_first_result_happy_case(first_result)

    def check_first_result_happy_case(self, first_result):
        self.assertEqual(first_result["id"], self.most_recent_pin.id)
        self.assertEqual(first_result["image_url"], self.most_recent_pin.image_url)
        self.assertEqual(first_result["title"], self.most_recent_pin.title)
        self.assertEqual(
            first_result["description"],
            self.most_recent_pin.description,
        )
        author_data = first_result["author"]
        self.assertEqual(author_data["username"], self.most_recent_pin_author.username)
        self.assertEqual(
            author_data["display_name"], self.most_recent_pin_author_display_name
        )
