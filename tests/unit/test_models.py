# vim:fileencoding=utf-8
from __future__ import unicode_literals
from caspy import models, closure
from caspy import str


class TestAccount:
    def test_str(self):
        account_obj = models.Account(name='Salary')
        assert str(account_obj) == 'Salary'

    def test_unicode(self):
        account_obj = models.Account(name='משכורת')
        assert str(account_obj) == 'משכורת'


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

        def __repr__(self):
            return 'Node(%s)' % self.pk

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
