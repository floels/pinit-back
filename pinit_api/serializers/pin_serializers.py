from rest_framework import serializers
from ..models import Pin


class PinWithAuthorReadSerializer(serializers.ModelSerializer):
    relationships = serializers.SerializerMethodField()

    class Meta:
        model = Pin
        fields = ["id"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["type"] = "pin"
        representation["attributes"] = {
            "title": instance.title,
            "image_url": instance.image_url,
        }
        representation["relationships"] = {
            "author": {
                "data": {
                    "type": "user",
                    "id": instance.author.username,
                }
            }
        }

    def get_included(self, obj):
        return {
            "type": "user",
            "id": obj.author.username,
            "attributes": {
                "first_name": obj.author.first_name,
                "last_name": obj.author.last_name,
            },
        }
