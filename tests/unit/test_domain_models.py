# vim:fileencoding=utf-8
from __future__ import unicode_literals

from caspy.domain import models


try:
    to_string = unicode  # 2
except NameError:
    to_string = str


class TestCurrency:
    def test_str(self):
        "String representation should be currency code"
        cur_obj = models.Currency(cur_code='USD')
        assert to_string(cur_obj) == 'USD'


class TestBook:
    def test_str(self):
        book_obj = models.Book(name='שנת 2015')
        assert to_string(book_obj) == 'שנת 2015'


class TestAccountType:
    def test_unicode(self):
        at_obj = models.AccountType(account_type='הוצאות')
        assert to_string(at_obj) == 'הוצאות'
