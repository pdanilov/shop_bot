import yaml
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        with open(options["path"], mode="r") as file:
            items = yaml.load(file, Loader=yaml.FullLoader)

        for item in items:
            model = apps.get_model(item["model"])
            model.objects.get_or_create(pk=item["pk"], **item["fields"])
