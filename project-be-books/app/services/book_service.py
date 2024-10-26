import requests


class BookService:
    endpoint = "http://gutendex.com/books"

    @classmethod
    def search_book(cls, query: str) -> list[dict]:
        response = requests.get(cls.endpoint, params={"search": query})
        return response.json()["results"]
