from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    edition = models.IntegerField()
    publication_year = models.IntegerField()
    authors = models.ManyToManyField(Author)

    def __str__(self):
        return f"{self.name} {self.edition} {self.publication_year}"

    class Meta:
        ordering = ['name']
