import mock
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
    def setup(self):
        self.now = timezone.now()    # get an aware timezone

    def test_null_created_at(self):
        "If created_at isn't set, it should be set to now"
        book_obj = models.Book(name='Test Book')
        with mock.patch.object(timezone, 'now', return_value=self.now):
            book_obj.set_created_at()
        assert book_obj.created_at == self.now

    def test_nonnull_created_at(self):
        return_value = self.now + timedelta(1)
        book_obj = models.Book(name='Test Book', created_at=self.now)
        with mock.patch.object(timezone, 'now', return_value=return_value):
            book_obj.set_created_at()
        assert book_obj.created_at == self.now
