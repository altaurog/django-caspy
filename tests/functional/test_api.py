from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class TestRoot(APITestCase):
    def test_api_root_get(self):
        api_root = reverse('api-root')
        response = self.client.get(api_root)
        assert response.status_code == status.HTTP_200_OK
        request = response.wsgi_request
        currency_url = reverse('api-currency-list')
        assert response.data['currency'] == request.build_absolute_uri(currency_url)

initial_currencies = 'USD', 'NIS', 'GBP', 'EUR', 'JPY', 'CHF', 'CAD', 'RUB',
currency_data = {
        'code': 'MM',
        'shortcut': 'M',
        'symbol': 'M',
        'long_name': 'Monopoly Money',
    }

class TestCurrency(APITestCase):
    def setUp(self):
        self.endpoint = reverse('api-currency-list')
        self.get_response = self.client.get(self.endpoint)

    def test_currency_endpoint_get(self):
        assert self.get_response.status_code == status.HTTP_200_OK
        assert len(self.get_response.data) == len(initial_currencies)
        for obj in self.get_response.data:
            assert isinstance(obj, dict)
            for field_name in currency_data.keys():
                assert field_name in obj
        for currency in initial_currencies:
            found = filter(lambda o: o['code'] == currency, self.get_response.data)
            assert len(list(found)) == 1

    def test_currency_endpoint_post(self):
        initial_count = len(self.get_response.data)
        post_response = self.client.post(self.endpoint, currency_data, format='json')
        assert post_response.status_code == status.HTTP_201_CREATED
        assert post_response.data == currency_data
        new_get_response = self.client.get(self.endpoint)
        assert len(new_get_response.data) == initial_count + 1
        assert currency_data in new_get_response.data

    def test_currency_endpoint_post_invalid(self):
        for field_omitted in currency_data.keys():
            post_data = currency_data.copy()
            del post_data[field_omitted]
            post_response = self.client.post(self.endpoint, post_data, format='json')
            assert post_response.status_code == status.HTTP_400_BAD_REQUEST
            assert post_response.data == {field_omitted: ['This field is required.']}

