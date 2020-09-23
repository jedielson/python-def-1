from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from webapi.models import Author, Book
from webapi.serializers import AuthorSerializer, BookWriteSerializer
from webapi.serializers import BooksReadSerializer


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'publication_year', 'edition']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return BooksReadSerializer
        return BookWriteSerializer
