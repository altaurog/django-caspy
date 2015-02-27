from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from caspy import models

class TestRoot(APITestCase):
    def test_api_root_get(self):
        api_root = reverse('api-root')
        response = self.client.get(api_root)
        assert response.status_code == status.HTTP_200_OK
        request = response.wsgi_request
        currency_url = reverse('api-currency-list')
        assert response.data['currency'] == request.build_absolute_uri(currency_url)

currency_data = {
        'code': 'MM',
        'shortcut': 'M',
        'symbol': 'M',
        'long_name': 'Monopoly Money',
    }

currency_fixture = [
    {
        'code': 'USD',
        'shortcut': '$',
        'symbol': '$',
        'long_name': 'US Dollar',
    }, {
        'code': 'EUR',
        'shortcut': 'E',
        'symbol': '',
        'long_name': 'Euro',
    },
]

class TestCurrency(APITestCase):
    def setUp(self):
        for data in currency_fixture:
            models.Currency.objects.create(**data)
        self.endpoint = reverse('api-currency-list')
        self.do_get()
        self.initial_response = self.get_response

    def do_get(self):
        self.get_response = self.client.get(self.endpoint)

    def test_list_get(self):
        assert self.get_response.status_code == status.HTTP_200_OK
        assert self.get_response.data == currency_fixture

    def test_list_post(self):
        post_response = self.client.post(self.endpoint, currency_data, format='json')
        assert post_response.status_code == status.HTTP_201_CREATED
        assert post_response.data == currency_data
        self.do_get()
        assert self.get_response.data == currency_fixture + [currency_data]

    def test_list_post_invalid(self):
        for field_omitted in currency_data.keys():
            post_data = currency_data.copy()
            del post_data[field_omitted]
            post_response = self.client.post(self.endpoint, post_data, format='json')
            assert post_response.status_code == status.HTTP_400_BAD_REQUEST
            assert post_response.data == {field_omitted: ['This field is required.']}

    def test_currency_detail(self):
        expected_data = currency_fixture[0]
        code = expected_data['code']
        url = reverse('api-currency-detail', kwargs={'pk': code})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_currency_delete(self):
        code = currency_fixture[0]['code']
        url = reverse('api-currency-detail', kwargs={'pk': code})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None
        self.do_get()
        assert self.get_response.data == currency_fixture[1:]

