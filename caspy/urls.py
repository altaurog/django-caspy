from django.conf.urls import patterns, include, url

urlpatterns = patterns('',  # noqa
    url(r'^api/', include('caspy.api.urls')),
)
