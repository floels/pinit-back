from rest_framework import serializers
from ..models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["unique_id", "title", "cover_image_url"]
