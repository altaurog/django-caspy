from rest_framework import generics, response, status, views
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

    def post(self, request, book_id, format=None):
        data = request.data.copy()
        data['book'] = book_id
        data.setdefault('parent_id', None)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            account = serializer.save()
            data['account_id'] = account.account_id
            return response.Response(data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(views.APIView):
    serializer_class = serializers.AnnotatedAccountSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return models.Account.objects.filter(book=book_id)

    def put(self, request, book_id, pk, format=None):
        qargs = {'pk': pk, 'book': book_id}
        account = models.Account.objects.get(**qargs)
        data = request.data.copy()
        data['book'] = book_id
        serializer = self.serializer_class(account, data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)
