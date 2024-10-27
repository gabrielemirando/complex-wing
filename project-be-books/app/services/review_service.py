from django.shortcuts import get_object_or_404

from app.models.review import Review
from app.services.book_service import BookService, BookDetail, EmptyBookDetail


class ReviewService:
    @staticmethod
    def get_review(id: str) -> Review:
        return Review.objects.get(id=id)

    @staticmethod
    def create_review(id: str, data: dict) -> None:
        book_id = data["id"]
        book_data: BookDetail

        try:
            book_data = BookService.get_book_detail(book_id)
        except Exception:
            book_data = EmptyBookDetail

        Review.objects.create(
            id=id,
            score=data["score"],
            content=data["review"],
            book_id=book_id,
            book_title=book_data["title"],
            book_authors=book_data["authors"],
            book_subjects=book_data["subjects"],
        )

    @staticmethod
    def update_review(id: str, data: dict) -> None:
        review = get_object_or_404(Review, id=id)
        review.score = data.get("score", review.score)
        review.content = data.get("review", review.content)
        review.save()

    @staticmethod
    def delete_review(id: str) -> None:
        review = get_object_or_404(Review, id=id)
        review.delete()
