from rest_framework import serializers
from caspy import models

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
