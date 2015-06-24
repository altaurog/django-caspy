from django.http import Http404
from rest_framework import response, status, views
from ..domain import command
from .. import models, query, time
from . import serializers


class BaseAPIView(views.APIView):
    def serialize(self, o, many=False):
        return self.serializer_class(o, many=many).data


class ListView(BaseAPIView):
    def create(self, ser):
        return ser.save()

    def get(self, request, format=None):
        objects = self.query_obj.all()
        data = self.serialize(objects, many=True)
        return response.Response(data)

    def post(self, request, format=None):
        ser = self.serializer_class(data=request.data)
        if not ser.is_valid():
            return response.Response(ser.errors,
                                     status=status.HTTP_400_BAD_REQUEST)
        obj = self.create(ser)
        self.query_obj.save(obj)
        data = self.serialize(obj)
        return response.Response(data, status=status.HTTP_201_CREATED)


class DetailView(BaseAPIView):
    def get(self, request, pk, format=None):
        obj = self.query_obj.get(pk)
        if obj is None:
            raise Http404('Not found')
        data = self.serialize(obj)
        return response.Response(data)

    def put(self, request, pk, format=None):
        obj = self.query_obj.get(pk)
        if obj is None:
            raise Http404('Not found')
        ser = self.serializer_class(obj, data=request.data)
        ser.is_valid()
        updated = ser.save()
        self.query_obj.save(updated)
        data = self.serialize(updated)
        return response.Response(data)

    def delete(self, request, pk, format=None):
        if not self.query_obj.delete(pk):
            raise Http404('Not found')
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class CurrencyList(ListView):
    query_obj = query.currency
    serializer_class = serializers.CurrencySerializer


class CurrencyDetail(DetailView):
    query_obj = query.currency
    serializer_class = serializers.CurrencySerializer


class BookList(ListView):
    query_obj = query.book
    serializer_class = serializers.BookSerializer

    def create(self, ser):
        return command.prepare_book(ser.save(), time.utcnow())


class BookDetail(DetailView):
    query_obj = query.book
    serializer_class = serializers.BookSerializer


class AccountTypeList(ListView):
    query_obj = query.accounttype
    serializer_class = serializers.AccountTypeSerializer


class AccountTypeDetail(DetailView):
    query_obj = query.accounttype
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

    def get_account(self, request, book_id, pk):
        qargs = {'pk': pk, 'book': book_id}
        return models.Account.objects.get(**qargs)

    def put(self, request, book_id, pk, format=None):
        account = self.get_account(request, book_id, pk)
        data = request.data.copy()
        data['book'] = book_id
        serializer = self.serializer_class(account, data=data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors,
                                 status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, book_id, pk, format=None):
        account = self.get_account(request, book_id, pk)
        account.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
