from django.views.generic import TemplateView

from .data import PRODUCTS, CATEGORIES


class CatalogView(TemplateView):
    template_name = "catalog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        chunk_size = 3
        rows = [
            PRODUCTS[i : i + chunk_size] for i in range(0, len(PRODUCTS), chunk_size)
        ]

        context["page_name"] = "Catalog"
        context["rows"] = rows
        context["categories"] = CATEGORIES

        return context


class ProductView(TemplateView):
    template_name = "catalog/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs["slug"]

        products = [p for p in PRODUCTS if p["slug"] == slug]
        product = products[0]

        context["page_name"] = product["name"]
        context["product"] = product

        return context


class CategoryView(TemplateView):
    template_name = "catalog/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs["slug"]

        categories = [c for c in CATEGORIES if c["slug"] == slug]
        category = categories[0]

        chunk_size = 3
        category_products = [p for p in PRODUCTS if p["category_id"] == category["id"]]
        rows = [
            category_products[i : i + chunk_size]
            for i in range(0, len(category_products), chunk_size)
        ]

        context["page_name"] = category["name"]
        context["category"] = category
        context["rows"] = rows
        context["categories"] = CATEGORIES

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
