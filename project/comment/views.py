from django.views.generic import CreateView

from shop.views import BaseContextMixin


class CommentCreateView(BaseContextMixin, CreateView):
    pass
