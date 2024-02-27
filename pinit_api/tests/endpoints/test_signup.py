from django.test import TestCase
from rest_framework import status
from pinit_api.models import User, Account
from pinit_api.utils.constants import (
    ERROR_CODE_INVALID_EMAIL,
    ERROR_CODE_INVALID_PASSWORD,
)
from pinit_api.serializers.user_serializers import (
    ERROR_CODE_EMAIL_ALREADY_SIGNED_UP,
    ERROR_CODE_INVALID_BIRTHDATE,
)
from pinit_api.tests.testing_utils.factories import AccountFactory


class SignupTests(TestCase):
    def setUp(self):
        self.existing_user_email = "existing.user@example.com"
        self.existing_user_password = "Pa$$wOrd_existing_user"

        self.existing_user = User.objects.create_user(
            email=self.existing_user_email,
            password=self.existing_user_password,
        )

        # Existing accounts with "newuser", "newuser1" and "newuser2" usernames
        # (to test suffix incrementation logic):
        AccountFactory.create(custom_username="newuser")
        AccountFactory.create(custom_username="newuser1")
        AccountFactory.create(custom_username="newuser2")

        self.number_existing_accounts = Account.objects.count()
        self.number_existing_users = User.objects.count()

    def test_signup_happy_path(self):
        request_payload = {
            "email": "new.user@example.com",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-01-01",
        }
        response = self.client.post("/api/signup/", request_payload, format="json")

        # Check response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        access_token = response_data["access_token"]
        assert bool(access_token)
        refresh_token = response_data["refresh_token"]
        assert bool(refresh_token)

        # Check user was created with correct attributes
        self.assertEqual(User.objects.count(), self.number_existing_users + 1)
        new_user = User.objects.get(email="new.user@example.com")
        self.assertEqual(str(new_user.birthdate), "1970-01-01")

        # Check account was created with correct attributes
        self.assertEqual(Account.objects.count(), self.number_existing_accounts + 1)
        new_account = Account.objects.get(owner=new_user)
        self.assertEqual(new_account.type, "personal")
        self.assertEqual(new_account.username, "newuser3")
        self.assertEqual(new_account.initial, "N")
        self.assertEqual(new_account.first_name, "New")
        self.assertEqual(new_account.last_name, "User")
        self.assertEqual(new_account.business_name, None)

    def test_signup_invalid_email(self):
        request_payload = {
            "email": "new.user@example.",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-01-01",
        }

        response = self.client.post("/api/signup/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_INVALID_EMAIL}],
        )

        # Check no user and no account was created
        self.assertEqual(User.objects.count(), self.number_existing_users)
        self.assertEqual(Account.objects.count(), self.number_existing_accounts)

    def test_signup_blank_email(self):
        request_payload = {
            "email": "",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-01-01",
        }
        response = self.client.post("/api/signup/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_INVALID_EMAIL}],
        )

        # Check no user and no account was created
        self.assertEqual(User.objects.count(), self.number_existing_users)
        self.assertEqual(Account.objects.count(), self.number_existing_accounts)

    def test_signup_email_already_signed_up(self):
        request_payload = {
            "email": self.existing_user_email,
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-01-01",
        }

        response = self.client.post("/api/signup/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_EMAIL_ALREADY_SIGNED_UP}],
        )

        # Check no user and no account was created:
        self.assertEqual(User.objects.count(), self.number_existing_users)
        self.assertEqual(Account.objects.count(), self.number_existing_accounts)

    def test_signup_invalid_password(self):
        request_payload = {
            "email": "new.user@example.com",
            "password": "abc",
            "birthdate": "1970-01-01",
        }

        response = self.client.post("/api/signup/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_INVALID_PASSWORD}],
        )

        # Check no user and no account was created
        self.assertEqual(User.objects.count(), self.number_existing_users)
        self.assertEqual(Account.objects.count(), self.number_existing_accounts)

    def test_signup_blank_password(self):
        request_payload = {
            "email": "new.user@example.com",
            "password": "",
            "birthdate": "1970-01-01",
        }

        response = self.client.post("/api/signup/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_INVALID_PASSWORD}],
        )

        # Check no user and no account was created
        self.assertEqual(User.objects.count(), self.number_existing_users)
        self.assertEqual(Account.objects.count(), self.number_existing_accounts)

    def test_signup_invalid_birthdate(self):
        request_payload = {
            "email": "new.user@example.com",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-13-01",
        }

        response = self.client.post("/api/signup/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_INVALID_BIRTHDATE}],
        )

        # Check no user and no account was created
        self.assertEqual(User.objects.count(), self.number_existing_users)
        self.assertEqual(Account.objects.count(), self.number_existing_accounts)

    def test_signup_blank_birthdate(self):
        request_payload = {
            "email": "new.user@example.com",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "",
        }

        response = self.client.post("/api/signup/", request_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_data = response.json()

        self.assertEqual(
            response_data["errors"],
            [{"code": ERROR_CODE_INVALID_BIRTHDATE}],
        )

        # Check no user and no account was created
        self.assertEqual(User.objects.count(), self.number_existing_users)
        self.assertEqual(Account.objects.count(), self.number_existing_accounts)
