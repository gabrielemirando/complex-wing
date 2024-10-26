from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.views import APIView
from rest_framework import serializers

from app.services.book_service import BookService


class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField()


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    authors = AuthorSerializer(many=True)


class BookSearchApi(APIView):
    def get(self, request):
        search_query = self.request.query_params.get("q")

        if not search_query:
            return HttpResponseBadRequest()

        books = BookService.search_book(query=search_query)
        book_serializer = BookSerializer(books, many=True)

        return JsonResponse(book_serializer.data, safe=False)
