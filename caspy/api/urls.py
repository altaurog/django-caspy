import re
from django.conf.urls import patterns, url
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import views


urlre_p1 = re.compile(r'\(\?P<(\w+)>.*?\)')
urlre_p2 = re.compile(r'^\^|\$$')


def rev(viewname, pk_name):
    def replace(matchobj):
        name = matchobj.group(1)
        if name == 'pk':
            return ':' + pk_name
        return ':' + name
    for urlp in urlpatterns:
        if urlp.name == viewname:
            return urlre_p2.sub('', urlre_p1.sub(replace, urlp._regex))
    raise RuntimeError("No reverse match for %s" % viewname)


def response(path, endpoints):
    return Response({name: path + p for name, p in endpoints.items()})


@api_view(('GET',))
def api_root(request):
    return response(request.path, {
            'currency': rev('api-currency-detail', 'cur_code'),
            'accounttype': rev('api-accounttype-detail', 'account_type'),
            'book': rev('api-book-detail', 'book_id'),
            'account': rev('api-account-detail', 'account_id'),
        })


urlpatterns = patterns('',  # noqa
    url(r'^$',
        api_root,
        name='api-root'),
    url(r'^currency/$',
        transaction.atomic(views.CurrencyList.as_view()),
        name='api-currency-list'),
    url(r'^currency/(?P<pk>[A-Z]+)/$',
        transaction.atomic(views.CurrencyDetail.as_view()),
        name='api-currency-detail'),
    url(r'^book/$',
        views.BookList.as_view(),
        name='api-book-list'),
    url(r'^book/(?P<pk>\d+)/$',
        views.BookDetail.as_view(),
        name='api-book-detail'),
    url(r'^accounttype/$',
        views.AccountTypeList.as_view(),
        name='api-accounttype-list'),
    url(r'^accounttype/(?P<pk>[\w ]+)/$',
        views.AccountTypeDetail.as_view(),
        name='api-accounttype-detail'),
    url(r'^book/(?P<book_id>\d+)/account/$',
        views.AccountList.as_view(),
        name='api-account-list'),
    url(r'^book/(?P<book_id>\d+)/account/(?P<pk>\d+)/$',
        views.AccountDetail.as_view(),
        name='api-account-detail'),
)
