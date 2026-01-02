from django.urls import path

from comment.views import CommentCreateView

urlpatterns = [path("create/", CommentCreateView.as_view(), name="comment_create_page")]
