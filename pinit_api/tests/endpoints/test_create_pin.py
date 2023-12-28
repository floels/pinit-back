import boto3
from io import BytesIO
from moto import mock_s3
from django.conf import settings
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from ..testing_utils import AccountFactory
from pinit_api.models import Pin


S3_BUCKET_NAME = settings.S3_PINS_BUCKET_NAME


# Inspired by https://docs.getmoto.org/en/latest/docs/getting_started.html#class-decorator
@mock_s3
class CreatePinTests(APITestCase):
    def setUp(self):
        self.test_account = AccountFactory()

        self.test_user = self.test_account.owner

        self.client = APIClient()
        tokens_pair = RefreshToken.for_user(self.test_user)
        access_token = str(tokens_pair.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        s3_resource = boto3.resource("s3")
        bucket = s3_resource.Bucket(S3_BUCKET_NAME)
        bucket.create()

    def check_file_in_s3(self, expected_key, expected_content):
        s3 = boto3.resource("s3")

        object = s3.Object(S3_BUCKET_NAME, expected_key)

        file_content = object.get()["Body"].read()

        self.assertEqual(file_content, expected_content)

    def test_create_pin_happy_path(self):
        pin_image_file_content = b"pin image data"
        pin_image_file = BytesIO(pin_image_file_content)
        pin_image_file.name = "pin_image_file.jpg"

        data = {"title": "", "description": "", "image_file": pin_image_file}

        response = self.client.post("/api/create-pin/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Pin.objects.count(), 1)

        created_pin = Pin.objects.get()

        pin_image_file_key_s3 = f"pins/pin_{created_pin.unique_id}.jpg"

        self.check_file_in_s3(pin_image_file_key_s3, pin_image_file_content)

    def test_create_pin_missing_file(self):
        data = {"title": "Title", "description": "Description"}

        response = self.client.post("/api/create-pin/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(Pin.objects.count(), 0)
