from django.views.generic import TemplateView


class BaseContextMixin:
    page_name = "Page Title"

    def get_context_data(self, **kwargs):
        # Check existing attr get_context_data in super()
        gcd = getattr(super(), "get_context_data")
        is_callable_gcd = callable(gcd)

        if gcd and is_callable_gcd:
            context = super().get_context_data(**kwargs)
        else:
            context = {}

        context["page_name"] = self.page_name

        return context


class ShopView(BaseContextMixin, TemplateView):
    template_name = "shop/index.html"
    page_name = "Home"
