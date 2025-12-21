from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

from shop.models import TimeStampedModel


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique

    # This makes email the unique identifier
    USERNAME_FIELD = "email"
    # 'email' is removed from here and put in USERNAME_FIELD
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


UserModel = get_user_model()


class Profile(TimeStampedModel):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


# Create a user Profile by default when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()


# Automate the profile thing
post_save.connect(create_profile, sender=UserModel)
