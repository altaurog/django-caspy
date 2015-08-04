import pytest
from caspy import models
import testapp.models
from testapp import factories, fixtures

pytestmark = pytest.mark.django_db()


class TestClosureTable:
    treemgr = testapp.models.Thing.tree
    pathmgr = testapp.models.ThingPath.objects

    def test_path_str(self):
        path = testapp.models.ThingPath(upper_id=1, lower_id=2, length=1)
        assert str(path) == '1 2 1'

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


class TestAccountPath:
    def setup(self):
        instances = fixtures.test_fixture()
        self.book = instances['books'][0]
        self.income = instances['accounts'][0]
        self.salary = instances['accounts'][1]
        self.tips = instances['accounts'][2]

    def test_load(self):
        accounts = sorted(models.Account.tree.load(), key=lambda a: a.name)
        expected_paths = [
                'Chase', 'Citibank', 'Income', 'Income::Salary', 'Tips'
            ]
        assert [a.path for a in accounts] == expected_paths
        parent_id = self.income.account_id
        expected_parents = [None, None, None, parent_id, None]
        assert [a.parent_id for a in accounts] == expected_parents

    def test_load_child(self):
        account = models.Account.tree.load_one(self.book.pk, self.salary.pk)
        assert account.path == 'Income::Salary'
        assert account.parent_id == self.income.pk

    def test_load_leaf(self):
        account = models.Account.tree.load_one(self.book.pk, self.tips.pk)
        assert account.path == 'Tips'
        assert account.parent_id is None

    def test_load_one_not_exists(self):
        book_id = self.book.pk
        account_id = self.tips.pk + 100
        account = models.Account.tree.load_one(book_id, account_id)
        assert account is None
