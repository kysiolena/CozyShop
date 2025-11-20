from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    price = models.FloatField()
    sale = models.DecimalField(default=0, decimal_places=2, max_digits=3)
    in_stock = models.BooleanField(null=True)
    description = models.TextField(null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    products = models.ManyToManyField(
        Product,
        related_name="categories",
    )
