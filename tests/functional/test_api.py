from operator import itemgetter, attrgetter
import pytest
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from caspy import models
from testapp import factories

pytestmark = pytest.mark.django_db(transaction=True)


class _TestEndpointMixin():
    _api_root_data = None

    def test_list_get(self):
        self.test = 'test_list_get'
        response = self.client.get(self._list_endpoint())
        assert response.status_code == 200
        pairs = list(self._pair(response.data, self.db_objs))
        for pd, db_o in pairs:
            self.check_match(pd, db_o)

    def test_list_post(self):
        self.test = 'test_list_post'
        data = self.new_pd()
        qset = self._qset(**data)
        assert not qset.exists()
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 201
        assert slicedict(response.data, data.keys()) == data
        assert qset.exists()

    def test_item_get(self):
        self.test = 'test_item_get'
        for db_o in self.db_objs:
            url = self._item_endpoint(db_o.pk)
            response = self.client.get(url)
            assert response.status_code == 200
            self.check_match(response.data, db_o)

    def test_item_put(self):
        self.test = 'test_item_put'
        for i, db_o in enumerate(self.db_objs):
            url = self._item_endpoint(db_o.pk)
            data = self.modified(i, db_o.pk)
            qset = self._qset(**data)
            assert not qset.exists()
            response = self.client.put(url, data)
            assert response.status_code == 200
            assert slicedict(response.data, data.keys()) == data
            assert qset.exists()

    def test_item_delete(self):
        self.test = 'test_item_delete'
        for db_o in self.db_objs:
            url = self._item_endpoint(db_o.pk)
            qset = self._qset(pk=db_o.pk)
            assert qset.exists()
            response = self.client.delete(url)
            assert response.status_code == 204
            assert not qset.exists()

    def _api_root(self):
        if _TestEndpointMixin._api_root_data is None:
            root_url = reverse('api-root')
            response = self.client.get(root_url)
            _TestEndpointMixin._api_root_data = response.data
        return _TestEndpointMixin._api_root_data

    def _endpoint(self, name=None):
        return self._api_root()[name or self.name]

    def _list_endpoint(self):
        return self._endpoint().replace(':{}/'.format(self.pk), '')

    def _item_endpoint(self, pk):
        return self._endpoint().replace(':{}'.format(self.pk), str(pk))

    def _pair(self, pdl, dbl):
        "sort and pair db objects with python dicts"
        spdl = sorted(pdl, key=itemgetter(self.pk))
        sdbl = sorted(dbl, key=attrgetter(self.pk))
        return zip(spdl, sdbl)

    def _qset(self, **qargs):
        return self.orm_filter(**qargs)


def slicedict(d, keys):
    return {k: d[k] for k in keys}


class TestCurrencyEndpoint(_TestEndpointMixin):
    count = 3
    name = 'currency'
    pk = 'cur_code'
    factory_class = factories.CurrencyFactory
    orm_filter = models.Currency.objects.filter

    def setup(self):
        self.client = APIClient()
        self.db_objs = self.factory_class.create_batch(self.count)

    def check_match(self, pd, db_o):
        "Compare a db obj with python dict"
        assert pd['cur_code'] == db_o.cur_code
        assert pd['shortcut'] == db_o.shortcut
        assert pd['symbol'] == db_o.symbol
        assert pd['long_name'] == db_o.long_name

    def new_pd(self):
        return {
                'cur_code': 'Au',
                'shortcut': 'g',
                'symbol': 'Au',
                'long_name': 'Gold Ingot',
            }

    def modified(self, i, pk):
        s = chr(ord('!') + i)
        return {
                'cur_code': pk,
                'shortcut': s,
                'symbol': s,
                'long_name': 'Modified Currency %d' % i,
            }


class TestBookEndpoint(_TestEndpointMixin):
    count = 3
    name = 'book'
    pk = 'book_id'
    factory_class = factories.BookFactory
    orm_filter = models.Book.objects.filter

    def setup(self):
        self.client = APIClient()
        self.db_objs = self.factory_class.create_batch(self.count)

    def check_match(self, pd, db_o):
        "Compare a db obj with python dict"
        assert pd['book_id'] == db_o.book_id
        assert pd['name'] == db_o.name

    def new_pd(self):
        return {
                'name': 'Functional Test Book',
            }

    def modified(self, i, pk):
        return {
                'book_id': pk,
                'name': 'Functional Test Book %d' % i,
            }


class TestAccountTypeEndpoint(_TestEndpointMixin):
    count = 3
    name = 'accounttype'
    pk = 'account_type'
    factory_class = factories.AccountTypeFactory
    orm_filter = models.AccountType.objects.filter

    def setup(self):
        self.client = APIClient()
        self.db_objs = self.factory_class.create_batch(self.count)

    def check_match(self, pd, db_o):
        assert pd['account_type'] == db_o.account_type
        assert pd['sign'] == db_o.sign
        assert pd['credit_term'] == db_o.credit_term
        assert pd['debit_term'] == db_o.debit_term

    def new_pd(self):
        return {
                'account_type': 'Asset',
                'sign': False,
                'credit_term': 'decrease',
                'debit_term': 'increase',
            }

    def modified(self, i, pk):
        return {
                'account_type': pk,
                'sign': False,
                'credit_term': 'decrease',
                'debit_term': 'increase',
            }
