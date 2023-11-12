from rest_framework import serializers
from ..models import Account


class AccountBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

    display_name = serializers.SerializerMethodField()

    def get_display_name(self, obj):
        return obj.display_name


class AccountWithOwnerEmailReadSerializer(AccountBaseSerializer):
    owner_email = serializers.SerializerMethodField()

    class Meta:
        fields = ("username", "type", "initial", "display_name", "owner_email")

    def get_owner_email(self, obj):
        return obj.owner.email


class AccountWithPublicDetailsReadSerializer(AccountBaseSerializer):
    class Meta:
        fields = (
            "username",
            "type",
            "display_name",
            "profile_picture_url",
            "background_profile_url",
            "description",
        )
