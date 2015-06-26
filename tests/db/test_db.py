import pytest
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict
from caspy import models

import testapp.models
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

    def test_load(self):
        kwargs = {
            'book': factories.BookFactory(),
            'currency': factories.CurrencyFactory(cur_code='USD'),
            'account_type': factories.AccountTypeFactory(
                                            account_type='Income'),
        }
        income = factories.AccountFactory(name='Income', **kwargs)
        salary = factories.AccountFactory(name='Salary', **kwargs)
        models.Account.tree.attach(salary, income)
        accounts = sorted(models.Account.tree.load(), key=lambda a: a.name)
        assert [a.path for a in accounts] == ['Income', 'Income::Salary']
        assert [a.parent_id for a in accounts] == [None, income.account_id]


class TestClosureTable:
    treemgr = testapp.models.Thing.tree
    pathmgr = testapp.models.ThingPath.objects

    def test_self_path_created(self):
        a = factories.ThingFactory()
        assert self.pathmgr.filter(
                    upper=a, lower=a, length=0,
                ).exists()

    def test_self_path_not_created_twice(self):
        factories.ThingFactory().save()

    def test_attach_leaf(self):
        a, b = factories.ThingFactory.create_batch(2)
        assert self.treemgr.attach(b, a) == 1
        assert self.pathmgr.filter(
                    upper=a, lower=b, length=1,
                ).exists()

    def test_attach_branch(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        assert self.treemgr.attach(c, b) == 1
        assert self.treemgr.attach(b, a) == 2
        assert self.pathmgr.filter(
                    upper=a, lower=c, length=2,
                ).exists()

    def test_path_table(self):
        assert self.treemgr._path_table() == 'testapp_thingpath'

    def test_table(self):
        assert self.treemgr._table() == 'testapp_thing'

    def test_columns(self):
        assert self.treemgr._columns() == ['id', 'name', 'tgroup']

    def test_pk(self):
        assert self.treemgr._pk() == 'id'

    def test_kwargs(self):
        expected = {
                'table': 'testapp_thing',
                'columns': ['id', 'name', 'tgroup'],
                'pk': 'id',
                'path_table': 'testapp_thingpath',
                'select': ('testapp_thing.id, '
                           'testapp_thing.name, '
                           'testapp_thing.tgroup'),
            }
        assert self.treemgr._query_format_kwargs() == expected

    def test_parent_annotated(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        self.treemgr.attach(c, b)
        self.treemgr.attach(b, a)
        paths = list(self.treemgr.parent_annotated())
        paths.sort(key=lambda o: o.name)
        assert [o.depth for o in paths] == [0, 1, 2]
        assert [o.parent_id for o in paths] == [None, a.id, b.id]

    def test_get_parent_id(self):
        a, b = factories.ThingFactory.create_batch(2)
        self.treemgr.attach(b, a)
        assert self.treemgr.parent_id(a) is None
        assert self.treemgr.parent_id(b) == a.id

    def test_get_paths(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        self.treemgr.attach(c, b)
        self.treemgr.attach(b, a)
        paths = self.treemgr.paths()
        assert paths == [[a], [a, b], [a, b, c]]

    def test_get_paths_with_where(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        e, f, g = factories.ThingFactory.create_batch(3, tgroup=2)
        self.treemgr.attach(c, b)
        self.treemgr.attach(b, a)
        self.treemgr.attach(g, f)
        self.treemgr.attach(f, e)
        paths = self.treemgr.paths('WHERE tgroup = %s', [1])
        assert paths == [[a], [a, b], [a, b, c]]

    def test_detach_leaf(self):
        a, b = factories.ThingFactory.create_batch(2)
        self.treemgr.attach(b, a)
        assert self.treemgr.detach(b) == 1
        assert not self.pathmgr.filter(
                    upper=a, lower=b, length=1,
                ).exists()

    def test_detach_branch(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        self.treemgr.attach(c, b)
        self.treemgr.attach(b, a)
        assert self.treemgr.detach(b) == 2
        assert not self.pathmgr.filter(
                    upper=a, lower=c, length=2,
                ).exists()

    def test_delete_middle_node(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        self.treemgr.attach(c, b)
        self.treemgr.attach(b, a)
        b.delete()
        assert not self.pathmgr.filter(
                    upper=a, lower=c, length=2,
                ).exists()
