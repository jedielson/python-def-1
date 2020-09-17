from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from webapi.models import Author, Book
from webapi.serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
