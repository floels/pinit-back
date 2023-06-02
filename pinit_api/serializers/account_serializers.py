from rest_framework import serializers
from ..models import Account


class AccountBaseSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    def get_display_name(self, obj):
        if obj.type == "personal":
            return f"{obj.first_name} {obj.last_name}"

        return obj.business_name


class AccountWithOwnerEmailReadSerializer(AccountBaseSerializer):
    owner_email = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ("username", "type", "initial", "display_name", "owner_email")

    def get_owner_email(self, obj):
        return obj.owner.email
