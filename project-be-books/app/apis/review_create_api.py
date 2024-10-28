import uuid

from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from app.services.book_service import BookService
from app.tasks import create_review_async


class ReviewCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    review = serializers.CharField(required=True, max_length=500)
    score = serializers.IntegerField(required=True, min_value=1, max_value=10)

    def validate_id(self, value):
        if not BookService.is_valid_book(id=value):
            raise serializers.ValidationError()
        return value


class ReviewCreateApi(APIView):
    @extend_schema(
        summary="Create review",
        request=ReviewCreateSerializer,
        responses=OpenApiResponse(
            response=str,
            description="Review ID",
        ),
    )
    def post(self, request, *args, **kwargs):
        data = ReviewCreateSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        review_id = str(uuid.uuid4())
        create_review_async.apply_async(
            kwargs={"id": review_id, "data": data.validated_data},
            task_id=review_id,
        )

        return Response(review_id)
