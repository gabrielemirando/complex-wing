import json

import responses

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from tests.services.mock_gutenedex_api import MockGutendexApi


class BookSearchApiTestCase(APITestCase):
    def test_return_400_if_search_query_param_is_missing(self):
        response = self.client.get(reverse("book_search"))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @responses.activate
    def test_return_book_list(self):
        MockGutendexApi.mock_search_book(
            query="Frankenstein",
            results=[
                {
                    "id": 1,
                    "title": "Frankenstein",
                    "authors": [
                        {
                            "name": "Mary Shelley",
                            "birth_year": 1797,
                            "death_year": 1851,
                        }
                    ],
                    "translators": [],
                    "subjects": [],
                    "bookshelves": [],
                },
                {
                    "id": 2,
                    "title": "Frankenstein 2",
                    "authors": [
                        {
                            "name": "Mary Shelley",
                            "birth_year": 1797,
                            "death_year": 1851,
                        },
                        {
                            "name": "Piero Angela",
                            "birth_year": 1920,
                            "death_year": 2020,
                        },
                    ],
                    "translators": [],
                    "languages": ["en"],
                    "media_type": "Text",
                },
            ],
        )

        response = self.client.get(
            reverse("book_search"),
            query_params={"q": "Frankenstein"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            [
                {
                    "id": 1,
                    "title": "Frankenstein",
                    "authors": [{"name": "Mary Shelley"}],
                },
                {
                    "id": 2,
                    "title": "Frankenstein 2",
                    "authors": [
                        {"name": "Mary Shelley"},
                        {"name": "Piero Angela"},
                    ],
                },
            ],
            json.loads(response.content),
        )

        MockGutendexApi.verify_search_book(query="Frankenstein", call_count=1)
