try:
    from itertools import izip_longest as zip_longest  # 2
except ImportError:
    from itertools import zip_longest  # 3
from datetime import datetime
from operator import itemgetter, attrgetter
import pytest
from django.core.urlresolvers import reverse
from django.db import connection
from rest_framework.test import APIClient
from rest_framework.fields import DateTimeField
from caspy import models, time
from testapp import factories, fixtures

pytestmark = pytest.mark.django_db(transaction=True)


def format_datetime(dt):
    return DateTimeField().to_representation(dt)


class EndpointMixin(object):
    _api_root_data = None

    def _api_root(self):
        if EndpointMixin._api_root_data is None:
            root_url = reverse('api-root')
            response = self.client.get(root_url)
            EndpointMixin._api_root_data = response.data
        return EndpointMixin._api_root_data

    def _endpoint(self, name=None):
        return self._api_root()[name or self.name]

    def _list_endpoint(self, *args, **kwargs):
        template = self._endpoint(*args, **kwargs)
        return template.replace(':{}/'.format(self.pk), '')

    def _item_endpoint(self, pk, *args, **kwargs):
        template = self._endpoint(*args, **kwargs)
        return template.replace(':{}'.format(self.pk), str(pk))

    def _pair(self, pdl, dbl):
        "sort and pair db objects with python dicts"
        spdl = sorted(pdl, key=itemgetter(self.pk))
        sdbl = sorted(dbl, key=attrgetter(self.pk))
        return zip_longest(spdl, sdbl)

    def _qset(self, **qargs):
        return self.orm_filter(**qargs)
    not_exists_pk = '100'


class APIMixin(EndpointMixin):
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

    def test_not_exists_get(self):
        assert not self._qset(pk=self.not_exists_pk).exists()
        url = self._item_endpoint(self.not_exists_pk)
        response = self.client.get(url)
        assert response.status_code == 404

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

    def test_not_exists_put(self):
        assert not self._qset(pk=self.not_exists_pk).exists()
        data = self.modified(5, self.not_exists_pk)
        url = self._item_endpoint(self.not_exists_pk)
        response = self.client.put(url, data)
        assert response.status_code == 404

    def test_item_delete(self):
        for db_o in self.db_objs:
            url = self._item_endpoint(db_o.pk)
            qset = self._qset(pk=db_o.pk)
            assert qset.exists()
            response = self.client.delete(url)
            assert response.status_code == 204
            assert not qset.exists()

    def test_not_exists_delete(self):
        assert not self._qset(pk=self.not_exists_pk).exists()
        url = self._item_endpoint(self.not_exists_pk)
        response = self.client.delete(url)
        assert response.status_code == 404


def slicedict(d, keys):
    return {k: d[k] for k in keys}


class TestCurrencyEndpoint(APIMixin):
    count = 3
    name = 'currency'
    pk = 'cur_code'
    not_exists_pk = 'SKR'
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
    def test_post_missing_required_fields(self, field):
        data = self.new_pd()
        del data[field]
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 400
        assert field in response.data
        assert 'This field is required.' in response.data[field]

    @pytest.mark.parametrize('field', ('shortcut', 'symbol', 'long_name',))
    def test_post_missing_optional_fields(self, field):
        data = self.new_pd()
        del data[field]
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 201

    @pytest.mark.parametrize('field', ('cur_code',))
    def test_put_missing_fields(self, field):
        for i, db_o in enumerate(self.db_objs):
            url = self._item_endpoint(db_o.pk)
            data = self.modified(i, db_o.pk)
            del data[field]
            response = self.client.put(url, data)
            assert response.status_code == 400
            assert field in response.data
            assert 'This field is required.' in response.data[field]

    @pytest.mark.parametrize('field', ('shortcut', 'symbol', 'long_name',))
    def test_put_missing_optional_fields(self, field):
        for i, db_o in enumerate(self.db_objs):
            url = self._item_endpoint(db_o.pk)
            data = self.modified(i, db_o.pk)
            del data[field]
            response = self.client.put(url, data)
            assert response.status_code == 200
            assert slicedict(response.data, data.keys()) == data
            assert self._qset(**data).exists()


