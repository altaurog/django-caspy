from rest_framework import generics
from .. import models
from . import serializers


class CurrencyList(generics.ListCreateAPIView):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class CurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class BookList(generics.ListCreateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class AccountTypeList(generics.ListCreateAPIView):
    queryset = models.AccountType.objects.all()
    serializer_class = serializers.AccountTypeSerializer


class AccountTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AccountType.objects.all()
    serializer_class = serializers.AccountTypeSerializer


class AccountList(generics.ListCreateAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
