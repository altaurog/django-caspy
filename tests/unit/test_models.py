from datetime import timedelta
from django.utils import timezone
from caspy import models


class TestCurrency:
    currency_data = {
            'code': 'MM',
            'shortcut': 'M',
            'symbol': 'M',
            'long_name': 'Monopoly Money',
        }

    def test_str(self):
        cur_obj = models.Currency(**self.currency_data)
        assert str(cur_obj) == 'MM'


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
