from catalog.models import ProductReview, Product
from django import forms


class ProductReviewForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control mt-2"}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control mt-2"})
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control mt-2"})
    )

    def save(self, product_slug: str):
        data = self.cleaned_data

        product_review = ProductReview(
            name=data["name"],
            description=data["description"],
            image=data["image"],
            product=Product.objects.get(slug=product_slug),
        )

        product_review.save()

        return product_review
