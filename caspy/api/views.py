from rest_framework import generics
from rest_framework import response
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
    serializer_class = serializers.AnnotatedAccountSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        accountlist = []
        for path in models.Account.tree.paths(queryset):
            account = path[-1]
            account.path = '::'.join([a.name for a in path])
            if len(path) > 1:
                account.parent_id = path[-2].account_id
            else:
                account.parent_id = None
            accountlist.append(account)
        serializer = self.get_serializer(accountlist, many=True)
        return response.Response(serializer.data)


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer
