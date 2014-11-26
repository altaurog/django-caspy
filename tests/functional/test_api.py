from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

class TestRoot(APITestCase):
    def test_api_root_exists(self):
        api_root = reverse('api-root')
        response = self.client.get(api_root)
