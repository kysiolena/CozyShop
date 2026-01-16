import random

from django.conf import settings
from django.core.management.base import BaseCommand

from catalog.management.commands._seeds_data import CATEGORIES, PRODUCTS
from catalog.models import Category, Product


# Command
class Command(BaseCommand):
    help = "This command seeds DB with mock data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding DB with mock data...")

        self.seed_db()

        self.stdout.write("DB was successfully seeded!")

    # Helper functions
    @staticmethod
    def bulk_insert_categories() -> None:
        if Category.objects.count() == 0:
            categories = [
                Category(
                    **{
                        "name": c["name"],
                        "slug": c["slug"],
                        "image": c["image"] if random.randint(0, 1) else None,
                        "description": (
                            c["description"] if random.randint(0, 1) else None
                        ),
                    }
                )
                for index, c in enumerate(CATEGORIES)
            ]

            Category.objects.bulk_create(categories)

    @staticmethod
    def bulk_insert_products() -> None:
        if Product.objects.count() == 0:
            products = [
                Product(
                    **{
                        "name": p["name"],
                        "slug": p["slug"],
                        "price": p["price"],
                        "sale": p["sale"],
                        "in_stock": p["in_stock"],
                        "image": p["image"],
                        "description": p.get("description", None),
                    }
                )
                for p in PRODUCTS
            ]
            Product.objects.bulk_create(products)

    @staticmethod
    def bulk_insert_category_product() -> None:
        if Product.categories.through.objects.count() == 0:
            products_ids = [p["id"] for p in Product.objects.all().values("id")]
            categories_ids = [c["id"] for c in Category.objects.all().values("id")]

            categories_products = [
                Product.categories.through(
                    product_id=p,
                    category_id=random.choice(categories_ids),
                )
                for p in products_ids
            ]

            Product.categories.through.objects.bulk_create(categories_products)

    def seed_db(self):
        try:
            self.bulk_insert_categories()
            self.bulk_insert_products()
            self.bulk_insert_category_product()
        except Exception as e:
            print(f"Error during bulk insert: {e}")
