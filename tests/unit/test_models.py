from datetime import timedelta
import mock
import pytest
from django.db.utils import IntegrityError
from django.utils import timezone
from caspy import models

pytestmark = pytest.mark.django_db()

class TestCurrency:
    mgr = models.Currency.objects
    currency_data = {
            'code': 'MM',
            'shortcut': 'M',
            'symbol': 'M',
            'long_name': 'Monopoly Money',
        }

    def test_create_currency(self):
        cur_obj = self.mgr.create(**self.currency_data)
        assert self.mgr.filter(**self.currency_data).exists()
        assert str(cur_obj) == 'MM'

    unique_fields = ('code', 'shortcut', 'long_name')

    @pytest.mark.parametrize('dupfield', unique_fields)
    def test_uniquness(self, dupfield):
        self.mgr.create(**self.currency_data)
        data = self.currency_data.copy()
        data.update({f: 'A' for f in data.keys() if f != dupfield})
        with pytest.raises(IntegrityError):
            self.mgr.create(**data)

class TestBook:
    def test_create_book(self):
        now = timezone.now()    # get an aware timezone
        name = 'Test Book'
        with mock.patch.object(timezone, 'now', return_value=now):
            book_obj = models.Book.objects.create(name=name)
        book_id = book_obj.book_id
        assert isinstance(book_id, int)
        assert book_obj.created_at == now
        data = {'book_id': book_id, 'name': name, 'created_at': now}
        assert models.Book.objects.filter(**data).exists()
        with mock.patch.object(timezone, 'now', return_value=now + timedelta(1)):
            book_obj.save()
        assert book_obj.created_at == now
        assert models.Book.objects.filter(**data).exists()

    def test_uniqueness(self):
        name = 'Test Book'
        models.Book.objects.create(name=name)
        with pytest.raises(IntegrityError):
            models.Book.objects.create(name=name)
