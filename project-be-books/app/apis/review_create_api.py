import uuid

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from app.services.book_service import BookService
from app.services.review_service import ReviewService


class ReviewCreateData(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    review = serializers.CharField(required=True, max_length=500)
    score = serializers.IntegerField(required=True, min_value=1, max_value=10)

    def validate_id(self, value):
        if not BookService.is_valid_book(id=value):
            raise serializers.ValidationError()
        return value


class ReviewCreateApi(APIView):
    def post(self, request, *args, **kwargs):
        data = ReviewCreateData(data=request.data)
        data.is_valid(raise_exception=True)

        review_id = str(uuid.uuid4())
        ReviewService.create_review(id=review_id, data=data.validated_data)

        return Response({"id": review_id})
