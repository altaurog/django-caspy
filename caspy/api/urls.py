import re
from django.conf.urls import patterns, url
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import views


urlre_p1 = re.compile(r'\(\?P<\w+>.*\(\?#(:\w+)\)\)')
urlre_p2 = re.compile(r'^\^|\$$')


def rev(viewname):
    for urlp in urlpatterns:
        if urlp.name == viewname:
            return urlre_p2.sub('', urlre_p1.sub(r'\g<1>', urlp._regex))
    raise RuntimeError("No reverse match for %s" % viewname)


def response(path, endpoints):
    return Response({name: path + p for name, p in endpoints.items()})


@api_view(('GET',))
def api_root(request):
    return response(request.path, {
        'currency': rev('api-currency-detail'),
        'book': rev('api-book-detail'),
    })


urlpatterns = patterns('',  # noqa
    url(r'^$',
        api_root,
        name='api-root'),
    url(r'^currency/$',
        transaction.atomic(views.CurrencyList.as_view()),
        name='api-currency-list'),
    url(r'^currency/(?P<pk>[A-Z]+(?#:cur_code))/$',
        transaction.atomic(views.CurrencyDetail.as_view()),
        name='api-currency-detail'),
    url(r'^book/$',
        views.BookList.as_view(),
        name='api-book-list'),
    url(r'^book/(?P<pk>\d+(?#:book_id))/$',
        views.BookDetail.as_view(),
        name='api-book-detail'),
)
