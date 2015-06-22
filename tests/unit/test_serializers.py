# vim:fileencoding=utf-8
from __future__ import unicode_literals
from datetime import datetime
import pytz
from caspy.api import serializers
from caspy.domain import models as dm


class TestCurrencySerializer:
    def test_dm_to_pd(self):
        obj = dm.Currency(
                cur_code='USD',
                shortcut='$',
                symbol='$',
                long_name='US Dollar',
            )
        ser = serializers.CurrencySerializer(obj)
        data = ser.data
        assert data['cur_code'] == 'USD'
        assert data['shortcut'] == '$'
        assert data['symbol'] == '$'
        assert data['long_name'] == 'US Dollar'

    def test_pd_to_dm(self):
        data = {
                'cur_code': 'NIS',
                'shortcut': 'S',
                'symbol': '₪',
                'long_name': 'New Israeli Shekel',
            }
        ser = serializers.CurrencySerializer(data=data)
        assert ser.is_valid()
        obj = ser.save()
        assert obj.cur_code == 'NIS'
        assert obj.shortcut == 'S'
        assert obj.symbol == '₪'
        assert obj.long_name == 'New Israeli Shekel'


class TestBookSerializer:
    naive_time = datetime(2015, 6, 7, 13, 30)
    aware_time = pytz.timezone('Asia/Jerusalem').localize(naive_time)
    datetime_string = aware_time.isoformat()

    def test_dm_to_pd(self):
        obj = dm.Book(
                book_id=2,
                name='Test Book',
                created_at=self.aware_time,
            )
        ser = serializers.BookSerializer(obj)
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
        ser = serializers.BookSerializer(data=data)
        assert ser.is_valid()
        obj = ser.save()
        assert obj.book_id == 18
        assert obj.name == 'Book for testing'
        assert obj.created_at == self.aware_time

    def test_only_name(self):
        data = {'name': 'Minimal data book'}
        ser = serializers.BookSerializer(data=data)
        assert ser.is_valid()


class TestAccountTypeSerializer:
    def test_dm_to_pd(self):
        obj = dm.AccountType(
                account_type='Asset',
                sign=False,
                credit_term='decrease',
                debit_term='increase',
            )
        ser = serializers.AccountTypeSerializer(obj)
        data = ser.data
        assert data['account_type'] == 'Asset'
        assert data['sign'] is False
        assert data['credit_term'] == 'decrease'
        assert data['debit_term'] == 'increase'

    def test_pd_to_dm(self):
        data = {
                'account_type': 'Liability',
                'sign': True,
                'credit_term': 'increase',
                'debit_term': 'decrease',
            }
        ser = serializers.AccountTypeSerializer(data=data)
        assert ser.is_valid()
        obj = ser.save()
        assert isinstance(obj, dm.AccountType)
        assert obj.account_type == 'Liability'
        assert obj.sign is True
        assert obj.credit_term == 'increase'
        assert obj.debit_term == 'decrease'
