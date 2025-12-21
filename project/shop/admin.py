from django.utils.safestring import mark_safe


class ImagePreviewMixin:
    """
    Mixin to provide a dynamic image preview in the Django admin.
    Set IMAGE_PREVIEW_FIELD to the name of your ImageField (default is 'image').
    """

    IMAGE_PREVIEW_FIELD = "image"

    class Media:
        # CSS is a dictionary mapping media types to lists of paths
        css = {"all": ("shop/css/admin/image_preview.css",)}

        # JS is a list/tuple of paths
        js = ("shop/js/admin/image_preview.js",)

    def image_preview(self, obj):
        """Generates the container and initial image for the script to target."""

        # Dynamically get the field defined in IMAGE_PREVIEW_FIELD
        image_field = getattr(obj, self.IMAGE_PREVIEW_FIELD, None)

        image_url = image_field.url if image_field else ""
        display_style = "block" if image_url else "none"

        return mark_safe(
            f"""
                <div class="field-preview" data-name="{self.IMAGE_PREVIEW_FIELD}">
                    <img src="{image_url}" style="display: {display_style};" />
                </div>
            """
        )

    image_preview.short_description = f"{IMAGE_PREVIEW_FIELD.capitalize()} Preview"
