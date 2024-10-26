from django.urls import path

from app.apis.book_search_api import BookSearchApi
from app.apis.review_api import ReviewApi
from app.apis.review_create_api import ReviewCreateApi

urlpatterns = [
    path(
        "search",
        view=BookSearchApi.as_view(),
        name="book_search",
    ),
    path(
        "review",
        view=ReviewCreateApi.as_view(),
        name="review_create",
    ),
    path(
        "review/<uuid:id>",
        view=ReviewApi.as_view(),
        name="review",
    ),
]
