from rest_framework import serializers
from caspy import models
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
        (MergeDict seems to cause the problem)
        """
        if 'data' in kwargs:
            kwargs['data'] = dict(kwargs['data'].items())
        super(AccountTypeSerializer, self).__init__(*args, **kwargs)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account


class AnnotatedAccountSerializer(AccountSerializer):
    path = serializers.CharField(read_only=True)
    parent_id = serializers.IntegerField(allow_null=True)

    def validate(self, data):
        book_id = data['book']
        parent_id = data.pop('parent_id')
        if parent_id is None:
            return data
        try:
            qargs = {'account_id': parent_id, 'book': book_id}
            data['parent'] = models.Account.objects.get(**qargs)
            return data
        except models.Account.DoesNotExist:
            raise serializers.ValidationError('Invalid parent account id')

    def create(self, validated_data):
        parent = validated_data.pop('parent', None)
        child = super(AnnotatedAccountSerializer, self).create(validated_data)
        if parent is not None:
            models.Account.tree.attach(child, parent)
        return child

    def update(self, instance, validated_data):
        new_parent = validated_data.pop('parent', None)
        super(AnnotatedAccountSerializer, self).update(instance,
                                                       validated_data)
        tree = models.Account.tree
        old_parent_id = tree.parent_id(instance)
        if new_parent is None:
            if old_parent_id is not None:
                tree.detach(instance)
        else:
            if old_parent_id != new_parent.account_id:
                if old_parent_id is not None:
                    tree.detach(instance)
                tree.attach(instance, new_parent)
        return instance
