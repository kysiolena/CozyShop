from django.contrib import admin

from comment.models import Comment
from shop.admin import ImagePreviewMixin


class CommentAdmin(ImagePreviewMixin, admin.ModelAdmin):
    fields = ["image_preview", "image", "body", "is_approved", "user", "product"]

    # Add image field and the new preview method to readonly_fields
    readonly_fields = ["image_preview", "created_at", "updated_at"]


admin.site.register(Comment, CommentAdmin)
