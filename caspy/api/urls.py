from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.api_root, name='api-root'),
    url(r'^currency/$', views.CurrencyList.as_view(), name='api-currency-list'),
)
