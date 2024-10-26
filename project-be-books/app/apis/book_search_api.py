from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from app.services.book_service import BookService


class BookSearchParams(serializers.Serializer):
    q = serializers.CharField(required=True)


class BookAuthorSerializer(serializers.Serializer):
    name = serializers.CharField()


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    authors = BookAuthorSerializer(many=True)


class BookSearchApi(APIView):
    def get(self, request, *args, **kwargs):
        params = BookSearchParams(data=self.request.query_params)
        params.is_valid(raise_exception=True)

        books = BookService.search_book(query=params.validated_data["q"])
        book_serializer = BookSerializer(books, many=True)

        return Response(data=book_serializer.data)
