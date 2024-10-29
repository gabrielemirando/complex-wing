from typing import TypedDict

import requests

from requests.models import Response


class BookDetail(TypedDict):
    id: int
    title: str
    authors: list[dict]
    subjects: list[str]


class BookService:
    def __init__(self, endpoint: str = "http://gutendex.com/books"):
        self.endpoint = endpoint

    def search_book(self, query: str) -> list[BookDetail]:
        response = requests.get(self.endpoint, params={"search": query})
        return response.json()["results"]

    def is_book_valid(self, id: int) -> bool:
        response = self._get_book_detail_response(id)
        return response.status_code == 200

    def get_book_detail(self, id: int) -> BookDetail:
        response = self._get_book_detail_response(id)
        return response.json()

    def _get_book_detail_response(self, id: int) -> Response:
        return requests.get(f"{self.endpoint}/{id}")
