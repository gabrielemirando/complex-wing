from celery.app import shared_task

from app.services.book_service import BookService
from app.services.review_service import ReviewService


@shared_task()
def create_review(id: str, create_data: dict) -> None:
    book_service = BookService()
    review_service = ReviewService(id)

    try:
        book_data = book_service.get_book_detail(create_data["id"])
        review_service.create(create_data, book_data)
    finally:
        review_service.remove_from_processing()
