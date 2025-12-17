from catalog.forms import ProductReviewForm
from catalog.models import Product, Category, ProductReview
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.views.generic import TemplateView


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


class CategoryView(TemplateView, ProductMixin):
    template_name = "catalog/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs.get("slug")

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


class ProductView(TemplateView):
    template_name = "catalog/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs.get("slug")

        # Product
        product = Product.objects.get(slug=slug)

        # Product Categories
        categories_set = product.categories.all()

        # Product Reviews
        reviews_set = product.reviews.all()

        context["page_name"] = product.name
        context["product"] = product
        context["categories"] = categories_set
        context["reviews"] = reviews_set

        return context


class ProductReviewView(TemplateView):
    template_name = "catalog/product-review.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product_slug = self.kwargs.get("slug")
        review_id = self.kwargs.get("review_id")

        # Product
        product = Product.objects.get(slug=product_slug)

        # Product Review
        product_review = ProductReview.objects.get(id=review_id) if review_id else None

        form = ProductReviewForm(product_review)

        context["page_name"] = f"Review for «{product.name}»"
        context["product_slug"] = product.slug
        context["review"] = product_review
        context["form"] = form

        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        product_slug = self.kwargs.get("slug")
        review_id = self.kwargs.get("review_id")

        # Product
        product = Product.objects.get(slug=product_slug)

        # Product Review
        product_review = ProductReview.objects.get(id=review_id) if review_id else None

        form = ProductReviewForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save(product_slug)
            context["form"] = ProductReviewForm()
            context["message"] = "Your review was successfully created!"
        else:
            context["form"] = form

        context["page_name"] = f"Review for «{product.name}»"
        context["product_slug"] = product_slug
        context["review"] = product_review

        return self.render_to_response(context)
