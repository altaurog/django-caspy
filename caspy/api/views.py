from rest_framework import response, status, views
from ..domain import command
from .. import models, query, time
from . import serializers


class CurrencyList(views.APIView):
    def get(self, request, format=None):
        objects = query.currency.all()
        ser = serializers.CurrencySerializer(objects, many=True)
        return response.Response(ser.data)

    def post(self, request, format=None):
        ser = serializers.CurrencySerializer(data=request.data)
        ser.is_valid()
        obj = ser.save()
        query.currency.save(obj)
        return response.Response(obj.dict(), status=status.HTTP_201_CREATED)


class CurrencyDetail(views.APIView):
    def get(self, request, pk, format=None):
        obj = query.currency.get(pk)
        ser = serializers.CurrencySerializer(obj)
        return response.Response(ser.data)

    def put(self, request, pk, format=None):
        obj = query.currency.get(pk)
        ser = serializers.CurrencySerializer(obj, data=request.data)
        ser.is_valid()
        updated = ser.save()
        query.currency.save(updated)
        return response.Response(updated.dict())

    def delete(self, request, pk, format=None):
        query.currency.delete(pk)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class BookList(views.APIView):
    def _serialize(self, o, many=False):
        return serializers.BookSerializer(o, many=many).data

    def get(self, request, format=None):
        objects = query.book.all()
        data = self._serialize(objects, many=True)
        return response.Response(data)

    def post(self, request, format=None):
        ser = serializers.BookSerializer(data=request.data)
        ser.is_valid()
        obj = command.prepare_book(ser.save(), time.utcnow())
        query.book.save(obj)
        data = self._serialize(obj)
        return response.Response(data, status=status.HTTP_201_CREATED)


class BookDetail(views.APIView):
    def _serialize(self, o, many=False):
        return serializers.BookSerializer(o, many=many).data

    def get(self, request, pk, format=None):
        obj = query.book.get(pk)
        data = self._serialize(obj)
        return response.Response(data)

    def put(self, request, pk, format=None):
        obj = query.book.get(pk)
        ser = serializers.BookSerializer(obj, data=request.data)
        ser.is_valid()
        updated = ser.save()
        query.book.save(updated)
        data = self._serialize(updated)
        return response.Response(data)

    def delete(self, request, pk, format=None):
        query.book.delete(pk)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class AccountTypeList(views.APIView):
    def get(self, request, format=None):
        objects = query.accounttype.all()
        ser = serializers.AccountTypeSerializer(objects, many=True)
        return response.Response(ser.data)

    def post(self, request, format=None):
        ser = serializers.AccountTypeSerializer(data=request.data)
        ser.is_valid()
        obj = ser.save()
        query.accounttype.save(obj)
        return response.Response(obj.dict(), status=status.HTTP_201_CREATED)


class AccountTypeDetail(views.APIView):
    def get(self, request, pk, format=None):
        obj = query.accounttype.get(pk)
        ser = serializers.AccountTypeSerializer(obj)
        return response.Response(ser.data)

    def put(self, request, pk, format=None):
        obj = query.accounttype.get(pk)
        ser = serializers.AccountTypeSerializer(obj, data=request.data)
        ser.is_valid()
        updated = ser.save()
        query.accounttype.save(updated)
        return response.Response(updated.dict())

    def delete(self, request, pk, format=None):
        query.accounttype.delete(pk)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


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
