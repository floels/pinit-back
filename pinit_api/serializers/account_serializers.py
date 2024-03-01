from rest_framework import serializers
from ..models import Account, Board
from ..serializers.board_serializers import BoardReadSerializer


class AccountBaseReadSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            "username",
            "display_name",
            "profile_picture_url",
        )

    def get_display_name(self, obj):
        return obj.display_name


class AccountWithBoardsReadSerializer(AccountBaseReadSerializer):
    boards = serializers.SerializerMethodField()

    class Meta(AccountBaseReadSerializer.Meta):
        fields = AccountBaseReadSerializer.Meta.fields + ("boards",)

    def get_boards(self, obj):
        ordered_boards = Board.objects.filter(author=obj).order_by(
            "-last_pin_added_at", "-created_at"
        )
        return BoardReadSerializer(ordered_boards, many=True).data


class AccountWithPublicDetailsReadSerializer(AccountWithBoardsReadSerializer):
    class Meta(AccountWithBoardsReadSerializer.Meta):
        fields = AccountWithBoardsReadSerializer.Meta.fields + (
            "background_picture_url",
            "description",
        )


class AccountWithPrivateDetailsReadSerializer(AccountWithPublicDetailsReadSerializer):
    class Meta(AccountWithPublicDetailsReadSerializer.Meta):
        fields = AccountWithPublicDetailsReadSerializer.Meta.fields + (
            "type",
            "initial",
        )
