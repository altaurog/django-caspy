from django.conf.urls import patterns, include, url

urlpatterns = patterns('',  # noqa
    url(r'^$', 'caspy.views.home'),
    url(r'^api/', include('caspy.api.urls')),
)
