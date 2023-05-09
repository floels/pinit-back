from django.test import TestCase
from rest_framework import status
from ..models import User
from ..utils.constants import (
    ERROR_CODE_INVALID_EMAIL,
    ERROR_CODE_INVALID_PASSWORD,
    ERROR_CODE_EMAIL_ALREADY_SIGNED_UP,
    ERROR_CODE_INVALID_BIRTHDATE,
)


class SignupTests(TestCase):
    def setUp(self):
        self.existing_user_email = "existing.user@example.com"
        self.existing_user_password = "Pa$$wOrd_existing_user"

        self.user = User.objects.create_user(
            email=self.existing_user_email,
            password=self.existing_user_password,
        )

        # Existing users with "newuser", "newuser1" and "newuser2" user name
        # (to test suffix incrementation in test_signup_happy_case):
        User.objects.create_user(
            email="username-newuser@example.com",
            password=self.existing_user_password,
            username="newuser",
        )
        User.objects.create_user(
            email="username-newuser1@example.com",
            password=self.existing_user_password,
            username="newuser1",
        )
        User.objects.create_user(
            email="username-newuser2@example.com",
            password=self.existing_user_password,
            username="newuser2",
        )

        self.number_existing_users = 4

    def test_signup_happy_case(self):
        data = {
            "email": "new.user@example.com",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-01-01",
        }
        response = self.client.post("/api/signup/", data, format="json")

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
        self.assertEqual(new_user.email, "new.user@example.com")
        self.assertEqual(str(new_user.birthdate), "1970-01-01")
        self.assertEqual(new_user.username, "newuser3")
        self.assertEqual(new_user.initial, "N")
        self.assertEqual(new_user.first_name, "New")
        self.assertEqual(new_user.last_name, "User")

    def test_signup_invalid_email(self):
        data = {
            "email": "new.user@example.",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-01-01",
        }
        response = self.client.post("/api/signup/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_INVALID_EMAIL}],
        )

        # Check no user was created
        self.assertEqual(User.objects.count(), self.number_existing_users)

    def test_signup_blank_email(self):
        data = {
            "email": "",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-01-01",
        }
        response = self.client.post("/api/signup/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_INVALID_EMAIL}],
        )

        # Check no user was created
        self.assertEqual(User.objects.count(), self.number_existing_users)

    def test_signup_email_already_signed_up(self):
        data = {
            "email": self.existing_user_email,
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-01-01",
        }
        response = self.client.post("/api/signup/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_EMAIL_ALREADY_SIGNED_UP}],
        )

        # Check no user was created
        self.assertEqual(User.objects.count(), self.number_existing_users)

    def test_signup_invalid_password(self):
        data = {
            "email": "new.user@example.com",
            "password": "abc",
            "birthdate": "1970-01-01",
        }
        response = self.client.post("/api/signup/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_INVALID_PASSWORD}],
        )

        # Check no user was created
        self.assertEqual(User.objects.count(), self.number_existing_users)

    def test_signup_blank_password(self):
        data = {
            "email": "new.user@example.com",
            "password": "",
            "birthdate": "1970-01-01",
        }
        response = self.client.post("/api/signup/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_INVALID_PASSWORD}],
        )

        # Check no user was created
        self.assertEqual(User.objects.count(), self.number_existing_users)

    def test_signup_invalid_birthdate(self):
        data = {
            "email": "new.user@example.com",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "1970-13-01",
        }
        response = self.client.post("/api/signup/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_INVALID_BIRTHDATE}],
        )

        # Check no user was created
        self.assertEqual(User.objects.count(), self.number_existing_users)

    def test_signup_blank_birthdate(self):
        data = {
            "email": "new.user@example.com",
            "password": "Pa$$w0rd_new_user",
            "birthdate": "",
        }
        response = self.client.post("/api/signup/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["errors"],
            [{"code": ERROR_CODE_INVALID_BIRTHDATE}],
        )

        # Check no user was created
        self.assertEqual(User.objects.count(), self.number_existing_users)
