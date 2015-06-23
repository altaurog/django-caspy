try:
    from itertools import izip_longest as zip_longest  # 2
except ImportError:
    from itertools import zip_longest  # 3
from datetime import datetime
from operator import itemgetter, attrgetter
import pytest
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient
from rest_framework.fields import DateTimeField
from caspy import models, time
from testapp import factories

pytestmark = pytest.mark.django_db(transaction=True)


def format_datetime(dt):
    return DateTimeField().to_representation(dt)


class _TestEndpointMixin():
    _api_root_data = None

    def test_list_get(self):
        response = self.client.get(self._list_endpoint())
        assert response.status_code == 200
        pairs = list(self._pair(response.data, self.db_objs))
        for pd, db_o in pairs:
            self.check_match(pd, db_o)

    def test_list_post(self):
        data = self.new_pd()
        qset = self._qset(**data)
        assert not qset.exists()
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 201
        assert slicedict(response.data, data.keys()) == data
        assert qset.exists()

    def test_item_get(self):
        for db_o in self.db_objs:
            url = self._item_endpoint(db_o.pk)
            response = self.client.get(url)
            assert response.status_code == 200
            self.check_match(response.data, db_o)

    def test_item_put(self):
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
        return zip_longest(spdl, sdbl)

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

    @pytest.mark.parametrize('field', ('cur_code',))
    def test_missing_required_fields(self, field):
        data = self.new_pd()
        del data[field]
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 400
        assert field in response.data
        assert 'This field is required.' in response.data[field]

    @pytest.mark.parametrize('field', ('shortcut', 'symbol', 'long_name',))
    def test_missing_optional_fields(self, field):
        data = self.new_pd()
        del data[field]
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 201


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
        return {'name': 'Functional Test Book'}

    def modified(self, i, pk):
        return {'name': 'Functional Test Book %d' % i}

    @pytest.mark.parametrize('field', ('name',))
    def test_missing_required_fields(self, field):
        data = self.new_pd()
        del data[field]
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 400
        assert field in response.data
        assert 'This field is required.' in response.data[field]

    def test_post_read_only_fields(self):
        data = self.new_pd()
        data['book_id'] = 10
        data['created_at'] = time.utc.localize(datetime(2015, 6, 20, 8, 20))
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 201
        assert response.data['book_id'] != data['book_id']
        created_at = format_datetime(data['created_at'])
        assert response.data['created_at'] != created_at


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

    required_fields = ('account_type', 'sign', 'credit_term', 'debit_term')

    @pytest.mark.parametrize('field', required_fields)
    def test_missing_required_fields(self, field):
        data = self.new_pd()
        del data[field]
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 400
        assert field in response.data
        assert 'This field is required.' in response.data[field]
