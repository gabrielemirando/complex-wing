import uuid

from django.core.cache import cache

from app.models.review import Review
from app.services.book_service import BookDetail


class ReviewStillProcessing(Exception):
    pass


class ReviewNotFound(Exception):
    pass


class ReviewService:
    def __init__(self, id: str):
        self.id = id

    @staticmethod
    def generate_id_for_processing() -> str:
        new_id = str(uuid.uuid4())
        cache.add(new_id, True)
        return new_id

    def is_processing(self) -> bool:
        return cache.get(self.id, False)

    def remove_from_processing(self) -> None:
        cache.delete(self.id)

    def create(self, create_data: dict, book_data: BookDetail) -> None:
        Review.objects.create(
            id=self.id,
            review=create_data["review"],
            score=create_data["score"],
            book_id=create_data["id"],
            book_title=book_data["title"],
            book_authors=book_data["authors"],
            book_subjects=book_data["subjects"],
        )

    def get(self) -> Review:
        try:
            return Review.objects.get(id=self.id)
        except Review.DoesNotExist:
            if self.is_processing():
                raise ReviewStillProcessing()
            else:
                raise ReviewNotFound()

    def update(self, update_data: dict) -> None:
        review = self.get()
        review.score = update_data.get("score", review.score)
        review.review = update_data.get("review", review.review)
        review.save()

    def delete(self) -> None:
        review = self.get()
        review.delete()
