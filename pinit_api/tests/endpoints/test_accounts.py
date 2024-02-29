from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from ..testing_utils import AccountFactory, BoardFactory


class GetAccountPublicDetailsTests(APITestCase):
    def setUp(self):
        self.account = AccountFactory()

        self.client = APIClient()

    def test_get_account_details_happy_path(self):
        response = self.client.get(f"/api/accounts/{self.account.username}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.assertEqual(response_data["username"], self.account.username)
        self.assertEqual(response_data["type"], self.account.type)
        self.assertEqual(response_data["display_name"], self.account.display_name)

        self.assertIn("profile_picture_url", response_data)
        self.assertIn("background_picture_url", response_data)
        self.assertIn("description", response_data)

    def test_get_account_details_not_found(self):
        response = self.client.get("/api/account/non_existing_username/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetMyAccountDetailsTests(APITestCase):
    def setUp(self):
        self.account = AccountFactory()

        self.boardLeastRecent = BoardFactory(author=self.account)
        self.boardMostRecent = BoardFactory(author=self.account)

        self.boardLeastRecent.last_pin_added_at = timezone.now() - timedelta(days=2)
        self.boardLeastRecent.save()

        self.boardMostRecent.last_pin_added_at = timezone.now() - timedelta(days=1)
        self.boardMostRecent.save()

        self.user = self.account.owner

    def check_response_data_against_account(self, response_data, account):
        self.assertEqual(response_data["username"], self.account.username)
        self.assertEqual(response_data["type"], self.account.type)
        self.assertEqual(response_data["display_name"], self.account.display_name)
        self.assertIn(
            response_data["profile_picture_url"], self.account.profile_picture_url
        )

        self.assertIn("background_picture_url", response_data)
        self.assertIn("description", response_data)

    def check_response_data_against_boards(self, response_data, boards):
        self.assertEqual(len(response_data["boards"]), len(boards))

        ordered_boards = sorted(
            boards, key=lambda board: board.last_pin_added_at, reverse=True
        )

        for i, board in enumerate(ordered_boards):
            self.assertEqual(response_data["boards"][i]["unique_id"], board.unique_id)
            self.assertEqual(response_data["boards"][i]["title"], board.title)
            self.assertEqual(
                response_data["boards"][i]["cover_picture_url"], board.cover_picture_url
            )

    def test_get_my_account_details_happy_path(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(f"/api/accounts/me/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()

        self.check_response_data_against_account(response_data, self.account)

        self.check_response_data_against_boards(
            response_data, [self.boardMostRecent, self.boardLeastRecent]
        )

    def test_get_my_account_details_unauthenticated(self):
        response = self.client.get(f"/api/accounts/me/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
