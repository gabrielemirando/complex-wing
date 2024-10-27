import json

import responses
from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase

from app.models.review import Review
from tests.services.mock_gutenedex_api import MockGutendexApi


class ReviewCreateApiTestCase(APITestCase):
    @responses.activate
    def test_return_400_if_book_id_does_not_exist(self):
        MockGutendexApi.mock_get_missing_book_detail(book_id=1)

        response = self.client.post(
            "/review",
            data={
                "id": 1,
                "review": "Good book!",
                "score": 5,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        MockGutendexApi.verify_get_book_detail(book_id=1, call_count=1)

    @responses.activate
    def test_return_400_if_score_is_not_in_range(self):
        MockGutendexApi.mock_get_book_detail(book_id=1)

        response = self.client.post(
            "/review",
            data={
                "id": 1,
                "review": "Good book!",
                "score": 50,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @responses.activate
    def test_return_400_if_content_is_too_long(self):
        MockGutendexApi.mock_get_book_detail(book_id=1)

        response = self.client.post(
            "/review",
            data={
                "id": 1,
                "review": "Good book!" * 500,
                "score": 5,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @responses.activate
    @override_settings(
        task_eager_propagates=True,
        task_always_eager=True,
        broker_url="memory://",
        backend="memory",
    )
    def test_create_review_successfully(self):
        MockGutendexApi.mock_get_book_detail(
            book_id=1,
            title="Frankenstein",
            authors=[{"name": "Mary Shelley"}],
            subjects=["Dr Frankenstein", "Monster"],
        )

        response = self.client.post(
            "/review",
            data={
                "id": 1,
                "review": "Good book!",
                "score": 5,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Review.objects.count(), 1)

        review = Review.objects.first()
        self.assertIsNotNone(review.id)
        self.assertEqual(review.score, 5)
        self.assertEqual(review.content, "Good book!")
        self.assertEqual(review.book_id, 1)
        self.assertEqual(review.book_title, "Frankenstein")
        self.assertEqual(review.book_authors, [{"name": "Mary Shelley"}])
        self.assertEqual(review.book_subjects, ["Dr Frankenstein", "Monster"])

        self.assertEqual(str(review.id), json.loads(response.content))
