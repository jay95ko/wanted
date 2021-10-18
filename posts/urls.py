from django.urls import path
from .views import PostsView, PostView

urlpatterns = [
    path("", PostsView.as_view()),
    path("/<int:post_id>", PostView.as_view()),
]
