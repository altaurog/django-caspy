from rest_framework import serializers
from caspy.domain import models as dm


class BlankableCharField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        super(BlankableCharField, self).__init__(*args, **kwargs)
        self.required = False
        self.allow_blank = True


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


class SplitSerializer(DomainModelSerializer):
    _domain_model = dm.Split
    number = BlankableCharField(max_length=32)
    description = BlankableCharField(max_length=128)
    account_id = serializers.IntegerField()
    status = serializers.CharField(max_length=1, required=False)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)


class TransactionSerializer(DomainModelSerializer):
    _domain_model = dm.Transaction
    transaction_id = serializers.IntegerField(read_only=True)
    date = serializers.DateField()
    description = BlankableCharField(max_length=128)
    splits = SplitSerializer(many=True)

    def create(self, validated_data):
        data = validated_data.copy()
        data['splits'] = [dm.Split(**sdata) for sdata in data['splits']]
        return super(TransactionSerializer, self).create(data)

    def update(self, instance, validated_data):
        data = validated_data.copy()
        # this won't support partial split updates
        data['splits'] = [dm.Split(**sdata) for sdata in data['splits']]
        return super(TransactionSerializer, self).update(instance, data)

    class Meta:
        def valid_splits(data):
            if len(data['splits']) == 0:
                raise serializers.ValidationError('Must not be an empty list')

        validators = [valid_splits]
