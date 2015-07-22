from datetime import datetime
import pytest
from django.db import connection
from caspy import query, models
from caspy.domain import models as dm
from testapp import factories, fixtures, set_constraints_immediate

pytestmark = pytest.mark.django_db()


class BaseTestQuery:
    def setup(self):
        self.db_objs = self.factory_class.create_batch(self.count)

    def test_get_all(self):
        ol = list(self.query_obj.all())
        assert len(ol) == self.count
        for i, o in enumerate(ol):
            self.check_match(o, self.db_objs[i])

    def test_get_one(self):
        for i, db_o in enumerate(self.db_objs):
            o = self.query_obj.get(db_o.pk)
            self.check_match(o, db_o)

    def test_update(self):
        for i, db_o in enumerate(self.db_objs):
            o = self.modified_domain_object(i, db_o.pk)
            qset = self.obj_qset(o)
            assert not qset.exists()
            self.query_obj.save(o)
            assert qset.exists()

    def test_create(self):
        o = self.new_domain_object()
        qset = self.obj_qset(o)
        assert not qset.exists()
        self.query_obj.save(o)
        assert qset.exists()

    def test_delete(self):
        for db_o in self.db_objs:
            qset = self.pk_qset(db_o.pk)
            assert qset.exists()
            assert self.query_obj.delete(db_o.pk)
            assert not qset.exists()

    def test_get_not_exists(self):
        assert self.query_obj.get('100') is None

    def test_delete_not_exists(self):
        assert not self.query_obj.delete('100')

    def pk_qset(self, pk):
        return self.orm_filter(pk=pk)

    def obj_qset(self, domain_object):
        return self.orm_filter(**domain_object.dict())


class TestCurrencyQuery(BaseTestQuery):
    count = 3
    query_obj = query.currency
    domain_model = dm.Currency
    factory_class = factories.CurrencyFactory
    orm_filter = models.Currency.objects.filter

    def check_match(self, o, db_o):
        assert isinstance(o, self.domain_model)
        assert o.cur_code == db_o.cur_code
        assert o.shortcut == db_o.shortcut
        assert o.symbol == db_o.symbol
        assert o.long_name == db_o.long_name

    def new_domain_object(self):
        return self.domain_model(
                    cur_code='ALT',
                    shortcut='@',
                    symbol='AL',
                    long_name='Aryeh Leib Currency',
                )

    def modified_domain_object(self, i, pk):
        s = chr(ord('!') + i)
        return self.domain_model(
                    cur_code=pk,
                    shortcut=s,
                    symbol=s,
                    long_name='Test Currency %d' % i,
                )


class TestBookQuery(BaseTestQuery):
    count = 2
    query_obj = query.book
    domain_model = dm.Book
    factory_class = factories.BookFactory
    orm_filter = models.Book.objects.filter

    def check_match(self, o, db_o):
        assert isinstance(o, self.domain_model)
        assert o.book_id == db_o.book_id
        assert o.name == db_o.name
        assert o.created_at == db_o.created_at

    def new_domain_object(self):
        return self.domain_model(
                    book_id=136,
                    name='Aryeh Leib Special Test Book',
                    created_at='2023-08-21',
                )

    def modified_domain_object(self, i, pk):
        x = i + 1
        return self.domain_model(
                    book_id=pk,
                    name='Test Update %d' % i,
                    created_at=datetime(2000 + x, x, x, x, x),
                )


class TestAccountTypeQuery(BaseTestQuery):
    count = 4
    query_obj = query.accounttype
    domain_model = dm.AccountType
    factory_class = factories.AccountTypeFactory
    orm_filter = models.AccountType.objects.filter

    def check_match(self, o, db_o):
        assert isinstance(o, self.domain_model)
        assert o.account_type == db_o.account_type
        assert o.sign == db_o.sign
        assert o.credit_term == db_o.credit_term
        assert o.debit_term == db_o.debit_term

    def new_domain_object(self):
        return self.domain_model(
                    account_type='Asset',
                    sign=False,
                    credit_term='decrease',
                    debit_term='increase',
                )

    def modified_domain_object(self, i, pk):
        return self.new_domain_object().copy(account_type=pk)


