from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from caspy import models


class TestRoot(APITestCase):
    def setUp(self):
        api_root = reverse('api-root')
        self.response = self.client.get(api_root)

    def test_api_root_get(self):
        assert self.response.status_code == status.HTTP_200_OK

    def test_currency_endpoint(self):
        self.check_endpoint('currency', 'api-currency-list')

    def check_endpoint(self, key, name):
        request = self.response.wsgi_request
        url = reverse('api-currency-list')
        absolute_url = request.build_absolute_uri(url)
        assert self.response.data[key] == absolute_url


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

    def do_post(self, data):
        return self.client.post(self.endpoint, data, format='json')

    def test_list_post(self):
        post_response = self.do_post(currency_data)
        assert post_response.status_code == status.HTTP_201_CREATED
        assert post_response.data == currency_data
        self.do_get()
        assert self.get_response.data == currency_fixture + [currency_data]

    def test_list_post_invalid(self):
        for field_omitted in currency_data.keys():
            post_data = currency_data.copy()
            del post_data[field_omitted]
            post_response = self.do_post(post_data)
            assert post_response.status_code == status.HTTP_400_BAD_REQUEST
            messages = ['This field is required.']
            assert post_response.data == {field_omitted: messages}

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
