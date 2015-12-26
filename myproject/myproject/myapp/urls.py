# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('myproject.myapp.views',
    url(r'^list/$', 'list', name='list'),
    url(r'^viewer/$', 'viewer', name='viewer'),
    url(r'^single_helix_stats/$', 'single_helix_stats', name='single_helix_stats'),
    url(r'^embedding/$', 'embedding', name='embedding'),
    url(r'^p(?P<tmhelixpair_id>[0-9]+)/$', views.pair, name='pair'),
    url(r'^(?P<tmhelix_id>[0-9]+)/$', views.detail, name='detail'),


    url(r'^list/Clear/$', view='Clear', name='Clear')
)
