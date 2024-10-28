from app.models.review import Review
from app.services.book_service import BookService, BookDetail, EmptyBookDetail


class ReviewNotFoundException(Exception):
    pass


class ReviewService:
    @classmethod
    def get_review(cls, id: str) -> Review:
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            raise ReviewNotFoundException

    @classmethod
    def create_review(cls, id: str, data: dict) -> None:
        book_id = data["id"]
        book_data: BookDetail

        try:
            book_data = BookService.get_book_detail(book_id)
        except Exception:
            book_data = EmptyBookDetail

        Review.objects.create(
            id=id,
            review=data["review"],
            score=data["score"],
            book_id=book_id,
            book_title=book_data["title"],
            book_authors=book_data["authors"],
            book_subjects=book_data["subjects"],
        )

    @classmethod
    def update_review(cls, id: str, data: dict) -> None:
        review = cls.get_review(id)
        review.score = data.get("score", review.score)
        review.review = data.get("review", review.review)
        review.save()

    @classmethod
    def delete_review(cls, id: str) -> None:
        review = cls.get_review(id)
        review.delete()
