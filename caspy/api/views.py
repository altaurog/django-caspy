try:
    from urllib.parse import unquote  # python3
except ImportError:
    from urllib import unquote  # python2
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from .. import models
from . import serializers


@api_view(('GET',))
def api_root(request, format=None):
    def rev(viewname, **kwargs):
        url = reverse(viewname, kwargs=kwargs, request=request, format=format)
        return unquote(url)

    return Response({
        'currency': rev('api-currency-detail', pk=':code'),
    })


class CurrencyList(generics.ListCreateAPIView):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer


class CurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Currency.objects.all()
    serializer_class = serializers.CurrencySerializer
