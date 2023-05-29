from rest_framework import serializers
from ..models import Account


class AccountJSONApiReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account

    def to_representation(self, instance):
        return self.to_json_api_representation(instance)

    def compute_display_name(self, instance):
        if instance.type == "personal":
            return f"{instance.first_name} {instance.last_name}"

        return instance.business_name

    def to_json_api_representation(self, instance):
        representation = super().to_representation(instance)

        representation["type"] = "accounts"
        representation["id"] = instance.username
        representation["attributes"] = {
            "username": instance.username,
            "type": instance.type,
            "display_name": self.compute_display_name(),
            "initial": instance.initial,
            "owner_email": instance.owner.email,
        }

        return representation
