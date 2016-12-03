from django.conf.urls import  include, url # patterns
from django.http import HttpResponseRedirect
from django.views.static import serve
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns =[ #patterns('',
    # Examples:
    # url(r'^$', 'upload.views.home', name='home'),

    url(r'^$', lambda x: HttpResponseRedirect('/upload/new/')),
    url(r'^upload/', include('fileupload.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]#)

from os.path import join, abspath, dirname

urlpatterns += url(r'^media/(.*)$', serve, {'document_root': join(abspath(dirname(__file__)), 'media')}),
#)

#urlpatterns += #patterns('',
#    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': join(abspath(dirname(__file__)), 'media')}),
#)
