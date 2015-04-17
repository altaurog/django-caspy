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

class Node:
    def __init__(self, pk, parent_id, depth):
        self.pk = pk
        self.parent_id = parent_id
        self.depth = depth

    def __repr__(self): return 'Node(%s)' % self.pk

class TestClosure:
    def test_make_paths(self):
        a = Node(0, None, 0)  # a - b - c
        b = Node(1, 0, 1)     #  \   \
        c = Node(2, 1, 2)     #   d   e
        d = Node(3, 0, 1)
        e = Node(4, 1, 2)
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
