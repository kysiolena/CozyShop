from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .data import PRODUCTS, CATEGORIES


def catalog_page(request: HttpRequest) -> HttpResponse:
    chunk_size = 3
    rows = [PRODUCTS[i : i + chunk_size] for i in range(0, len(PRODUCTS), chunk_size)]

    context = {"page_name": "Catalog", "rows": rows, "categories": CATEGORIES}
    return render(request=request, template_name="catalog/index.html", context=context)


def product_page(request: HttpRequest, slug) -> HttpResponse:
    products = [p for p in PRODUCTS if p["slug"] == slug]
    product = products[0]

    context = {"page_name": product["name"], "product": products[0]}
    return render(
        request=request, template_name="catalog/product.html", context=context
    )


def category_page(request: HttpRequest, slug) -> HttpResponse:
    categories = [c for c in CATEGORIES if c["slug"] == slug]
    category = categories[0]

    context = {"page_name": category["name"], "category": categories[0]}
    return render(
        request=request, template_name="catalog/category.html", context=context
    )
