from django.contrib.auth import get_user_model
from django.db import models

from catalog.models import Product
from shop.models import TimeStampedModel

UserModel = get_user_model()


class Comment(TimeStampedModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="comments/", null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment - {self.id}"

    @property
    def img(self):
        if self.image:
            return self.image.url

        return None
