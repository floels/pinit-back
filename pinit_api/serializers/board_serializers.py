from rest_framework import serializers
from ..models import Board, PinInBoard

NUMBER_FIRST_IMAGES = 3


class BoardReadSerializer(serializers.ModelSerializer):
    first_image_urls = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["unique_id", "title", "first_image_urls"]

    def get_first_image_urls(self, obj):
        oldest_pins = PinInBoard.objects.filter(board=obj).order_by("last_saved_at")[
            :NUMBER_FIRST_IMAGES
        ]

        return [pin_in_board.pin.image_url for pin_in_board in oldest_pins]
