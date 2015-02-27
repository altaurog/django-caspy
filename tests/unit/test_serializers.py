import pytest
from caspy.api import serializers
from caspy import models

pytestmark = pytest.mark.django_db

currency_data = {
        'code': 'MM',
        'shortcut': 'M',
        'symbol': 'M',
        'long_name': 'Monopoly Money',
    }


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
        obj = models.Currency.objects.create(**currency_data)
        data = currency_data.copy()
        data.update({'symbol': 'm', 'long_name': 'Play Money'})
        serializer = serializers.CurrencySerializer(obj, data=data)
        assert serializer.is_valid()  # updating existing currency
        instance = serializer.save()
        assert instance is obj
        assert models.Currency.objects.filter(**data).exists()

    def test_pk_unique(self):
        models.Currency.objects.create(**currency_data)
        serializer = serializers.CurrencySerializer(data=currency_data)
        assert not serializer.is_valid()  # must request update explicitly

    def test_deserialize(self):
        obj = models.Currency.objects.create(**currency_data)
        serializer = serializers.CurrencySerializer(obj)
        assert serializer.data == currency_data


class TestBookSerializer:
    def test_valid_without_date(self):
        data = {'name': 'Test Book'}
        serializer = serializers.BookSerializer(data=data)
        assert serializer.is_valid()
