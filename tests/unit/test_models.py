import pytest
from caspy import models

@pytest.mark.django_db()
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



