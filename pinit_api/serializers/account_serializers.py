from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from ..models import Account


class AccountBaseSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    @extend_schema_field(str)  # Necessary to avoid errors with drf_spectactular
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
