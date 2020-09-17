from django.test import SimpleTestCase
from django.urls import reverse, resolve
from webapi.views import AuthorViewSet


class TestUrls(SimpleTestCase):
    def test_list_url_list_is_resolved(self):
        url = reverse('author-list')
        self.assertEquals(resolve(url).func.cls, AuthorViewSet)

    def test_list_url_detail_is_resolved(self):
        url = reverse('author-detail', args=['some-pk'])
        self.assertEquals(resolve(url).func.cls, AuthorViewSet)
