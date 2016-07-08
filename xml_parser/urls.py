# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('xml_parser.views',
    url(r'^database/$', 'database', name='database'),
        url(r'^myapp/',include('myapp.urls')),

#    url(r'^t(?P<tmhelixtriplet_id>[0-9]+)/$', views.triplet, name='triplet'),
#    url(r'^p(?P<tmhelixpair_id>[0-9]+)/$', views.pair, name='pair'),
#    url(r'^h(?P<tmhelix_id>[0-9]+)/$', views.helix, name='helix'),
#    url(r'^upload/', include('fileupload.urls')),
#    url(r'^d(?P<database_id>[0-9]+)/$', views.database, name='database'),

    url(r'^list/Update/$', view='Update', name='Update')
)
