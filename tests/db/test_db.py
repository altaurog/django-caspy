import pytest
from django.db import connection, IntegrityError
from django.forms.models import model_to_dict
from caspy import models

from testapp import factories, set_constraints_immediate

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
    def setup(self):
        set_constraints_immediate(connection)

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

    fkeys = ('book_id', 'currency_id', 'account_type_id')

    @pytest.mark.parametrize('ref', fkeys)
    def test_foreign_key_constraints(self, ref):
        book = factories.BookFactory.create()
        currency = factories.CurrencyFactory.create()
        account_type = factories.AccountTypeFactory.create()
        kwargs = {
                'book_id': book.pk,
                'currency_id': currency.pk,
                'account_type_id': account_type.pk,
                'name': 'Integrity',
            }
        kwargs[ref] = 1000
        with pytest.raises(IntegrityError):
            models.Account.objects.create(**kwargs)


class TestTransaction:
    mgr = models.Transaction.objects
    def test_create_transaction(self):
        kwargs = {'date': '2015-07-21'}
        self.mgr.create(**kwargs)
        qset = self.mgr.filter(description__isnull=True, **kwargs)
        assert qset.exists()

    def test_create_with_description(self):
        kwargs = {'date': '2015-07-21', 'description': 'Test Transaction'}
        self.mgr.create(**kwargs)
        qset = self.mgr.filter(**kwargs)
        assert qset.exists()

    def test_date_not_unique(self):
        kwargs = {'date': '2015-07-21'}
        self.mgr.create(**kwargs)
        self.mgr.create(**kwargs)
        qset = self.mgr.filter(**kwargs)
        assert qset.count() == 2


class TestSplit:
    mgr = models.Split.objects
    def setup(self):
        self.xact = models.Transaction.objects.create(date='2017-07-22')
        self.account_a = factories.AccountFactory()
        self.account_b = factories.AccountFactory()

    def test_create_split(self):
        kwargs = {
                'transaction': self.xact,
                'number': '11-a',
                'account': self.account_a,
                'status': 'n',
                'amount': 47.50,
            }
        self.mgr.create(**kwargs)
        qset = self.mgr.filter(**kwargs)
        assert qset.exists()
