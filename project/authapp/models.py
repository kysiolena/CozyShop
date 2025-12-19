from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique

    # This makes email the unique identifier
    USERNAME_FIELD = "email"
    # 'email' is removed from here and put in USERNAME_FIELD
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