class TestAccountQuery:
    query_obj = query.account

    def setup(self):
        set_constraints_immediate(connection)
        instances = fixtures.test_fixture()
        self.book = instances['books'][0]
        self.income = instances['accounts'][0]
        self.salary = instances['accounts'][1]
        self.tips = instances['accounts'][2]
        self.citibank = instances['accounts'][3]

    def test_get_book(self):
        qres = self.query_obj.all(book_id=self.book.book_id)
        ol = sorted(qres, key=lambda a: a.name)
        assert len(ol) == 4
        assert all(isinstance(o, dm.Account) for o in ol)
        assert ol[0].account_id == self.citibank.account_id
        assert ol[0].name == 'Citibank'
        assert ol[0].book == self.citibank.book_id
        assert ol[0].account_type == self.citibank.account_type_id
        assert ol[0].currency == self.citibank.currency_id
        assert ol[0].description == 'Citibank Test Account'
        assert ol[0].parent_id is None
        assert ol[0].path == 'Citibank'
        assert ol[1].account_id == self.income.account_id
        assert ol[1].name == 'Income'
        assert ol[1].book == self.income.book_id
        assert ol[1].account_type == self.income.account_type_id
        assert ol[1].currency == self.income.currency_id
        assert ol[1].description == 'Income Test Account'
        assert ol[1].parent_id is None
        assert ol[1].path == 'Income'
        assert ol[2].account_id == self.salary.account_id
        assert ol[2].name == 'Salary'
        assert ol[2].book == self.salary.book_id
        assert ol[2].account_type == self.salary.account_type_id
        assert ol[2].currency == self.salary.currency_id
        assert ol[2].description == 'Salary Test Account'
        assert ol[2].parent_id == self.income.pk
        assert ol[2].path == 'Income::Salary'

    def test_get_one(self):
        book_id = self.tips.book_id
        account_id = self.tips.account_id
        o = self.query_obj.get(book_id, account_id)
        assert isinstance(o, dm.Account)
        assert o.account_id == account_id
        assert o.name == 'Tips'
        assert o.book == book_id
        assert o.account_type == self.tips.account_type_id
        assert o.currency == self.tips.currency_id
        assert o.description == 'Tips Test Account'
        assert o.parent_id is None
        assert o.path == 'Tips'

    def test_get_one_not_exists(self):
        book_id = self.tips.book_id
        o = self.query_obj.get(book_id, -1)
        assert o is None

    def test_create_no_parent(self):
        currency = factories.CurrencyFactory()
        o = dm.Account(
                    name='Other',
                    account_type=self.salary.account_type_id,
                    currency=currency.cur_code,
                    description='Other description',
                    book=self.salary.book_id,
                )
        qset = models.Account.objects.filter(
                name=o.name,
                description=o.description,
                account_type=self.salary.account_type_id,
                currency=currency,
                book=self.salary.book,
            )
        assert not qset.exists()
        self.query_obj.save(o)
        assert qset.exists()

    def test_create_with_parent(self):
        currency = factories.CurrencyFactory()
        o = dm.Account(
                    name='Example',
                    account_type=self.salary.account_type_id,
                    currency=currency.cur_code,
                    description='Example description',
                    book=self.salary.book_id,
                    parent_id=self.salary.account_id,
                )
        qset = models.Account.objects.filter(
                name=o.name,
                description=o.description,
                account_type=self.salary.account_type_id,
                currency=currency,
                book=self.salary.book,
            )
        assert not qset.exists()
        self.query_obj.save(o)
        assert qset.exists()
        o = self.query_obj.get(self.salary.book_id, qset.get().pk)
        assert o.parent_id == self.salary.account_id
        assert o.path == 'Income::Salary::Example'

    @pytest.mark.parametrize('field', ('currency', 'book', 'account_type'))
    def test_create_with_reference_not_exists(self, field):
        currency = factories.CurrencyFactory()
        o = dm.Account(
                    name='Example',
                    account_type=self.salary.account_type_id,
                    currency=currency.cur_code,
                    description='Example description',
                    book=self.salary.book_id,
                    parent_id=self.salary.account_id,
                )
        setattr(o, field, 1000)
        with pytest.raises(query.IntegrityError):
            self.query_obj.save(o)

    def test_update_with_parent(self):
        account_type = factories.AccountTypeFactory(account_type='Bank Accont')
        currency = factories.CurrencyFactory()
        o = dm.Account(
                account_id=self.tips.account_id,
                name='Acme',
                account_type=account_type.account_type,
                currency=currency.cur_code,
                description='Modified description',
                book=self.salary.book_id,
                parent_id=self.salary.account_id,
            )
        qset = models.Account.objects.filter(
                account_id=o.account_id,
                name=o.name,
                description=o.description,
                account_type=account_type,
                currency=currency,
                book=self.salary.book,
            )
        assert not qset.exists()
        self.query_obj.save(o)
        assert qset.exists()
        o = self.query_obj.get(o.book, o.account_id)
        assert o.path == 'Income::Salary::Acme'

    def test_update_no_parent(self):
        book_id = self.salary.book_id
        account_id = self.salary.account_id
        o = self.query_obj.get(book_id, account_id)
        assert o.path == 'Income::Salary'
        o.parent_id = None
        self.query_obj.save(o)
        o = self.query_obj.get(o.book, o.account_id)
        assert o.path == 'Salary'

    def test_delete(self):
        for instance in (self.salary, self.income, self.tips):
            qset = models.Account.objects.filter(pk=instance.pk)
            assert qset.exists()
            assert self.query_obj.delete(instance.book_id, instance.pk)
            assert not qset.exists()

    def test_delete_not_exists(self):
        book_id = self.tips.book_id
        account_id = self.tips.account_id
        assert not self.query_obj.delete(book_id, account_id + 100)
