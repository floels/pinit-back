import os
import random
import json
from django.conf import settings
from django.core.management import BaseCommand
from pinit_api.models import Pin
from pinit_api.tests.testing_utils import PinFactory
from faker import Faker


class Command(BaseCommand):
    help = "Generates up to 10,000 random pins and the corresponding authors, using the list of unique image URLs in fixtures."

    def handle(self, *args, **options):
        self.generate_pins()

    def generate_pins(self):
        fake = Faker()

        file_path = os.path.join(
            settings.BASE_DIR, "..", "pinit_api", "fixtures", "unique_image_urls.json"
        )

        with open(file_path, "r") as unique_image_urls_file:
            unique_image_urls = json.load(unique_image_urls_file)

            while Pin.objects.count() < 10000:
                PinFactory.create(
                    image_url=random.choice(unique_image_urls),
                )

        self.stdout.write(self.style.SUCCESS("Successfully created pins"))
