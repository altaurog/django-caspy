from datetime import timedelta
import mock
import pytest
from django.utils import timezone
from caspy import models

pytestmark = pytest.mark.django_db()

class TestCurrency:
    def test_create_currency(self):
        currency_data = {
                'code': 'MM',
                'shortcut': 'M',
                'symbol': 'M',
                'long_name': 'Monopoly Money',
            }
        cur_obj = models.Currency.objects.create(**currency_data)
        assert models.Currency.objects.filter(**currency_data).exists()
        assert str(cur_obj) == 'MM'

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
