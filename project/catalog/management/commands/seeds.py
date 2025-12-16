from django.core.management.base import BaseCommand

from ._seeds_data import CATEGORIES, PRODUCTS
from ...models import Category, Product


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
        categories = [
            Category(
                **{
                    "name": c["name"],
                    "slug": c["slug"],
                }
            )
            for c in CATEGORIES
        ]
        Category.objects.bulk_create(categories)

    @staticmethod
    def bulk_insert_products() -> None:
        products = [
            Product(
                **{
                    "name": p["name"],
                    "slug": p["slug"],
                    "price": p["price"],
                    "sale": p["sale"],
                    "in_stock": p["in_stock"],
                    "image": p["image"],
                }
            )
            for p in PRODUCTS
        ]
        Product.objects.bulk_create(products)

    @staticmethod
    def bulk_insert_category_product() -> None:
        categories_products = [
            Product.categories.through(
                product_id=p.id,
                category_id=[
                    p_fake["category_id"] for p_fake in PRODUCTS if p_fake["id"] == p.id
                ][0],
            )
            for p in Product.objects.all()
        ]
        Product.categories.through.objects.bulk_create(categories_products)

    def seed_db(self):
        try:
            self.bulk_insert_categories()
            self.bulk_insert_products()
            self.bulk_insert_category_product()
        except Exception as e:
            print(f"Error during bulk insert: {e}")
