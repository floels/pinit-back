"""
A script to import all pins found in the HTML file `pinterest.html` (= source code of Pinterest.com homepage).
The `pinterest.html` should be saved in the same folder as this file.
The script will parse the HTML code with BeautifulSoup and create the corresponding instances in the database.
"""

from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from pinit_api.models import Pin
from pinit_api.tests.testing_utils import AccountFactory


DEFAULT_MAX_NUMBER_PINS_TO_CREATE = 300


class Command(BaseCommand):
    help = "Import all pins found in the HTML file `pinterest.html`"

    def add_arguments(self, parser):
        parser.add_argument(
            "html_file_path", type=str, help="Path to the input HTML file"
        )

    def handle(self, *args, **options):
        self.html_file_path = options["html_file_path"]
        self.create_pin_instances()

    def create_pin_instances(self):
        max_number_pins_to_create = input(
            f"Enter the maximum number of pins to create (default: {DEFAULT_MAX_NUMBER_PINS_TO_CREATE}): "
        )

        if not max_number_pins_to_create:
            max_number_pins_to_create = DEFAULT_MAX_NUMBER_PINS_TO_CREATE
        else:
            max_number_pins_to_create = int(max_number_pins_to_create)

        pin_divs = self.extract_pin_divs_from_html()

        self.create_pin_instances_from_pin_divs(pin_divs, max_number_pins_to_create)

    def extract_pin_divs_from_html(self):
        with open(self.html_file_path, "r") as file:
            html = file.read()

        soup = BeautifulSoup(html, "html.parser")

        return soup.find_all("div", {"data-test-id": "pin"})

    def create_pin_instances_from_pin_divs(self, pin_divs, max_number_pins_to_create):
        for index, pin_div in enumerate(pin_divs):
            if index >= max_number_pins_to_create:
                break

            pin = self.get_pin_instance_from_pin_div(pin_div)
            pin.save()

    def get_pin_instance_from_pin_div(self, pin_div):
        # Extract image URL
        image_div = pin_div.find("div", {"data-test-id": "non-story-pin-image"})
        image_url = image_div.find("img")["src"]

        # Extract pin description
        title_a = pin_div.find("a", {"class": "Wk9 xQ4 CCY S9z DUt iyn kVc agv LIa"})
        title = title_a.text.strip()
        if title == "":
            title = None

        author = AccountFactory.create()

        return Pin(image_url=image_url, title=title, author=author)
