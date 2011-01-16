# coding=utf-8
from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from frontend.handlers import EntryHandler, ArbitraryDataHandler

auth = HttpBasicAuthentication(realm="Ticker API")
ad = { 'authentication': auth }

#blogpost_resource = Resource(handler=EntryHandler, **ad)
blogpost_resource = Resource(handler=EntryHandler)
arbitrary_resource = Resource(handler=ArbitraryDataHandler, **ad)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^Ticker/', include('Ticker.foo.urls')),
	(r'^$', 'Ticker.frontend.views.index'),
	(r'^(?P<pin>\d+)/$', 'Ticker.frontend.views.index'),
	(r'^manage/$', 'Ticker.frontend.views.manage'),
	(r'^accounts/login/$', 'Ticker.frontend.views.login'),
	(r'^accounts/logout/$', 'Ticker.frontend.views.logout'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^api/entries/(?P<id>[^/]+)/$', blogpost_resource), 
    url(r'^api/entries/$', blogpost_resource), 
    # url(r'^other/(?P<username>[^/]+)/(?P<data>.+)/$', arbitrary_resource), 
)
