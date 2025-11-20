import os

import psycopg2
from django.core.management.base import BaseCommand
from psycopg2._psycopg import cursor
from psycopg2.extras import execute_values

from ._seeds_data import CATEGORIES, PRODUCTS


# Command
class Command(BaseCommand):
    help = "This command seeds DB with mock data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding DB with mock data...")

        self.seed_db()

        self.stdout.write("DB was successfully seeded!")

    # Helper functions
    @staticmethod
    def bulk_insert(cur: cursor, sql: str, data: list[tuple]) -> None:
        execute_values(cur, sql, data)

    def bulk_insert_categories(self, cur: cursor) -> None:
        sql = "INSERT INTO catalog_category (name, slug) VALUES %s"
        data = [(c["name"], c["slug"]) for c in CATEGORIES]

        self.bulk_insert(cur, sql, data)

    def bulk_insert_products(self, cur: cursor) -> None:
        sql = "INSERT INTO catalog_product (name, slug, image, price, sale, in_stock) VALUES %s"
        data = [
            (
                c["name"],
                c["slug"],
                c["image"],
                c["price"],
                c["sale"],
                c["in_stock"],
            )
            for c in PRODUCTS
        ]

        self.bulk_insert(cur, sql, data)

    def bulk_insert_category_product(self, cur: cursor) -> None:
        sql = (
            "INSERT INTO catalog_category_products (category_id, product_id) VALUES %s"
        )
        data = [
            (
                c["category_id"],
                c["id"],
            )
            for c in PRODUCTS
        ]

        self.bulk_insert(cur, sql, data)

    def seed_db(self):
        try:
            with psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
            ) as conn:
                with conn.cursor() as curs:
                    self.bulk_insert_categories(curs)
                    self.bulk_insert_products(curs)
                    self.bulk_insert_category_product(curs)

                conn.commit()
        except psycopg2.Error as e:
            print(f"Error during bulk insert: {e}")
