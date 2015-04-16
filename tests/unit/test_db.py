import pytest
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from caspy import models
from testapp import factories

pytestmark = pytest.mark.django_db()


class TestCurrency:
    def test_create_currency(self):
        currency = factories.CurrencyFactory()
        data = model_to_dict(currency)
        assert models.Currency.objects.filter(**data).exists()

    unique_fields = ('cur_code', 'shortcut', 'long_name')

    @pytest.mark.parametrize('dupfield', unique_fields)
    def test_uniquness(self, dupfield):
        data = {dupfield: 'A'}
        factories.CurrencyFactory(**data)
        with pytest.raises(IntegrityError):
            factories.CurrencyFactory(**data)


class TestBook:
    def test_create_book(self):
        book_obj = factories.BookFactory()
        data = model_to_dict(book_obj)
        assert models.Book.objects.filter(**data).exists()

    def test_uniqueness(self):
        name = 'Test Book'
        factories.BookFactory(name=name)
        with pytest.raises(IntegrityError):
            factories.BookFactory(name=name)


class TestAccountType:
    def test_create_accounttype(self):
        accounttype = factories.AccountTypeFactory()
        data = model_to_dict(accounttype)
        assert models.AccountType.objects.filter(**data).exists()

    def test_uniqueness(self):
        factories.AccountTypeFactory(account_type='Accounts Receivable')
        with pytest.raises(IntegrityError):
            factories.AccountTypeFactory(account_type='Accounts Receivable')


class TestAccount:
    def test_create_account(self):
        account_obj = factories.AccountFactory()
        data = model_to_dict(account_obj)
        assert models.Account.objects.filter(**data).exists()

    def test_create_with_empty_description(self):
        factories.AccountFactory(description='')

    def test_unique_id(self):
        account_obj = factories.AccountFactory()
        with pytest.raises(IntegrityError):
            factories.AccountFactory(account_id=account_obj.account_id)

    def test_unique_together(self):
        account_obj = factories.AccountFactory()
        name = account_obj.name
        book = account_obj.book
        factories.AccountFactory(name=name)
        factories.AccountFactory(book=book)
        with pytest.raises(IntegrityError):
            factories.AccountFactory(name=name, book=book)
