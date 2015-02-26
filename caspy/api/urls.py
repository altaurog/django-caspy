from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',  # noqa
    url(r'^$',
        views.api_root,
        name='api-root'),
    url(r'^currency/$',
        views.CurrencyList.as_view(),
        name='api-currency-list'),
    url(r'^currency/(?P<pk>[A-Z]+)/$',
        views.CurrencyDetail.as_view(),
        name='api-currency-detail'),
)
