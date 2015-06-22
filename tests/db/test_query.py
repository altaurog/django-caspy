from datetime import datetime
import pytest
from caspy import query, models
from caspy.domain import models as dm
from testapp import factories

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
            self.query_obj.delete(db_o.pk)
            assert not qset.exists()

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
    query_obj = query.accountttype
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
