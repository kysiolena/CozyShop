import os

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            UserModel.objects.get(email=os.getenv("ADMIN_EMAIL"))

            self.stdout.write("User already exists")
        except UserModel.DoesNotExist:
            # Create User Admin
            user = UserModel.objects.create_user(
                email=os.getenv("ADMIN_EMAIL"),
                username=os.getenv("ADMIN_USERNAME"),
                password=os.getenv("ADMIN_PASSWORD"),
            )

            # Grant admin privileges
            user.is_staff = True
            user.is_superuser = True

            user.save()

            self.stdout.write("Successfully created admin user")
