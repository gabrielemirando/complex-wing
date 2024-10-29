from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from app.apis.book_search_api import BookAuthorSerializer
from app.models import Review
from app.services.review_service import (
    ReviewService,
    ReviewNotFound,
    ReviewStillProcessing,
)


class ReviewSerializer(serializers.ModelSerializer):
    book_authors = BookAuthorSerializer(many=True)
    book_subjects = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Review
        fields = "__all__"


class ReviewUpdateSerializer(serializers.Serializer):
    review = serializers.CharField(required=False, max_length=500)
    score = serializers.IntegerField(required=False, min_value=1, max_value=10)


class ReviewApi(APIView):
    @extend_schema(
        summary="Get review",
        responses={
            200: ReviewSerializer,
            202: OpenApiResponse(description="Processing"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def get(self, request, *args, **kwargs):
        review_service = self._get_review_service(**kwargs)

        try:
            review = review_service.get()
            return Response(ReviewSerializer(review).data)
        except ReviewStillProcessing:
            return Response(status=202)
        except ReviewNotFound:
            return Response(status=404)

    @extend_schema(
        summary="Update review or score",
        request=ReviewUpdateSerializer,
        responses={
            200: OpenApiResponse(str, description="ok"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def put(self, request, *args, **kwargs):
        update_data = ReviewUpdateSerializer(data=request.data)
        update_data.is_valid(raise_exception=True)

        review_service = self._get_review_service(**kwargs)

        try:
            review_service.update(update_data.validated_data)
            return Response("ok")
        except (ReviewNotFound, ReviewStillProcessing):
            return Response(status=404)

    @extend_schema(
        summary="Delete review",
        responses={
            200: OpenApiResponse(str, description="ok"),
            404: OpenApiResponse(description="Not found"),
        },
    )
    def delete(self, request, *args, **kwargs):
        review_service = self._get_review_service(**kwargs)

        try:
            review_service.delete()
            return Response("ok")
        except (ReviewNotFound, ReviewStillProcessing):
            return Response(status=404)

    def _get_review_service(self, **kwargs) -> ReviewService:
        return ReviewService(str(kwargs["id"]))
