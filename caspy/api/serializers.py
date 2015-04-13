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
