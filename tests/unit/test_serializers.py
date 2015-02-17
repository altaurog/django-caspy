import pytest
from caspy.api import serializers
from caspy import models

currency_data = {
        'code': 'MM',
        'shortcut': 'M',
        'symbol': 'M',
        'long_name': 'Monopoly Money',
    }

pytestmark = pytest.mark.django_db

class TestCurrencySerializer:
    """
    All a bit overkill, perhaps, but a good way for me to learn
    about the serializer class.
    """
    @pytest.mark.parametrize("field_omitted", currency_data.keys())
    def test_invalid_if(self, field_omitted):
        data = currency_data.copy()
        del data[field_omitted]
        serializer = serializers.CurrencySerializer(data=data)
        assert not serializer.is_valid()

    def test_create(self):
        serializer = serializers.CurrencySerializer(data=currency_data)
        assert serializer.is_valid()
        instance = serializer.save()
        assert isinstance(instance, models.Currency)
        for k, v in currency_data.items():
            assert getattr(instance, k) == v
        assert models.Currency.objects.filter(**currency_data).exists()

    def test_update(self):
        data = currency_data.copy()
        data['code'] = 'USD'
        usd = models.Currency.objects.get(code='USD')
        serializer = serializers.CurrencySerializer(usd, data=data)
        assert serializer.is_valid()  # updating existing currency
        instance = serializer.save()
        assert instance is usd
        assert models.Currency.objects.filter(**data).exists()

    def test_pk_unique(self):
        data = currency_data.copy()
        data['code'] = 'USD'
        serializer = serializers.CurrencySerializer(data=data)
        assert not serializer.is_valid()  # must request update explicitly

    def test_deserialize(self):
        usd = models.Currency.objects.get(code='USD')
        serializer = serializers.CurrencySerializer(usd)
        data = {
                'code': usd.code,
                'shortcut': usd.shortcut,
                'symbol': usd.symbol,
                'long_name': usd.long_name,
            }
        assert serializer.data == data

