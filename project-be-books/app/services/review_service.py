from django.shortcuts import get_object_or_404

from app.models.review import Review
from app.services.book_service import BookService, BookDetail


class ReviewService:
    @staticmethod
    def get_review(id: int) -> Review:
        return get_object_or_404(Review, id=id)

    @staticmethod
    def create_review(id: str, data: dict) -> None:
        try:
            book_data = BookService.get_book_detail(data["id"])
        except Exception:
            book_data = BookDetail(id=0, title="", authors=[], subjects=[])

        Review.objects.create(
            id=id,
            score=data["score"],
            content=data["review"],
            book_id=data["id"],
            book_title=book_data["title"],
            book_authors=book_data["authors"],
            book_subjects=book_data["subjects"],
        )

    @staticmethod
    def update_review(id: int, data: dict) -> None:
        review = get_object_or_404(Review, id=id)
        review.score = data.get("score", review.score)
        review.content = data.get("review", review.content)
        review.save()

    @staticmethod
    def delete_review(id: int) -> None:
        review = get_object_or_404(Review, id=id)
        review.delete()
