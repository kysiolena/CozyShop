from django.views.generic import ListView, DetailView

from catalog.models import Product, Category
from shop.views import BaseContextMixin


class CategoriesContextMixin:

    def get_context_data(self, **kwargs):
        # Categories
        categories = Category.objects.all()

        context = super().get_context_data(**kwargs)

        context["categories"] = categories

        return context


class CatalogView(BaseContextMixin, CategoriesContextMixin, ListView):
    template_name = "catalog/index.html"
    page_name = "Catalog"
    model = Product
    paginate_by = 9
    ordering = "-created_at"


class CategoryView(BaseContextMixin, CategoriesContextMixin, ListView):
    template_name = "catalog/category.html"
    model = Product
    paginate_by = 9

    def get_queryset(self):
        # Get Category slug
        slug = self.kwargs.get("slug")

        return (
            super()
            .get_queryset()
            .filter(categories__slug__contains=slug)
            .order_by("-created_at")
        )

    def get_context_data(self, **kwargs):
        # Get Category slug
        slug = self.kwargs.get("slug")

        # Category
        category = Category.objects.get(slug=slug)

        # Set Page Name
        self.page_name = category.name

        context = super().get_context_data(**kwargs)

        context["category"] = category

        return context


class ProductView(BaseContextMixin, DetailView):
    template_name = "catalog/product.html"
    model = Product
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("categories")
