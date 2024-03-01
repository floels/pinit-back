from rest_framework import serializers

from ..models import Pin
from .account_serializers import AccountBaseReadSerializer


class PinBasicReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = ["unique_id", "image_url", "title", "description"]


class PinWithAuthorReadSerializer(serializers.ModelSerializer):
    author = AccountBaseReadSerializer(read_only=True)

    class Meta:
        model = Pin
        fields = ["unique_id", "image_url", "title", "description", "author"]
