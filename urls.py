# coding=utf-8
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^wapticker/', include('wapticker.foo.urls')),
	(r'^$', 'wapticker.frontend.views.index'),
	(r'^(?P<pin>\d+)/$', 'wapticker.frontend.views.intern'),
	(r'^manage/$', 'wapticker.frontend.views.manage'),
	(r'^accounts/login/$', 'wapticker.frontend.views.login'),
	(r'^accounts/logout/$', 'wapticker.frontend.views.logout'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
