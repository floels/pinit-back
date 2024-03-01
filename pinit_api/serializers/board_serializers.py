from rest_framework import serializers
from ..models import Board


class BoardReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["unique_id", "title", "cover_picture_url"]
