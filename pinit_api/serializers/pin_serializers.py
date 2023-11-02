from rest_framework import serializers

from ..models import Account, Pin
from .account_serializers import AccountBaseSerializer


class AccountReadSerializer(AccountBaseSerializer):
    class Meta:
        model = Account
        fields = ("username", "display_name", "profile_picture_url")


class PinWithAuthorReadSerializer(serializers.ModelSerializer):
    author = AccountReadSerializer(read_only=True)

    class Meta:
        model = Pin
        fields = ["unique_id", "image_url", "title", "description", "author"]
