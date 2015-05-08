# vim:fileencoding=utf-8
from __future__ import unicode_literals
from datetime import timedelta
from django.utils import timezone
from caspy import models, closure

try:
    to_string = unicode  # 2
except NameError:
    to_string = str


class TestCurrency:
    def test_str(self):
        "String representation should be currency code"
        cur_obj = models.Currency(cur_code='USD')
        assert to_string(cur_obj) == 'USD'


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

    def test_str(self):
        book_obj = models.Book(name='Test Book')
        assert to_string(book_obj) == 'Test Book'

    def test_unicode(self):
        book_obj = models.Book(name='שנת 2015')
        assert to_string(book_obj) == 'שנת 2015'


class TestAccountType:
    def test_str(self):
        at_obj = models.AccountType(account_type='Income')
        assert to_string(at_obj) == 'Income'

    def test_unicode(self):
        at_obj = models.AccountType(account_type='הוצאות')
        assert to_string(at_obj) == 'הוצאות'


class TestAccount:
    def test_str(self):
        account_obj = models.Account(name='Salary')
        assert to_string(account_obj) == 'Salary'

    def test_unicode(self):
        account_obj = models.Account(name='משכורת')
        assert to_string(account_obj) == 'משכורת'


class TestAccountTree:
    tree = models.Account.tree

    class Node:
        def __init__(self, account_id, name):
            self.account_id = account_id
            self.name = name

    def setup(self):
        self.a = self.Node(0, 'A')
        self.b = self.Node(1, 'B')
        self.c = self.Node(2, 'C')

    def test_path_name(self):
        assert self.tree.path_name([self.a]) == 'A'
        assert self.tree.path_name([self.a, self.b]) == 'A::B'
        assert self.tree.path_name([self.a, self.b, self.c]) == 'A::B::C'

    def test_path_parent(self):
        assert self.tree.path_parent([self.a]) == None
        assert self.tree.path_parent([self.a, self.b]) == 0
        assert self.tree.path_parent([self.a, self.b, self.c]) == 1

    def test_annotate(self):
        a = self.tree.annotate([self.a])
        assert a is self.a
        assert a.parent_id is None
        assert a.path == 'A'
        b = self.tree.annotate([self.a, self.b])
        assert b is self.b
        assert b.parent_id == 0
        assert b.path == 'A::B'
        c = self.tree.annotate([self.a, self.b, self.c])
        assert c is self.c
        assert c.parent_id == 1
        assert c.path == 'A::B::C'


class TestClosure:
    class Node:
        def __init__(self, pk, parent_id, depth):
            self.pk = pk
            self.parent_id = parent_id
            self.depth = depth

        def __repr__(self): return 'Node(%s)' % self.pk

    def test_make_paths(self):
        a = self.Node(0, None, 0)
        b = self.Node(1, 0, 1)
        c = self.Node(2, 1, 2)
        d = self.Node(3, 0, 1)
        e = self.Node(4, 1, 2)
        # The tree looks like this:
        #    a - b - c
        #     \   \
        #      d   e
        objects = [e, c, d, b, a]
        paths = closure.make_paths(objects)
        expected = set((
                (a,),
                (a, b),
                (a, d),
                (a, b, c),
                (a, b, e),
            ))
        assert set(map(tuple, paths)) == expected
