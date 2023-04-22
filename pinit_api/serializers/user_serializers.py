import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from ..models import User
from ..utils.constants import (
    ERROR_CODE_EMAIL_ALREADY_SIGNED_UP,
    ERROR_CODE_INVALID_EMAIL,
    ERROR_CODE_INVALID_PASSWORD,
    ERROR_CODE_INVALID_BIRTHDATE,
)


def get_initial_from_email(email):
    match_letter_before_at = re.search(r"([a-zA-Z])[^@]*@", email)

    # If no letter found before the '@', return "X" by default:
    return match_letter_before_at.group(1).upper() if match_letter_before_at else "X"


def get_first_last_name_from_email(email):
    local_part = email.split("@")[0]

    separators_pattern = r"[._-]"

    name_parts = re.split(separators_pattern, local_part)

    # Remove any non-alphabetical characters from the name parts
    name_parts = ["".join(re.findall(r"[a-zA-Z]+", part)) for part in name_parts]

    # Assume first name is in first place after splitting by separators,
    # and last second in second place:
    first_name = name_parts[0].capitalize() if len(name_parts) > 0 else ""
    last_name = name_parts[1].capitalize() if len(name_parts) > 1 else ""

    return first_name, last_name


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "initial", "first_name", "last_name"]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message=ERROR_CODE_EMAIL_ALREADY_SIGNED_UP
            )
        ],
        error_messages={
            "invalid": ERROR_CODE_INVALID_EMAIL,
            "required": ERROR_CODE_INVALID_EMAIL,
            "blank": ERROR_CODE_INVALID_EMAIL,
        },
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            "invalid": ERROR_CODE_INVALID_PASSWORD,
            "required": ERROR_CODE_INVALID_PASSWORD,
            "blank": ERROR_CODE_INVALID_PASSWORD,
        },
    )
    birthdate = serializers.DateField(
        required=True,
        error_messages={
            "invalid": ERROR_CODE_INVALID_BIRTHDATE,
            "required": ERROR_CODE_INVALID_BIRTHDATE,
            "blank": ERROR_CODE_INVALID_BIRTHDATE,
        },
    )

    class Meta:
        model = User
        fields = ("email", "password", "birthdate")

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError:
            raise serializers.ValidationError(ERROR_CODE_INVALID_PASSWORD)
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        first_name, last_name = get_first_last_name_from_email(email)

        user = User.objects.create_user(
            email=email,
            password=validated_data["password"],
            birthdate=validated_data["birthdate"],
            initial=get_initial_from_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        return user
