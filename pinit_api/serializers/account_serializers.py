from rest_framework import serializers
from ..models import Account


class AccountBaseSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    def get_display_name(self, obj):
        return obj.display_name


class AccountSimpleReadSerializer(AccountBaseSerializer):
    class Meta:
        model = Account
        fields = (
            "username",
            "type",
            "initial",
            "display_name",
            "profile_picture_url",
        )


class AccountWithPublicDetailsReadSerializer(AccountBaseSerializer):
    class Meta:
        model = Account
        fields = (
            "username",
            "type",
            "display_name",
            "profile_picture_url",
            "background_picture_url",
            "description",
        )
