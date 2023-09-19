from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.db import transaction
from pinit_api.models import Pin
from pinit_api.tests.testing_utils import AccountFactory


DEFAULT_MAX_NUMBER_PINS_TO_CREATE = 1000


class Command(BaseCommand):
    help = "Import all pins found in the HTML file `pinterest.html`. Example of call: 'python manage.py import_pins_from_pinterest_html /absolute/path/to/pinterest.html'"

    def add_arguments(self, parser):
        parser.add_argument(
            "html_file_path",
            type=str,
            help="Path to the input HTML file (Pinterest homepage)",
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

        return soup.find_all("div", {"class": "zI7 iyn Hsu"})

    def create_pin_instances_from_pin_divs(self, pin_divs, max_number_pins_to_create):
        number_pins_created = 0

        for pin_div in pin_divs:
            if number_pins_created <= max_number_pins_to_create:
                try:
                    with transaction.atomic():
                        author = AccountFactory.create()
                        pin = self.get_pin_instance_from_pin_div(pin_div, author)
                        pin.save()
                    print(f"Successfully saved new pin with ID {pin.unique_id}")
                    number_pins_created += 1
                except Exception as e:
                    print(f"Error creating pin from dive: {e}")

    def get_pin_instance_from_pin_div(self, pin_div, author):
        img_tag = pin_div.find("img")
        image_url = img_tag["src"] if img_tag else None

        title = None

        title_container = pin_div.find(
            "div", {"data-test-id": "pointer-events-wrapper"}
        )
        if title_container:
            title_a = title_container.find(
                "a", {"class": "Wk9 xQ4 CCY S9z DUt iyn kVc agv LIa"}
            )
            if title_a and title_a.text:
                title = title_a.text.strip()

        return Pin(image_url=image_url, title=title, author=author)
