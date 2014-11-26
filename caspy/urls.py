from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # url(r'^$', 'caspysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('caspy.api.urls')),
)
