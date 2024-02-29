from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from pinit_api.models import Pin
from ..testing_utils import PinFactory, BoardFactory
from pinit_api.utils.constants import (
    ERROR_CODE_PIN_NOT_FOUND,
    ERROR_CODE_BOARD_NOT_FOUND,
    ERROR_CODE_FORBIDDEN,
)

NUMBER_EXISTING_PINS = 150
PAGINATION_PAGE_SIZE = settings.REST_FRAMEWORK["PAGE_SIZE"]


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
        self.assertEqual(
            response_data["author"]["profile_picture_url"],
            first_pin.author.profile_picture_url,
        )

    def test_get_pin_details_not_exists(self):
        tentative_non_existing_unique_id = 100_000_000_000_000_000

        while Pin.objects.filter(unique_id=tentative_non_existing_unique_id).exists():
            tentative_non_existing_unique_id += 1

        non_existing_unique_id = tentative_non_existing_unique_id

        response = self.client.get(f"/api/pins/{non_existing_unique_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SavePinTests(APITestCase):
    def setUp(self):
        self.board = BoardFactory()

        self.pin_already_saved = PinFactory()
        self.board.pins.add(self.pin_already_saved)

        self.pin_to_save = PinFactory()

        self.client = APIClient()
        self.client.force_authenticate(user=self.board.author.owner)

        self.board_not_owned = BoardFactory()

    def test_save_pin_happy_path(self):
        request_payload = {
            "pinID": self.pin_to_save.unique_id,
            "boardID": self.board.unique_id,
        }

        response = self.client.post("/api/save-pin/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.board.pins.count(), 2)

    def test_save_pin_already_saved(self):
        now = timezone.now()

        request_payload = {
            "pinID": self.pin_already_saved.unique_id,
            "boardID": self.board.unique_id,
        }

        response = self.client.post("/api/save-pin/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertAlmostEqual(
            self.board.pins_in_board.first().last_saved_at,
            now,
            delta=timedelta(seconds=1),
        )

        self.assertEqual(self.board.pins.count(), 1)

    def test_save_pin_doesnt_exist(self):
        non_existing_pin_id = 100_000_000_000_000_000

        request_payload = {
            "pinID": non_existing_pin_id,
            "boardID": self.board.unique_id,
        }

        response = self.client.post("/api/save-pin/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response_data = response.json()

        self.assertEqual(response_data["errors"], [{"code": ERROR_CODE_PIN_NOT_FOUND}])

        self.assertEqual(self.board.pins.count(), 1)

    def test_save_board_doesnt_exist(self):
        non_existing_board_id = 100_000_000_000_000

        request_payload = {
            "pinID": self.pin_to_save.unique_id,
            "boardID": non_existing_board_id,
        }

        response = self.client.post("/api/save-pin/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"], [{"code": ERROR_CODE_BOARD_NOT_FOUND}]
        )

        self.assertEqual(self.board.pins.count(), 1)

    def test_save_board_not_owned(self):
        request_payload = {
            "pinID": self.pin_to_save.unique_id,
            "boardID": self.board_not_owned.unique_id,
        }

        response = self.client.post("/api/save-pin/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response_data = response.json()

        self.assertEqual(response_data["errors"], [{"code": ERROR_CODE_FORBIDDEN}])

        self.assertEqual(self.board.pins.count(), 1)
