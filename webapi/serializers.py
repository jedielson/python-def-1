from rest_framework import serializers

from webapi.models import Author, Book


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'edition', 'publication_year', 'authors']
