# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('myproject.myapp.views',
    url(r'^list/$', 'list', name='list'),
    url(r'^mail/$', 'mail', name='mail'),
    url(r'^viewer/$', 'viewer', name='viewer'),
    url(r'^single_helix_stats/$', 'single_helix_stats', name='single_helix_stats'),
    url(r'^helix_pair_stats/$', 'helix_pair_stats', name='helix_pair_stats'),
    url(r'^helix_triplet_stats/$', 'helix_triplet_stats', name='helix_triplet_stats'),
    url(r'^embedding/$', 'embedding', name='embedding'),
    url(r'^t(?P<tmhelixtriplet_id>[0-9]+)/$', views.triplet, name='triplet'),
    url(r'^p(?P<tmhelixpair_id>[0-9]+)/$', views.pair, name='pair'),
    url(r'^h(?P<tmhelix_id>[0-9]+)/$', views.helix, name='helix'),


    url(r'^list/Clear/$', view='Clear', name='Clear')
)
