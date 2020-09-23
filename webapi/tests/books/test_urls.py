from django.test import SimpleTestCase
from django.urls import reverse, resolve
from webapi.views import BookViewSet


class TestUrls(SimpleTestCase):
    def test_list_url_list_is_resolved(self):
        url = reverse('book-list')
        self.assertEquals(resolve(url).func.cls, BookViewSet)

    def test_list_url_detail_is_resolved(self):
        url = reverse('book-detail', args=['some-pk'])
        self.assertEquals(resolve(url).func.cls, BookViewSet)
