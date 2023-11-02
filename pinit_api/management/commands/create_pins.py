import os
import random
import json
from django.conf import settings
from django.core.management import BaseCommand
from pinit_api.models import Pin
from pinit_api.tests.testing_utils import PinFactory


class Command(BaseCommand):
    help = "Creates up to 10,000 pins and the corresponding authors, using the list of unique image URLs in fixtures."

    def handle(self, *args, **options):
        self.generate_pins()

    def generate_pins(self):
        file_path = os.path.join(
            settings.BASE_DIR, "..", "pinit_api", "fixtures", "pin_image_urls.json"
        )

        with open(file_path, "r") as image_urls_file:
            image_urls = json.load(image_urls_file)

            while Pin.objects.count() < 10000:
                PinFactory.create(
                    image_url=random.choice(image_urls),
                )

        self.stdout.write(self.style.SUCCESS("Successfully created pins"))
