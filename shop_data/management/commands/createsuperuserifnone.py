from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from loguru import logger

from shop_bot import settings


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument("--username", required=False, help="Admin's username")
        parser.add_argument("--email", required=False, help="Admin's email")
        parser.add_argument("--password", required=False, help="Admin's password")

    def handle(self, *args, **options):
        username = options["username"] or settings.DJANGO_SUPERUSER_USERNAME
        email = options["email"] or settings.DJANGO_SUPERUSER_EMAIL
        password = options["password"] or settings.DJANGO_SUPERUSER_PASSWORD

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username, email=email, password=password
            )
            logger.info(f"Superuser '{username}' has been created.")
