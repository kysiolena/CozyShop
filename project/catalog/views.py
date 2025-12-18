from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.views.generic import TemplateView

from catalog.forms import ProductReviewForm
from catalog.models import Product, Category, ProductReview
from shop.views import BaseContextMixin


class ProductMixin:
    @staticmethod
    def get_products_rows(products_set: QuerySet, products_in_row=3):
        paginator = Paginator(products_set, products_in_row)

        rows = [
            paginator.page(page_number).object_list
            for page_number in paginator.page_range
        ]

        return rows


class CatalogView(BaseContextMixin, ProductMixin, TemplateView):
    template_name = "catalog/index.html"
    page_name = "Catalog"

    def get_context_data(self, **kwargs):
        # Products
        products_set = Product.objects.all()
        # Products by rows
        rows = self.get_products_rows(products_set)

        # Categories
        categories_set = Category.objects.all()

        context = super().get_context_data(**kwargs)

        context["rows"] = rows
        context["categories"] = categories_set

        return context


class CategoryView(BaseContextMixin, ProductMixin, TemplateView):
    template_name = "catalog/category.html"

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug")

        # Category
        category = Category.objects.get(slug=slug)

        self.page_name = category.name

        # Products by rows
        rows = self.get_products_rows(category.products.all())

        # Categories
        categories_set = Category.objects.all()

        context = super().get_context_data(**kwargs)

        context["category"] = category
        context["rows"] = rows
        context["categories"] = categories_set

        return context


class ProductView(BaseContextMixin, TemplateView):
    template_name = "catalog/product.html"

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug")

        # Product
        product = Product.objects.get(slug=slug)

        self.page_name = product.name

        # Product Categories
        categories_set = product.categories.all()

        # Product Reviews
        reviews_set = product.reviews.all()

        context = super().get_context_data(**kwargs)

        context["product"] = product
        context["categories"] = categories_set
        context["reviews"] = reviews_set

        return context


class ProductReviewView(BaseContextMixin, TemplateView):
    template_name = "catalog/product-review.html"

    def get_context_data(self, **kwargs):
        product_slug = self.kwargs.get("slug")
        review_id = self.kwargs.get("review_id")

        # Product
        product = Product.objects.get(slug=product_slug)

        self.page_name = f"Review for «{product.name}»"

        # Product Review
        product_review = ProductReview.objects.get(id=review_id) if review_id else None

        form = ProductReviewForm(product_review)

        context = super().get_context_data(**kwargs)

        context["product_slug"] = product.slug
        context["review"] = product_review
        context["form"] = form

        return context

    def post(self, request, *args, **kwargs):
        product_slug = self.kwargs.get("slug")
        review_id = self.kwargs.get("review_id")

        # Product
        product = Product.objects.get(slug=product_slug)

        self.page_name = f"Review for «{product.name}»"

        # Product Review
        product_review = ProductReview.objects.get(id=review_id) if review_id else None

        form = ProductReviewForm(request.POST or None, request.FILES or None)

        context = super().get_context_data(**kwargs)

        if form.is_valid():
            form.save(product_slug)
            context["form"] = ProductReviewForm()
            context["message"] = "Your review was successfully created!"
        else:
            context["form"] = form

        context["product_slug"] = product_slug
        context["review"] = product_review

        return self.render_to_response(context)
