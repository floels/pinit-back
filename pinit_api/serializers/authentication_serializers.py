from rest_framework import serializers
from ..models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    birthdate = serializers.DateField(required=True)

    class Meta:
        model = User
        fields = ("email", "password", "birthdate")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            birthdate=validated_data["birthdate"],
        )
        return user
