import functools
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from .. import models
from . import serializers


@api_view(('GET',))
def api_root(request, format=None):
    rev = functools.partial(reverse, request=request, format=format)
    return Response({
            'currency': rev('api-currency-list'),
        })


class CurrencyList(generics.ListCreateAPIView):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class CurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer
