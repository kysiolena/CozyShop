from django.db.models import Q, Prefetch
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from catalog.models import Product, Category
from comment.models import Comment
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

    def get_breadcrumbs(self):
        # Define breadcrumbs as a list of (name, url) tuples
        return [("Home", reverse_lazy("shop_page")), (self.page_name, None)]


class CategoryView(BaseContextMixin, CategoriesContextMixin, ListView):
    template_name = "catalog/category.html"
    model = Product
    paginate_by = 9

    def get_breadcrumbs(self):
        # Define breadcrumbs as a list of (name, url) tuples
        return [
            ("Home", reverse_lazy("shop_page")),
            ("Catalog", reverse_lazy("catalog_page")),
            (self.page_name, None),
        ]

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

    def get_breadcrumbs(self):
        # Define breadcrumbs as a list of (name, url) tuples
        return [
            ("Home", reverse_lazy("shop_page")),
            ("Catalog", reverse_lazy("catalog_page")),
            (self.page_name, None),
        ]

    def get_queryset(self):
        # Define a custom, filtered queryset for the related objects
        approved_comments = Comment.objects.filter(is_approved=True).prefetch_related(
            "user"
        )

        return (
            super()
            .get_queryset()
            .prefetch_related("categories")
            .prefetch_related(
                Prefetch(
                    "comment_set",
                    queryset=approved_comments,
                    to_attr="approved_comments",
                )
            )
        )

    def get_context_data(self, **kwargs):
        # Set Page Name
        self.page_name = self.object.name

        return super().get_context_data(**kwargs)


class SearchView(BaseContextMixin, ListView):
    template_name = "catalog/search.html"
    model = Product
    paginate_by = 12
    ordering = "-created_at"

    def get_breadcrumbs(self):
        # Define breadcrumbs as a list of (name, url) tuples
        return [
            ("Home", reverse_lazy("shop_page")),
            ("Catalog", reverse_lazy("catalog_page")),
            (self.page_name, None),
        ]

    def get_queryset(self):
        # Get search parameter
        search = self.request.GET.get("search") or ""

        # Set Page Name
        self.page_name = f"Search results for «{search}»"

        return (
            super()
            .get_queryset()
            .filter(Q(name__icontains=search) | Q(description__icontains=search))
            .order_by("-created_at")
        )
