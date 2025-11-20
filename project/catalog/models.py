from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    price = models.FloatField()
    sale = models.FloatField(default=0, help_text="The value must be between 0 and 1")
    in_stock = models.BooleanField(null=True)
    description = models.TextField(null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    products = models.ManyToManyField(
        Product,
        related_name="categories",
    )
