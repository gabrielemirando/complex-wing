from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from app.models import Review
from app.services.review_service import ReviewService


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewUpdateData(serializers.Serializer):
    review = serializers.CharField(required=False, max_length=500)
    score = serializers.IntegerField(required=False, min_value=1, max_value=10)


class ReviewApi(APIView):
    def get(self, request, *args, **kwargs):
        review = ReviewService.get_review(id=kwargs["id"])
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        data = ReviewUpdateData(data=request.data)
        data.is_valid(raise_exception=True)
        ReviewService.update_review(id=kwargs["id"], data=data.validated_data)
        return Response("ok")

    def delete(self, request, *args, **kwargs):
        ReviewService.delete_review(id=kwargs["id"])
        return Response("ok")
