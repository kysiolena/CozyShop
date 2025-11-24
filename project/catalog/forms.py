from django import forms

from .models import ProductReview, Product


class ProductReviewForm(forms.Form):
    name = forms.CharField()
    text = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()

    def save(self, product_slug: str):
        data = self.cleaned_data

        product_review = ProductReview(
            name=data["name"],
            text=data["text"],
            image=data["image"],
            product=Product.objects.get(slug=product_slug),
        )

        product_review.save()

        return product_review
