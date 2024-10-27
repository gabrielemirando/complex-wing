from celery.app import shared_task
from celery.result import AsyncResult

from app.services.review_service import ReviewService


@shared_task()
def create_review_async(id: str, data: dict) -> None:
    ReviewService.create_review(id=id, data=data)


def is_create_review_pending(id: str) -> bool:
    return not AsyncResult(id).ready()
