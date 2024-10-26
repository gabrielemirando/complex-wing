import responses


class MockGutendexApi:
    @staticmethod
    def mock_search_book(
        query: str,
        results: list[dict],
        count: int or None = None,
        next_url: str or None = None,
        previous_url: str or None = None,
        status_code=200,
    ) -> None:
        responses.add(
            responses.GET,
            f"http://gutendex.com/books?search={query}",
            status=status_code,
            json={
                "count": count or len(results),
                "next": next_url,
                "previous": previous_url,
                "results": results,
            },
        )

    @staticmethod
    def verify_search_book(query: str, call_count: int = 1) -> None:
        responses.assert_call_count(
            f"http://gutendex.com/books?search={query}",
            call_count,
        )

    @staticmethod
    def mock_get_book_detail(
        book_id: int,
        title: str = "",
        authors: list[dict] = None,
        subjects: list[str] = None,
        status_code=200,
    ) -> None:
        responses.add(
            responses.GET,
            f"http://gutendex.com/books/{book_id}",
            status=status_code,
            json={
                "id": book_id,
                "title": title,
                "authors": authors or [],
                "subjects": subjects or [],
                "translators": [],
                "bookshelves": [],
                "languages": [],
                "copyright": None,
                "media_type": "",
                "formats": {},
                "download_count": 1,
            },
        )

    @staticmethod
    def mock_get_missing_book_detail(
        book_id: int,
        status_code=404,
    ) -> None:
        responses.add(
            responses.GET,
            f"http://gutendex.com/books/{book_id}",
            status=status_code,
            json={"detail": "No Book matches the given query."},
        )

    @staticmethod
    def verify_get_book_detail(book_id: int, call_count: int = 1) -> None:
        responses.assert_call_count(
            f"http://gutendex.com/books/{book_id}",
            call_count,
        )
