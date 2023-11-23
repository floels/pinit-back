import os
import json
import random
from django.conf import settings
from django.core.management import BaseCommand
from pinit_api.models import Account


class Command(BaseCommand):
    help = "Sets a random profile picture to all accounts not having one, using the list of picture URLs in fixtures."

    def handle(self, *args, **options):
        self.set_profile_picture_urls()

    def set_profile_picture_urls(self):
        file_path = os.path.join(
            settings.BASE_DIR,
            "..",
            "pinit_api",
            "fixtures",
            "profile_picture_urls.json",
        )

        number_accounts_updated = 0

        with open(file_path, "r") as picture_urls_file:
            picture_urls = json.load(picture_urls_file)

            for account in Account.objects.filter(profile_picture_url__isnull=True):
                random_url = random.choice(picture_urls)

                account.profile_picture_url = random_url

                account.save()

                number_accounts_updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully set {number_accounts_updated} profile pictures."
            )
        )
