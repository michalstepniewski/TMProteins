# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('myproject.myapp.views',
    url(r'^list/$', 'list', name='list'),
    url(r'^viewer/$', 'viewer', name='viewer'),
    url(r'^embedding/$', 'embedding', name='embedding'),
    url(r'^(?P<tmhelix_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^list/Clear/$', view='Clear', name='Clear')
)
