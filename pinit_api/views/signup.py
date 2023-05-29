from rest_framework import generics
from ..serializers import UserCreateSerializer
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from ..doc.signup_doc import SWAGGER_SCHEMAS
from ..utils import compute_username_candidate_from_email
from ..models import Account


class SignupView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def compute_default_account_username_from_email(self, email):
        username_candidate = compute_username_candidate_from_email

        return self.compute_default_account_username_from_candidate(username_candidate)

    def compute_default_account_username_from_candidate(self, username_candidate):
        if Account.objects.filter(username=username_candidate):
            return self.compute_first_available_username_from_candidate(
                username_candidate
            )

        # No account exists with this candidate
        return username_candidate

    def compute_first_available_username_from_candidate(self, username_candidate):
        accounts_with_username_starting_with_candidate = Account.objects.filter(
            username__startswith=username_candidate
        )

        usernames_starting_with_candidate = [
            account.username
            for account in accounts_with_username_starting_with_candidate
        ]

        # Starting from 1, we increment a suffix until the resulting username does not already exist:
        suffix = 1

        while True:
            username = f"{username_candidate}{suffix}"

            if username not in usernames_starting_with_candidate:
                break

            suffix += 1

        return username

    @swagger_auto_schema(**SWAGGER_SCHEMAS["SignupView"])
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh_token = RefreshToken.for_user(user)

            return JsonResponse(
                {
                    "access_token": str(refresh_token.access_token),
                    "refresh_token": str(refresh_token),
                }
            )

        flattened_errors = []

        for field_errors in serializer.errors.values():
            for error in field_errors:
                flattened_errors.append({"code": str(error)})

        return JsonResponse({"errors": flattened_errors}, status=400)
