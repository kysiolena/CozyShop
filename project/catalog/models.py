from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def img(self):
        if self.image:
            return self.image.url
        else:
            return None


class Product(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    price = models.FloatField()
    sale = models.FloatField(default=0, help_text="The value must be between 0 and 1")
    in_stock = models.BooleanField(null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    categories = models.ManyToManyField(
        Category,
        related_name="products",
    )

    def __str__(self):
        return self.name

    @property
    def img(self):
        if self.image and self.image.url:
            return self.image if str(self.image).startswith("http") else self.image.url
        else:
            return f"{settings.STATIC_URL}catalog/images/image-not-found.png"

    @property
    def sale_price(self):
        if self.sale:
            return round(self.price - (self.price * self.sale), 2)
        else:
            return None


class ProductReview(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to="reviews/", null=True, blank=True)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )

    def __str__(self):
        return f"{self.id} - {self.product.name}"

    @property
    def img(self):
        if self.image:
            return self.image.url
        else:
            return None
