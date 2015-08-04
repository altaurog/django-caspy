from django.db import transaction
from django.http import Http404
from rest_framework import response, status, views
from ..domain import command
from .. import query, time
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
        with transaction.atomic():
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
        if not ser.is_valid():
            return response.Response(ser.errors,
                                     status=status.HTTP_400_BAD_REQUEST)
        updated = ser.save()
        with transaction.atomic():
            self.query_obj.save(updated)
            data = self.serialize(updated)
            return response.Response(data)

    def delete(self, request, pk, format=None):
        with transaction.atomic():
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


class AccountList(ListView):
    query_obj = query.account
    serializer_class = serializers.AccountSerializer

    def get(self, request, book_id, format=None):
        objects = self.query_obj.all(book_id)
        data = self.serialize(objects, many=True)
        return response.Response(data)

    def post(self, request, book_id, format=None):
        data = request.data.copy()
        data['book'] = book_id
        ser = self.serializer_class(data=data)
        if not ser.is_valid():
            return response.Response(ser.errors,
                                     status=status.HTTP_400_BAD_REQUEST)
        obj = self.create(ser)
        with transaction.atomic():
            self.query_obj.save(obj)
            data = self.serialize(obj)
            return response.Response(data, status=status.HTTP_201_CREATED)


class AccountDetail(DetailView):
    query_obj = query.account
    serializer_class = serializers.AccountSerializer

    def get(self, request, book_id, pk, format=None):
        obj = self.query_obj.get(book_id, pk)
        data = self.serialize(obj)
        return response.Response(data)

    def put(self, request, book_id, pk, format=None):
        obj = self.query_obj.get(book_id, pk)
        if obj is None:
            raise Http404('Not found')
        data = request.data.copy()
        data['book'] = book_id
        ser = self.serializer_class(obj, data=data)
        if not ser.is_valid():
            return response.Response(ser.errors,
                                     status=status.HTTP_400_BAD_REQUEST)
        updated = ser.save()
        with transaction.atomic():
            self.query_obj.save(updated)
            data = self.serialize(updated)
            return response.Response(data)

    def delete(self, request, book_id, pk, format=None):
        with transaction.atomic():
            if not self.query_obj.delete(book_id, pk):
                raise Http404('Not found')
            return response.Response(status=status.HTTP_204_NO_CONTENT)


class TransactionList(ListView):
    query_obj = query.transaction
    serializer_class = serializers.TransactionSerializer

    def get(self, request, book_id, format=None):
        objects = self.query_obj.all(book_id)
        data = self.serialize(objects, many=True)
        return response.Response(data)

    def post(self, request, book_id, format=None):
        data = request.data.copy()
        data['book'] = book_id
        ser = self.serializer_class(data=data)
        if not ser.is_valid():
            return response.Response(ser.errors,
                                     status=status.HTTP_400_BAD_REQUEST)
        obj = self.create(ser)
        with transaction.atomic():
            self.query_obj.save(obj)
            data = self.serialize(obj)
            return response.Response(data, status=status.HTTP_201_CREATED)


class TransactionDetail(DetailView):
    query_obj = query.transaction
    serializer_class = serializers.TransactionSerializer

    def get(self, request, book_id, pk, format=None):
        obj = self.query_obj.get(book_id, pk)
        data = self.serialize(obj)
        return response.Response(data)

    def put(self, request, book_id, pk, format=None):
        obj = self.query_obj.get(book_id, pk)
        if obj is None:
            raise Http404('Not found')
        data = request.data.copy()
        data['book'] = book_id
        ser = self.serializer_class(obj, data=data)
        if not ser.is_valid():
            return response.Response(ser.errors,
                                     status=status.HTTP_400_BAD_REQUEST)
        updated = ser.save()
        with transaction.atomic():
            self.query_obj.save(updated)
            data = self.serialize(updated)
            return response.Response(data)

    def delete(self, request, book_id, pk, format=None):
        with transaction.atomic():
            if not self.query_obj.delete(book_id, pk):
                raise Http404('Not found')
            return response.Response(status=status.HTTP_204_NO_CONTENT)
