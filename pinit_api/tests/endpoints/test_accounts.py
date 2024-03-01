from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..testing_utils import AccountFactory, BoardFactory


class AccountsTestCase(APITestCase):
    def setUp(self):
        self.account = AccountFactory()

        self.client = APIClient()

        self.user = self.account.owner

    def check_response_data_against_account_public_details(
        self, response_data, account
    ):
        self.assertEqual(response_data["username"], account.username)
        self.assertEqual(response_data["display_name"], account.display_name)
        self.assertEqual(
            response_data["profile_picture_url"], account.profile_picture_url
        )
        self.assertEqual(
            response_data["background_picture_url"], account.background_picture_url
        )
        self.assertEqual(response_data["description"], account.description)
        self.assertEqual(
            response_data["boards"],
            [
                {
                    "unique_id": board.unique_id,
                    "title": board.title,
                    "cover_picture_url": board.cover_picture_url,
                }
                for board in account.boards.order_by(
                    "-last_pin_added_at", "-created_at"
                )
            ],
        )


class GetAccountPublicDetailsTests(AccountsTestCase):
    def setUp(self):
        super().setUp()

        self.board = BoardFactory(author=self.account)

    def test_get_account_details_happy_path(self):
        response = self.client.get(f"/api/accounts/{self.account.username}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.check_response_data_against_account_public_details(
            response_data, self.account
        )

    def test_get_account_details_not_found(self):
        response = self.client.get("/api/account/non_existing_username/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetMyAccountDetailsTests(AccountsTestCase):
    def setUp(self):
        super().setUp()

        self.boardLeastRecent = BoardFactory(author=self.account)
        self.boardMostRecent = BoardFactory(author=self.account)

        self.boardLeastRecent.last_pin_added_at = timezone.now() - timedelta(days=2)
        self.boardLeastRecent.save()

        self.boardMostRecent.last_pin_added_at = timezone.now() - timedelta(days=1)
        self.boardMostRecent.save()

    def check_response_data_against_account_private_details(
        self, response_data, account
    ):
        self.check_response_data_against_account_public_details(response_data, account)

        self.assertEqual(response_data["type"], account.type)

        self.assertEqual(response_data["initial"], account.initial)

    def test_get_my_account_details_happy_path(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(f"/api/accounts/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.check_response_data_against_account_private_details(
            response_data, self.account
        )

    def test_get_my_account_details_unauthenticated(self):
        response = self.client.get(f"/api/accounts/me/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
