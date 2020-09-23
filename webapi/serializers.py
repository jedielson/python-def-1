from rest_framework import serializers

from webapi.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BooksReadSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'edition', 'publication_year', 'authors']


class BookWriteSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(many=True,
                                                 queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ['id', 'name', 'edition', 'publication_year', 'authors']
