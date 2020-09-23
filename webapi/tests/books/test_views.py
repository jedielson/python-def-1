import random
from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

from webapi.models import Book, Author


class TestViews(TestCase):
    def setUp(self):
        self.url_list = reverse('book-list')
        self.url_detail = reverse('book-detail', args=['pk'])
        # self.books = []
        self.names = []
        self.fake = Faker()

        for _ in range(10):
            name = self.fake.name()
            Author.objects.create(name=name)

        authors = Author.objects.all()
        for _ in range(10):
            name = self.fake.name()
            self.names.append(name)
            au = random.choice(authors)
            book = Book(name=name, edition=1, publication_year=2020)
            book.save()
            book.authors.add(au)

    def test_books_list_returns_200(self):
        response = self.client.get(self.url_list)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_book_list_returns_correct_itens(self):
        response = self.client.get(self.url_list,
                                   data={
                                       'limit': 10,
                                       'offset': 0
                                   })
        self.assertEquals(10, len(response.data['results']))

    def test_book_list_is_paged(self):
        response = self.client.get(self.url_list,
                                   data={
                                       'limit': 5,
                                       'offset': 0
                                   })

        self.assertEquals(5, len(response.data['results']))
        self.assertEquals(10, response.data['count'])

    def test_book_list_filter_by_name_is_200(self):
        response = self.client.get(self.url_list, data={'name': self.names[0]})

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(self.names[0], response.data['results'][0]['name'])
        self.assertEquals(1, response.data['count'])

    def test_book_list_filter_by_wrong_name_is_200(self):
        name = self.fake.name()
        response = self.client.get(self.url_list, data={'name': name})

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(0, response.data['count'])

    def test_book_list_filter_by_publication_year_is_200(self):
        response = self.client.get(self.url_list,
                                   data={'publication_year': 2020})

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(10, response.data['count'])

    def test_book_list_filter_by_wrong_publication_year_is_200(self):
        response = self.client.get(self.url_list,
                                   data={'publication_year': 2018})

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(0, response.data['count'])

    def test_book_list_filter_by_edition_is_200(self):
        response = self.client.get(self.url_list,
                                   data={'edition': 1})

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(10, response.data['count'])

    def test_book_list_filter_by_wrong_edition_is_200(self):
        response = self.client.get(self.url_list,
                                   data={'edition': 2})

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(0, response.data['count'])

    def test_detail_is_200(self):
        response = self.client.get(reverse('book-detail', args=[1]))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_detail_is_404(self):
        response = self.client.get(reverse('book-detail', args=[100]))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_book_list_wrong_methods_is_405(self):
        response = self.client.put(self.url_list)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.url_list)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_book_detail_wrong_methods_is_404(self):
        response = self.client.post(self.url_detail)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)
