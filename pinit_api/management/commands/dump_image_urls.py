import json
from django.core.management import BaseCommand
from pinit_api.models import Pin
from django.core.serializers.json import DjangoJSONEncoder


class Command(BaseCommand):
    help = "Dump the list of unique image_url's from the Pin instances present in the database."

    def handle(self, *args, **options):
        self.dump_image_urls()

    def dump_image_urls(self):
        unique_image_urls = Pin.objects.values_list("image_url", flat=True).distinct()

        with open(
            "pinit_api/fixtures/unique_image_urls.json", "w", encoding="utf-8"
        ) as file:
            json.dump(
                list(unique_image_urls), file, ensure_ascii=False, cls=DjangoJSONEncoder
            )
