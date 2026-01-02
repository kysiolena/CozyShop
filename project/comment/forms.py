from django import forms

from comment.models import Comment
from shop.forms import BootstrapFieldsMixin


class CommentCreateForm(BootstrapFieldsMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            "image",
            "body",
        )
        exclude = (
            "user",
            "product",
        )
