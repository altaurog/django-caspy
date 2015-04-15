from datetime import timedelta
from django.utils import timezone
from caspy import models


class TestCurrency:
    def test_str(self):
        "String representation should be currency code"
        cur_obj = models.Currency(cur_code='USD')
        assert str(cur_obj) == 'USD'


class TestBook:
    def test_null_created_at(self):
        "If created_at isn't set, it should be set to now"
        before = timezone.now()
        book_obj = models.Book(name='Test Book')
        book_obj.set_created_at()
        after = timezone.now()
        assert before <= book_obj.created_at <= after

    def test_nonnull_created_at(self):
        "If created_at is set, it should remain unchanged"
        before = timezone.now() - timedelta(1)
        book_obj = models.Book(name='Test Book', created_at=before)
        book_obj.set_created_at()
        assert book_obj.created_at == before


class TestAccountType:
    def test_str(self):
        at_obj = models.AccountType(account_type='Income')
        assert str(at_obj) == 'Income'


class TestAccount:
    def test_str(self):
        account_obj = models.Account(name='Salary')
        assert str(account_obj) == 'Salary'
