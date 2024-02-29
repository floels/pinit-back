import boto3
from io import BytesIO
from moto import mock_s3
from unittest import mock
from django.conf import settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from ..testing_utils import AccountFactory
from pinit_api.models import Pin
from pinit_api.views.pin_creation import compute_file_url_s3
from pinit_api.utils.constants import (
    ERROR_CODE_MISSING_PIN_IMAGE_FILE,
    ERROR_CODE_PIN_CREATION_FAILED,
)

S3_BUCKET_NAME = settings.S3_PINS_BUCKET_NAME


# Inspired by https://docs.getmoto.org/en/latest/docs/getting_started.html#class-decorator
@mock_s3
class CreatePinTests(APITestCase):
    def setUp(self):
        self.test_account = AccountFactory()
        self.test_username = self.test_account.username
        self.test_user = self.test_account.owner

        self.client = APIClient()
        self.client.force_authenticate(self.test_user)

        self.pin_image_file_content = b"pin image data"
        self.pin_image_file = BytesIO(self.pin_image_file_content)
        self.pin_image_file.name = "pin_image_file.jpg"

        s3_resource = boto3.resource("s3")
        bucket = s3_resource.Bucket(S3_BUCKET_NAME)
        bucket.create()

    def check_file_in_s3(self, expected_key, expected_content):
        s3 = boto3.resource("s3")

        object = s3.Object(S3_BUCKET_NAME, expected_key)

        file_content = object.get()["Body"].read()

        self.assertEqual(file_content, expected_content)

    def test_create_pin_happy_path(self):
        data = {
            "title": "Title",
            "description": "Description",
            "image_file": self.pin_image_file,
        }

        response = self.client.post("/api/create-pin/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Pin.objects.count(), 1)

        created_pin = Pin.objects.get()

        self.assertEqual(created_pin.title, data["title"])
        self.assertEqual(created_pin.description, data["description"])
        self.assertEqual(created_pin.author.username, self.test_username)

        pin_image_file_key_s3 = f"pins/pin_{created_pin.unique_id}.jpg"

        self.assertEqual(
            created_pin.image_url, compute_file_url_s3(pin_image_file_key_s3)
        )

        self.check_file_in_s3(pin_image_file_key_s3, self.pin_image_file_content)

    def test_create_pin_s3_upload_fails(self):
        data = {
            "title": "Title",
            "description": "Description",
            "image_file": self.pin_image_file,
        }

        with mock.patch("boto3.client") as mock_s3_client:
            # Simulate upload failure:
            mock_s3_client.return_value.upload_fileobj.side_effect = Exception(
                "S3 upload failed"
            )

            response = self.client.post(
                "/api/create-pin/",
                data,
                format="multipart",
            )

            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            response_data = response.json()
            self.assertEqual(
                response_data["errors"], [{"code": ERROR_CODE_PIN_CREATION_FAILED}]
            )

            self.assertEqual(Pin.objects.count(), 0)

    def test_create_pin_missing_file(self):
        data = {"title": "Title", "description": "Description"}

        response = self.client.post("/api/create-pin/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()
        self.assertEqual(
            response_data["errors"], [{"code": ERROR_CODE_MISSING_PIN_IMAGE_FILE}]
        )

        self.assertEqual(Pin.objects.count(), 0)
