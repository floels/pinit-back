import os
import json
import random
from django.conf import settings
from django.core.management import BaseCommand
from pinit_api.models import Account


class Command(BaseCommand):
    help = "Sets a random background picture on all accounts with a username of the form 'user_XXX', where 'XXX' is a number lower than 50_000_000, using the list of picture URLs in fixtures."

    def handle(self, *args, **options):
        self.set_background_picture_urls()

    def set_background_picture_urls(self):
        file_path = os.path.join(
            settings.BASE_DIR,
            "..",
            "pinit_api",
            "fixtures",
            "profile_background_picture_urls.json",
        )

        number_accounts_updated = 0

        with open(file_path, "r") as picture_urls_file:
            picture_urls = json.load(picture_urls_file)

            for account in Account.objects.filter(background_picture_url__isnull=True):
                if (
                    account.username.startswith("user_")
                    and account.username[5:].isdigit()
                ):
                    account_number = int(account.username[5:])
                    if (
                        account_number < 50_000_000
                    ):  # statistically, half of the 'user_XXX' acccounts, since 'XXX' has 8 digits
                        random_url = random.choice(picture_urls)

                        account.background_picture_url = random_url

                        account.save()

                        number_accounts_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully set {number_accounts_updated} profile background pictures."
            )
        )
