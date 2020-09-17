from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status

from webapi.models import Author


class TestViews(TestCase):
    def setUp(self):
        self.url_list = reverse('author-list')
        self.url_detail = reverse('author-detail', args=['pk'])
        self.names = []
        self.fake = Faker()

        for _ in range(10):
            name = self.fake.name()
            self.names.append(name)
            Author.objects.create(name=name)

    def test_author_list_returns_200(self):
        response = self.client.get(self.url_list)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_author_list_returns_correct_itens(self):

        response = self.client.get(self.url_list,
                                   data={
                                       'limit': 10,
                                       'offset': 0
                                   })
        self.assertEquals(10, len(response.data['results']))

    def test_author_list_is_paged(self):
        response = self.client.get(self.url_list,
                                   data={
                                       'limit': 5,
                                       'offset': 0
                                   })

        self.assertEquals(5, len(response.data['results']))
        self.assertEquals(10, response.data['count'])

    def test_author_list_filter_is_200(self):
        response = self.client.get(self.url_list, data={'name': self.names[0]})

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(self.names[0], response.data['results'][0]['name'])
        self.assertEquals(1, response.data['count'])

    def test_author_list_filter_with_wrong_name_should_be_200(self):
        response = self.client.get(self.url_list,
                                   data={'name': self.fake.name()})

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(0, response.data['count'])

    def test_detail_is_200(self):
        response = self.client.get(reverse('author-detail', args=[1]))
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_detail_is_404(self):
        response = self.client.get(reverse('author-detail', args=[100]))
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_author_list_wrong_methods_is_404(self):
        response = self.client.post(self.url_list)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.url_list)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.url_list)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_author_detail_wrong_methods_is_404(self):
        response = self.client.post(self.url_detail)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.url_detail)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(self.url_detail)
        self.assertEquals(response.status_code,
                          status.HTTP_405_METHOD_NOT_ALLOWED)
