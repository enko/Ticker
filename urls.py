# coding=utf-8
from django.conf.urls.defaults import *
from django.conf import settings

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

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
