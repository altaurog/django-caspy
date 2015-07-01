from rest_framework import serializers
from caspy.domain import models as dm


class DomainModelSerializer(serializers.Serializer):
    def create(self, validated_data):
        return self._domain_model(**validated_data)

    def update(self, instance, validated_data):
        return instance.copy(**validated_data)


class CurrencySerializer(DomainModelSerializer):
    _domain_model = dm.Currency
    cur_code = serializers.CharField(max_length=8)
    shortcut = serializers.CharField(max_length=1, required=False)
    symbol = serializers.CharField(max_length=24, required=False)
    long_name = serializers.CharField(max_length=128, required=False)


class BookSerializer(DomainModelSerializer):
    _domain_model = dm.Book
    book_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=64)
    created_at = serializers.DateTimeField(read_only=True)


class AccountTypeSerializer(DomainModelSerializer):
    _domain_model = dm.AccountType
    account_type = serializers.CharField(max_length=128)
    sign = serializers.BooleanField()
    credit_term = serializers.CharField(max_length=32)
    debit_term = serializers.CharField(max_length=32)

    def __init__(self, *args, **kwargs):
        """
        Hack to make required BooleanField work
        (When passing a MergeDict to the serializer, it behaves
        as if the field is present even when it's not.)
        """
        if 'data' in kwargs:
            kwargs['data'] = dict(kwargs['data'].items())
        super(AccountTypeSerializer, self).__init__(*args, **kwargs)


class AccountSerializer(DomainModelSerializer):
    _domain_model = dm.Account
    account_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=64)
    book = serializers.IntegerField()
    account_type = serializers.CharField(max_length=128)
    currency = serializers.CharField(max_length=8)
    description = serializers.CharField(max_length=255, required=False)
    path = serializers.CharField(read_only=True)
    parent_id = serializers.IntegerField(allow_null=True)
