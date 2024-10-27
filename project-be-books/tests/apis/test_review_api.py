import json

from rest_framework import status
from rest_framework.test import APITestCase

from app.models import Review
from tests.models.review_builder import ReviewBuilder


class ReviewGetApiTestCase(APITestCase):
    def test_return_202_if_review_is_processing(self):
        response = self.client.get(f"/review/{ReviewBuilder.default_id}")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_get_review(self):
        (
            ReviewBuilder()
            .with_id(ReviewBuilder.default_id)
            .with_score(8)
            .with_review("Nice")
            .with_book_id(84)
            .with_book_title("The Great Gatsby")
            .with_book_authors([{"name": "F. Scott Fitzgerald"}])
            .with_book_subjects(["Gatsby", "Fiction"])
            .build()
        )

        response = self.client.get(f"/review/{ReviewBuilder.default_id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        review = json.loads(response.content)

        self.assertEqual(review["id"], ReviewBuilder.default_id)
        self.assertEqual(review["review"], "Nice")
        self.assertEqual(review["score"], 8)
        self.assertEqual(review["book_id"], 84)
        self.assertEqual(review["book_title"], "The Great Gatsby")
        self.assertEqual(review["book_authors"], [{"name": "F. Scott Fitzgerald"}])
        self.assertEqual(review["book_subjects"], ["Gatsby", "Fiction"])


class ReviewUpdateApiTestCase(APITestCase):
    def test_return_404_if_review_does_not_exists(self):
        response = self.client.put(
            f"/review/{ReviewBuilder.default_id}",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_return_400_if_score_is_out_of_range(self):
        response = self.client.put(
            f"/review/{ReviewBuilder.default_id}",
            data={"score": 800},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_review(self):
        (
            ReviewBuilder()
            .with_id(ReviewBuilder.default_id)
            .with_score(8)
            .with_review("Not nice")
            .build()
        )

        response = self.client.put(
            f"/review/{ReviewBuilder.default_id}",
            data={"review": "Nice"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        review = Review.objects.get(id=ReviewBuilder.default_id)

        self.assertEqual(review.score, 8)
        self.assertEqual(review.review, "Nice")


class ReviewDeleteApiTestCase(APITestCase):
    def test_return_404_if_review_does_not_exists(self):
        response = self.client.delete(f"/review/{ReviewBuilder.default_id}")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_review(self):
        ReviewBuilder().with_id(ReviewBuilder.default_id).build()

        response = self.client.delete(f"/review/{ReviewBuilder.default_id}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 0)
