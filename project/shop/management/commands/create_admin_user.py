from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

UserModel = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        ADMIN_DATA = {
            "username": "admin",
            "email": "cozyshop01122026@gmail.com",
            "password": "01162026",
        }

        try:
            UserModel.objects.get(email=ADMIN_DATA["email"])

            self.stdout.write("User already exists")
        except UserModel.DoesNotExist:
            # Create User Admin
            user = UserModel.objects.create_user(**ADMIN_DATA)

            # Grant admin privileges
            user.is_staff = True
            user.is_superuser = True

            user.save()

            self.stdout.write("Successfully created admin user")
