from datetime import datetime
from caspy.domain import models as domain
from caspy import models as db
from caspy import orm


class TestCurrency:
    def test_domain_to_orm(self):
        obj = domain.Currency(
                cur_code='USD',
                shortcut='$',
                symbol='$',
                long_name='US Dollar',
            )
        instance = orm.domain_to_orm(obj)
        assert isinstance(instance, db.Currency)
        assert instance.cur_code == 'USD'
        assert instance.shortcut == '$'
        assert instance.symbol == '$'
        assert instance.long_name == 'US Dollar'

    def test_orm_to_domain(self):
        instance = db.Currency(
                cur_code='USD',
                shortcut='$',
                symbol='$',
                long_name='US Dollar',
            )
        obj = orm.orm_to_domain(instance)
        assert isinstance(obj, domain.Currency)
        assert obj.cur_code == 'USD'
        assert obj.shortcut == '$'
        assert obj.symbol == '$'
        assert obj.long_name == 'US Dollar'


class TestBook:
    the_time = datetime(2015, 6, 7, 13, 30)

    def test_domain_to_orm(self):
        obj = domain.Book(
                name='Test Book',
                created_at=self.the_time,
            )
        instance = orm.domain_to_orm(obj)
        assert isinstance(instance, db.Book)
        assert instance.book_id is None
        assert instance.name == 'Test Book'
        assert instance.created_at == self.the_time
        obj.book_id = 1
        instance = orm.domain_to_orm(obj)
        assert instance.book_id == 1

    def test_orm_to_domain(self):
        instance = db.Book(
                book_id=2,
                name='Test Book',
                created_at=self.the_time,
            )
        obj = orm.orm_to_domain(instance)
        assert isinstance(obj, domain.Book)
        assert obj.book_id == 2
        assert obj.name == 'Test Book'
        assert obj.created_at == self.the_time


class TestAccountType:
    def test_domain_to_orm(self):
        obj = domain.AccountType(
                account_type='Income',
                sign=True,
                credit_term='income',
                debit_term='expense',
            )
        instance = orm.domain_to_orm(obj)
        assert isinstance(instance, db.AccountType)
        assert instance.account_type == 'Income'
        assert instance.sign is True
        assert instance.credit_term == 'income'
        assert instance.debit_term == 'expense'

    def test_orm_to_domain(self):
        instance = db.AccountType(
                account_type='Income',
                sign=True,
                credit_term='income',
                debit_term='expense',
            )
        obj = orm.orm_to_domain(instance)
        assert isinstance(obj, domain.AccountType)
        assert obj.account_type == 'Income'
        assert obj.sign is True
        assert obj.credit_term == 'income'
        assert obj.debit_term == 'expense'


class TestAccount:
    book = domain.Book(book_id=3, name='Test Book')
    currency = domain.Currency(cur_code='USD', symbol='$')
    account_type = domain.AccountType(account_type='Expense')

    def test_deep_domain_to_orm(self):
        obj = domain.Account(
                    account_id=10,
                    name='Education',
                    book=self.book,
                    account_type=self.account_type,
                    currency=self.currency,
                    description='Education Expense',
                )
        instance = orm.domain_to_orm(obj)
        assert isinstance(instance, db.Account)
        assert isinstance(instance.book, db.Book)
        assert instance.book.book_id == 3
        assert instance.book.name == 'Test Book'
        assert isinstance(instance.currency, db.Currency)
        assert isinstance(instance.account_type, db.AccountType)
        assert instance.account_id == 10
        assert instance.name == 'Education'
        assert instance.description == 'Education Expense'

    def test_shallow_domain_to_orm(self):
        obj = domain.Account(
                    account_id=10,
                    name='Education',
                    book=3,
                    account_type='Expense',
                    currency='USD',
                    description='Education Expense',
                )
        instance = orm.domain_to_orm(obj)
        assert isinstance(instance, db.Account)
        assert instance.book_id == 3
        assert instance.currency_id == 'USD'
        assert instance.account_type_id == 'Expense'
        assert instance.account_id == 10
        assert instance.name == 'Education'
        assert instance.description == 'Education Expense'

    def test_shallow_orm_to_domain(self):
        instance = db.Account(
                    account_id=11,
                    name='Utilities',
                    book_id=3,
                    account_type_id='Expense',
                    currency_id='USD',
                    description='Education Expense',
                )
        obj = orm.orm_to_domain(instance)
        assert isinstance(obj, domain.Account)
        assert obj.account_id == 11
        assert obj.name == 'Utilities'
        assert obj.book == 3
        assert obj.account_type == 'Expense'
        assert obj.currency == 'USD'
        assert obj.description == 'Education Expense'

    def test_deep_orm_to_domain(self):
        book = db.Book(book_id=3, name='Test Book')
        account_type = db.AccountType(account_type='Expense')
        currency = db.Currency(cur_code='NIS')
        instance = db.Account(
                    account_id=11,
                    name='Utilities',
                    book=book,
                    account_type=account_type,
                    currency=currency,
                    description='Education Expense',
                )
        obj = orm.orm_to_domain(instance)
        assert isinstance(obj, domain.Account)
        assert obj.account_id == 11
        assert obj.name == 'Utilities'
        assert obj.book == 3
        assert obj.account_type == 'Expense'
        assert obj.currency == 'NIS'
        assert obj.description == 'Education Expense'
