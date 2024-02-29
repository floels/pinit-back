from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from pinit_api.models import Pin, PinSave
from ..testing_utils import PinFactory, AccountFactory

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
        self.account = AccountFactory()

        self.pin_already_saved = PinFactory()
        self.account.saved_pins.add(self.pin_already_saved)

        self.pin_to_save = PinFactory()

        self.client = APIClient()
        self.client.force_authenticate(user=self.account.owner)

    def test_save_pin_happy_path(self):
        response = self.client.post(f"/api/save-pin/{self.pin_to_save.unique_id}/")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_data = response.json()

        self.assertEqual(response_data["pin"]["unique_id"], self.pin_to_save.unique_id)
        self.assertEqual(response_data["account"], self.account.username)

        self.assertEqual(self.account.saved_pins.count(), 2)

    def test_save_pin_already_saved(self):
        now = timezone.now()

        response = self.client.post(
            f"/api/save-pin/{self.pin_already_saved.unique_id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(self.account.saved_pins.count(), 1)
        self.assertAlmostEqual(
            self.account.pin_saves.first().last_saved_at,
            now,
            delta=timedelta(seconds=1),
        )

    def test_save_pin_not_exists(self):
        non_existing_pin_id = 100_000_000_000_000_000

        response = self.client.post(f"/api/save-pin/{non_existing_pin_id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(self.account.saved_pins.count(), 1)
