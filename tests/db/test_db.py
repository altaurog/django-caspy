import pytest
from django.db import connection, IntegrityError
from django.forms.models import model_to_dict
from caspy import models

import testapp.models
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


class TestAccountPath:
    def setup(self):
        self.book = factories.BookFactory()
        kwargs = {
            'book': self.book,
            'currency': factories.CurrencyFactory(cur_code='USD'),
            'account_type': factories.AccountTypeFactory(
                                            account_type='Income'),
        }
        self.income = factories.AccountFactory(name='Income', **kwargs)
        self.salary = factories.AccountFactory(name='Salary', **kwargs)
        self.tips = factories.AccountFactory(name='Tips', **kwargs)
        models.Account.tree.attach(self.salary, self.income)
        models.Account.tree.attach(self.tips, self.income)

    def test_load(self):
        accounts = sorted(models.Account.tree.load(), key=lambda a: a.name)
        expected_paths = ['Income', 'Income::Salary', 'Income::Tips']
        assert [a.path for a in accounts] == expected_paths
        parent_id = self.income.account_id
        expected_parents = [None, parent_id, parent_id]
        assert [a.parent_id for a in accounts] == expected_parents

    def test_load_one(self):
        account = models.Account.tree.load_one(self.book.pk, self.tips.pk)
        assert account.path == 'Income::Tips'
        assert account.parent_id == self.income.pk

    def test_load_one_not_exists(self):
        book_id = self.book.pk
        account_id = self.tips.pk + 100
        account = models.Account.tree.load_one(book_id, account_id)
        assert account is None


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
        assert self.treemgr._pk_column() == 'id'

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

    def test_get_one_path(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        self.treemgr.attach(c, b)
        self.treemgr.attach(b, a)
        paths = self.treemgr.one_path(c.pk)
        assert list(paths) == [a, b, c]

    def test_get_one_path_with_filter(self):
        a, b, c = factories.ThingFactory.create_batch(3)
        self.treemgr.attach(c, b)
        self.treemgr.attach(b, a)
        paths = self.treemgr.one_path(c.pk, pk__gt=a.pk)
        assert list(paths) == [b, c]

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
