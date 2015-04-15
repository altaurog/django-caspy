import pytest
from django.db.utils import IntegrityError
from caspy import models

pytestmark = pytest.mark.django_db()


currency = {
        'cur_code': 'MM',
        'shortcut': 'M',
        'symbol': 'M',
        'long_name': 'Monopoly Money',
    }


class TestCurrency:
    mgr = models.Currency.objects
    def test_create_currency(self):
        self.mgr.create(**currency)
        assert self.mgr.filter(**currency).exists()

    unique_fields = ('cur_code', 'shortcut', 'long_name')

    @pytest.mark.parametrize('dupfield', unique_fields)
    def test_uniquness(self, dupfield):
        self.mgr.create(**currency)
        data = currency.copy()
        data.update({f: 'A' for f in data.keys() if f != dupfield})
        with pytest.raises(IntegrityError):
            self.mgr.create(**data)


class TestBook:
    def test_create_book(self):
        name = 'Test Book'
        book_obj = models.Book.objects.create(name=name)
        book_id = book_obj.book_id
        now = book_obj.created_at
        data = {'book_id': book_id, 'name': name, 'created_at': now}
        assert models.Book.objects.filter(**data).exists()

    def test_uniqueness(self):
        name = 'Test Book'
        models.Book.objects.create(name=name)
        with pytest.raises(IntegrityError):
            models.Book.objects.create(name=name)


accounttype = {
        'account_type': 'Income',
        'sign': True,
        'credit_term': 'income',
        'debit_term': 'expense',
    }


class TestAccountType:
    mgr = models.AccountType.objects

    def test_create_accounttype(self):
        self.mgr.create(**accounttype)
        assert self.mgr.filter(**accounttype).exists()

    def test_uniqueness(self):
        self.mgr.create(**accounttype)
        with pytest.raises(IntegrityError):
            self.mgr.create(
                    account_type='Income',
                    sign=False,
                    credit_term='credit',
                    debit_term='debit',
                )


class TestAccount:
    mgr = models.Account.objects

    def setup(self):
        self.book = models.Book.objects.create(name='Test Book')
        self.currency = models.Currency.objects.create(**currency)
        self.accounttype = models.AccountType.objects.create(**accounttype)
        self.data = {
                'name': 'Salary',
                'book': self.book,
                'account_type': self.accounttype,
                'currency': self.currency,
                'description': 'Salary account',
            }

    def test_create_account(self):
        self.mgr.create(**self.data)

    def test_create_with_empty_description(self):
        data = self.data.copy()
        del data['description']
        self.mgr.create(**data)

    def test_uniqueness(self):
        self.mgr.create(**self.data)
        data = self.data.copy()
        data['name'] = 'Something different'
        self.mgr.create(**data)
        data = self.data.copy()
        data['book'] = models.Book.objects.create(name='Different Book')
        self.mgr.create(**data)
        with pytest.raises(IntegrityError):
            self.mgr.create(**self.data)
