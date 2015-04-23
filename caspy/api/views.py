from rest_framework import generics, response, views
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


class AccountList(views.APIView):
    serializer_class = serializers.AnnotatedAccountSerializer

    def get(self, request, book_id, format=None):
        accounts = models.Account.tree.load_book(int(book_id))
        serializer = self.serializer_class(accounts, many=True)
        return response.Response(serializer.data)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
