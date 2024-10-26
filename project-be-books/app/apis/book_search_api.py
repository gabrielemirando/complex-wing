from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from app.services.book_service import BookService


class BookAuthorSerializer(serializers.Serializer):
    name = serializers.CharField()


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    authors = BookAuthorSerializer(many=True)


class BookSearchApi(APIView):
    def get(self, request):
        search_query = self.request.query_params.get("q")

        if not search_query:
            return HttpResponseBadRequest()

        books = BookService.search_book(query=search_query)
        book_serializer = BookSerializer(books, many=True)

        return Response(data=book_serializer.data)
