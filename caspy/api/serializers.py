from rest_framework import serializers
from caspy import models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency


class BookSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.Book


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AccountType


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account


class AnnotatedAccountSerializer(AccountSerializer):
    path = serializers.CharField(read_only=True)
    parent_id = serializers.IntegerField(allow_null=True)

    def validate(self, data):
        book_id = data['book']
        parent_id = data.pop('parent_id')
        try:
            qargs = {'account_id': parent_id, 'book': book_id}
            data['parent'] = models.Account.objects.get(**qargs)
            return data
        except models.Account.DoesNotExist:
            raise serializers.ValidationError('Invalid parent account id')

    def create(self, validated_data):
        parent = validated_data.pop('parent')
        child = super(AnnotatedAccountSerializer, self).create(validated_data)
        models.Account.tree.attach(child, parent)
        return child