class TestBookEndpoint(APIMixin):
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
    def test_post_missing_required_fields(self, field):
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


class TestAccountTypeEndpoint(APIMixin):
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
    def test_post_missing_required_fields(self, field):
        data = self.new_pd()
        del data[field]
        response = self.client.post(self._list_endpoint(), data)
        assert response.status_code == 400
        assert field in response.data
        assert 'This field is required.' in response.data[field]


class TestAccountEndpoint(EndpointMixin):
    name = 'account'
    pk = 'account_id'
    orm_filter = models.Account.objects.filter

    def setup(self):
        self.client = APIClient()
        self.instances = fixtures.test_fixture()
        self.book = self.instances['books'][0]
        self.book1_accounts = self.instances['accounts'][:4]
        self.citibank = self.instances['accounts'][3]

    def teardown(self):
        # django's flush doesn't purge db intelligently enough
        cur = connection.cursor()
        cur.execute("DELETE FROM caspy_split")
        cur.execute("DELETE FROM caspy_accountpath")
        cur.execute("DELETE FROM caspy_account")
        cur.close()

    def test_list_get(self):
        response = self.client.get(self._list_endpoint(self.book.book_id))
        assert response.status_code == 200
        pairs = list(self._pair(response.data, self.book1_accounts))
        for pd, db_o in pairs:
            self.check_match(pd, db_o)

    def test_list_post(self):
        data = self.new_pd()
        qargs = {k: v for k, v in data.items() if k != 'parent_id'}
        qset = self._qset(**qargs)
        assert not qset.exists()
        endpoint = self._list_endpoint(self.book.book_id)
        response = self.client.post(endpoint, data)
        data['book'] = self.book.book_id
        assert response.status_code == 201
        assert slicedict(response.data, data.keys()) == data
        assert qset.exists()

    def test_item_get(self):
        for db_o in self.book1_accounts:
            url = self._item_endpoint(db_o.pk, book_id=db_o.book_id)
            response = self.client.get(url)
            assert response.status_code == 200
            self.check_match(response.data, db_o)

    def test_item_put(self):
        for i, db_o in enumerate(self.book1_accounts):
            url = self._item_endpoint(db_o.pk, book_id=db_o.book_id)
            data = self.modified(i, db_o)
            response = self.client.put(url, data)
            assert response.status_code == 200
            assert slicedict(response.data, data.keys()) == data
            del data['parent_id']
            assert self._qset(book=db_o.book, **data).exists()

    def test_item_delete(self):
        for i, db_o in enumerate(self.book1_accounts):
            url = self._item_endpoint(db_o.pk, book_id=db_o.book_id)
            qset = self._qset(pk=db_o.pk)
            assert qset.exists()
            response = self.client.delete(url)
            assert response.status_code == 204
            assert not qset.exists()

    def new_pd(self):
        return {
                'name': 'Test',
                'account_type': self.citibank.account_type_id,
                'currency': 'USD',
                'description': 'Test account description',
                'parent_id': None,
            }

    def modified(self, i, db_o):
        return {
                'account_id': db_o.pk,
                'name': 'Test Account %d' % i,
                'account_type': db_o.account_type_id,
                'currency': 'CAD',
                'description': 'Test Account %d Description' % i,
                'parent_id': None,
            }

    def _endpoint(self, book_id):
        url_template = super(TestAccountEndpoint, self)._endpoint()
        return url_template.replace(':book_id', str(book_id))

    def check_match(self, pd, db_o):
        assert pd['account_id'] == db_o.account_id
        assert pd['name'] == db_o.name
        assert pd['book'] == db_o.book_id
        assert pd['account_type'] == db_o.account_type_id
        assert pd['currency'] == db_o.currency_id
        assert pd['description'] == db_o.description
