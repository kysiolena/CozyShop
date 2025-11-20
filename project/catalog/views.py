from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.views.generic import TemplateView

from .models import Product, Category


class ProductMixin:
    @staticmethod
    def get_products_rows(products_set: QuerySet, products_in_row=3):
        paginator = Paginator(products_set, products_in_row)

        rows = [
            paginator.page(page_number).object_list
            for page_number in paginator.page_range
        ]

        return rows


class CatalogView(TemplateView, ProductMixin):
    template_name = "catalog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Products
        products_set = Product.objects.all()
        # Products by rows
        rows = self.get_products_rows(products_set)

        # Categories
        categories_set = Category.objects.all()

        context["page_name"] = "Catalog"
        context["rows"] = rows
        context["categories"] = categories_set

        return context


class ProductView(TemplateView):
    template_name = "catalog/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs["slug"]

        # Product
        product = Product.objects.get(slug=slug)

        # Product Categories
        categories_set = product.categories.all()

        context["page_name"] = product.name
        context["product"] = product
        context["categories"] = categories_set

        return context


class CategoryView(TemplateView, ProductMixin):
    template_name = "catalog/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs["slug"]

        # Category
        category = Category.objects.get(slug=slug)

        # Products by rows
        rows = self.get_products_rows(category.products.all())

        # Categories
        categories_set = Category.objects.all()

        context["page_name"] = category.name
        context["category"] = category
        context["rows"] = rows
        context["categories"] = categories_set

        return context


# def catalog_page(request: HttpRequest) -> HttpResponse:
#     chunk_size = 3
#     rows = [PRODUCTS[i : i + chunk_size] for i in range(0, len(PRODUCTS), chunk_size)]
#
#     context = {"page_name": "Catalog", "rows": rows, "categories": CATEGORIES}
#     return render(request=request, template_name="catalog/index.html", context=context)


# def product_page(request: HttpRequest, slug) -> HttpResponse:
#     products = [p for p in PRODUCTS if p["slug"] == slug]
#     product = products[0]
#
#     context = {"page_name": product["name"], "product": product}
#     return render(
#         request=request, template_name="catalog/product.html", context=context
#     )


# def category_page(request: HttpRequest, slug) -> HttpResponse:
#     categories = [c for c in CATEGORIES if c["slug"] == slug]
#     category = categories[0]
#
#     chunk_size = 3
#     category_products = [p for p in PRODUCTS if p["category_id"] == category["id"]]
#     rows = [
#         category_products[i : i + chunk_size]
#         for i in range(0, len(category_products), chunk_size)
#     ]
#
#     context = {
#         "page_name": category["name"],
#         "category": category,
#         "rows": rows,
#         "categories": CATEGORIES,
#     }
#     return render(
#         request=request, template_name="catalog/category.html", context=context
#     )
