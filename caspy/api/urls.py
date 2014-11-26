from django.conf.urls import patterns, url

urlpatterns = patterns('caspy.api.views',
    url(r'^$', 'api_root', name='api-root'),
)
