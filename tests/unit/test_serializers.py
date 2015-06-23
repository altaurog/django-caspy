# vim:fileencoding=utf-8
from __future__ import unicode_literals
from datetime import datetime
import pytz
import pytest
from caspy.api import serializers
from caspy.domain import models as dm


class TestCurrencySerializer:
    serializer_class = serializers.CurrencySerializer
    def test_dm_to_pd(self):
        obj = dm.Currency(
                cur_code='USD',
                shortcut='$',
                symbol='$',
                long_name='US Dollar',
            )
        ser = self.serializer_class(obj)
        data = ser.data
        assert data['cur_code'] == 'USD'
        assert data['shortcut'] == '$'
        assert data['symbol'] == '$'
        assert data['long_name'] == 'US Dollar'

    data = {
            'cur_code': 'NIS',
            'shortcut': 'S',
            'symbol': '₪',
            'long_name': 'New Israeli Shekel',
        }

    def test_pd_to_dm(self):
        ser = self.serializer_class(data=self.data)
        assert ser.is_valid()
        obj = ser.save()
        assert obj.cur_code == 'NIS'
        assert obj.shortcut == 'S'
        assert obj.symbol == '₪'
        assert obj.long_name == 'New Israeli Shekel'

    def test_required_field(self):
        data = self.data.copy()
        del data['cur_code']
        ser = self.serializer_class(data=data)
        assert not ser.is_valid()
        assert 'cur_code' in ser.errors
        assert 'This field is required.' in ser.errors['cur_code']

    @pytest.mark.parametrize('field', ('shortcut', 'symbol', 'long_name',))
    def test_optional_fields(self, field):
        data = self.data.copy()
        del data[field]
        ser = self.serializer_class(data=data)
        assert ser.is_valid()


class TestBookSerializer:
    serializer_class = serializers.BookSerializer
    naive_time = datetime(2015, 6, 7, 13, 30)
    aware_time = pytz.timezone('Asia/Jerusalem').localize(naive_time)
    datetime_string = aware_time.isoformat()

    def test_dm_to_pd(self):
        obj = dm.Book(
                book_id=2,
                name='Test Book',
                created_at=self.aware_time,
            )
        ser = self.serializer_class(obj)
        data = ser.data
        assert data['book_id'] == 2
        assert data['name'] == 'Test Book'
        assert data['created_at'] == self.datetime_string

    def test_pd_to_dm(self):
        data = {
                'book_id': 18,
                'name': 'Book for testing',
                'created_at': self.datetime_string,
            }
        ser = self.serializer_class(data=data)
        assert ser.is_valid()
        obj = ser.save()
        assert obj.book_id is None
        assert obj.name == 'Book for testing'
        assert obj.created_at is None

    def test_only_name(self):
        data = {'name': 'Minimal data book'}
        ser = self.serializer_class(data=data)
        assert ser.is_valid()


class TestAccountTypeSerializer:
    serializer_class = serializers.AccountTypeSerializer
    def test_dm_to_pd(self):
        obj = dm.AccountType(
                account_type='Asset',
                sign=False,
                credit_term='decrease',
                debit_term='increase',
            )
        ser = self.serializer_class(obj)
        data = ser.data
        assert data['account_type'] == 'Asset'
        assert data['sign'] is False
        assert data['credit_term'] == 'decrease'
        assert data['debit_term'] == 'increase'

    data = {
            'account_type': 'Liability',
            'sign': True,
            'credit_term': 'increase',
            'debit_term': 'decrease',
        }

    def test_pd_to_dm(self):
        ser = self.serializer_class(data=self.data)
        assert ser.is_valid()
        obj = ser.save()
        assert isinstance(obj, dm.AccountType)
        assert obj.account_type == 'Liability'
        assert obj.sign is True
        assert obj.credit_term == 'increase'
        assert obj.debit_term == 'decrease'

    @pytest.mark.parametrize('field', data.keys())
    def test_required_fields(self, field):
        data = self.data.copy()
        del data[field]
        ser = self.serializer_class(data=data)
        assert not ser.is_valid()
        assert field in ser.errors
        assert 'This field is required.' in ser.errors[field]
