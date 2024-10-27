from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from app.models import Review
from app.services.review_service import ReviewService
from app.tasks import is_create_review_pending


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewUpdateData(serializers.Serializer):
    review = serializers.CharField(required=False, max_length=500)
    score = serializers.IntegerField(required=False, min_value=1, max_value=10)


class ReviewApi(APIView):
    @extend_schema(
        summary="Get review",
        responses={
            200: ReviewSerializer,
            202: OpenApiResponse(description="Still processing"),
        },
    )
    def get(self, request, *args, **kwargs):
        review_id = str(kwargs["id"])

        try:
            review = ReviewService.get_review(id=review_id)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            status_code = 202 if is_create_review_pending(review_id) else 404
            return Response(status=status_code)

    @extend_schema(
        summary="Update review or score",
        request=ReviewUpdateData,
        responses=OpenApiResponse(str, description="ok"),
    )
    def put(self, request, *args, **kwargs):
        data = ReviewUpdateData(data=request.data)
        data.is_valid(raise_exception=True)
        ReviewService.update_review(id=kwargs["id"], data=data.validated_data)
        return Response("ok")

    @extend_schema(
        summary="Delete review",
        responses=OpenApiResponse(str, description="ok"),
    )
    def delete(self, request, *args, **kwargs):
        ReviewService.delete_review(id=kwargs["id"])
        return Response("ok")
