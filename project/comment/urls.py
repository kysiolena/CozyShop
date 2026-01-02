from django.urls import path

from comment.views import CommentCreateView

urlpatterns = [
    path(
        "create/<int:product_id>/",
        CommentCreateView.as_view(),
        name="comment_create_page",
    )
]
