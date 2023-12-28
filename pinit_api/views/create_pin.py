import os
import boto3
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from pinit_api.models import Pin
from pinit_api.utils.constants import (
    ERROR_CODE_PIN_CREATION_FAILED,
    ERROR_CODE_MISSING_PIN_IMAGE_FILE,
)
from pinit_api.tests.testing_utils import AccountFactory
from pinit_api.serializers.pin_serializers import PinBasicReadSerializer


def upload_file_to_s3(file, file_name):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.S3_PINS_BUCKET_UPLOADER_ACCESS_KEY_ID,
        aws_secret_access_key=settings.S3_PINS_BUCKET_UPLOADER_SECRET_ACCESS_KEY,
    )

    s3_client.upload_fileobj(file, settings.S3_PINS_BUCKET_NAME, file_name)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_pin(request):
    title = request.data.get("title")
    description = request.data.get("description")
    image_file = request.FILES.get("image_file")

    if not image_file:
        response_data = {"errors": [{"code": ERROR_CODE_MISSING_PIN_IMAGE_FILE}]}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # TODO: retrieve account of authenticated user, based on request header

    pin = Pin.objects.create(
        title=title, description=description, author=AccountFactory()
    )  # TODO: save with owner account

    _, file_extension = os.path.splitext(image_file.name)
    file_name = f"pins/pin_{pin.unique_id}{file_extension}"

    try:
        upload_file_to_s3(image_file, file_name)
    except:
        pin.delete()
        response_data = {"errors": [{"code": ERROR_CODE_PIN_CREATION_FAILED}]}
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    pin.image_url = f"https://{settings.S3_PINS_BUCKET_URL}/{file_name}"
    pin.save()

    pin_serializer = PinBasicReadSerializer(pin)

    return Response(pin_serializer.data, status=status.HTTP_201_CREATED)
