from django.urls import path

from app.apis.book_search_api import BookSearchApi


urlpatterns = [
    path(
        "search",
        view=BookSearchApi.as_view(),
        name="book_search",
    ),
]
