import requests

from requests.models import Response

from typing import TypedDict


class BookDetail(TypedDict):
    id: int
    title: str
    authors: list[dict]
    subjects: list[str]


class BookService:
    endpoint = "http://gutendex.com/books"

    @classmethod
    def search_book(cls, query: str) -> list[BookDetail]:
        response = requests.get(BookService.endpoint, params={"search": query})
        return response.json()["results"]

    @classmethod
    def is_valid_book(cls, id: int) -> bool:
        return cls._get_book_detail_response(id).status_code == 200

    @classmethod
    def get_book_detail(cls, id: int) -> BookDetail:
        return cls._get_book_detail_response(id).json()

    @classmethod
    def _get_book_detail_response(cls, id: int) -> Response:
        return requests.get(f"{cls.endpoint}/{id}")
