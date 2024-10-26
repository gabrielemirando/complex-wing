from typing import Self

from app.models.review import Review


class ReviewBuilder:
    default_id = "8103515f-4fb0-44cc-a374-4c02b451b7c7"

    def __init__(self):
        self.id = self.default_id
        self.score = 5
        self.content = ""
        self.book_id = 1
        self.book_title = ""
        self.book_authors = []
        self.book_subjects = []

    def with_id(self, value: str) -> Self:
        self.id = value
        return self

    def with_score(self, value: int) -> Self:
        self.score = value
        return self

    def with_content(self, value: str) -> Self:
        self.content = value
        return self

    def with_book_id(self, value: int) -> Self:
        self.book_id = value
        return self

    def with_book_title(self, value: str) -> Self:
        self.book_title = value
        return self

    def with_book_authors(self, value: list) -> Self:
        self.book_authors = value
        return self

    def with_book_subjects(self, value: list) -> Self:
        self.book_subjects = value
        return self

    def build(self) -> Review:
        return Review.objects.create(
            id=self.id,
            score=self.score,
            content=self.content,
            book_id=self.book_id,
            book_title=self.book_title,
            book_authors=self.book_authors,
            book_subjects=self.book_subjects,
        )
