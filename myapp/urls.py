# -*- coding: utf-8 -*-
from django.conf.urls import  url, include#, patterns
from . import views
from django.contrib.auth import views as auth_views
from myapp.views import *

urlpatterns = [#patterns('myapp.views',
    url(r'^accounts/login/$', auth_views.login),
    url(r'^list/$', list, name='list'),
    url(r'^mail/$', mail, name='mail'),
    url(r'^viewer/$', viewer, name='viewer'),
    url(r'^aboutme/$', aboutme, name='aboutme'),
    url(r'^aboutapp/$', aboutapp, name='aboutapp'),
    url(r'^userguide/$', userguide, name='userguide'),
    url(r'^contact/$', contact, name='contact'),    
    url(r'^single_helix_stats/$', single_helix_stats, name='single_helix_stats'),
    url(r'^helix_pair_stats/$', helix_pair_stats, name='helix_pair_stats'),
    url(r'^helix_triplet_stats/$', helix_triplet_stats, name='helix_triplet_stats'),
    url(r'^embedding/$', embedding, name='embedding'),
    url(r'^t(?P<tmhelixtriplet_id>[0-9]+)/$', views.triplet, name='triplet'),
    url(r'^p(?P<tmhelixpair_id>[0-9]+)/$', views.pair, name='pair'),
    url(r'^h(?P<tmhelix_id>[0-9]+)/$', views.helix, name='helix'),
    url(r'^pr(?P<tmprotein_id>[0-9]+)/$', views.tmprotein, name='tmprotein'),
    url(r'^d(?P<database_id>[0-9]+)/$', views.database, name='database'),
    url(r'^clustering(?P<clustering_id>[0-9]+)/$', views.clustering, name='clustering'),
    url(r'^cluster(?P<cluster_id>[0-9]+)/$', views.cluster, name='cluster'),
    
    url(r'^delete-database/(?P<id>\d+)/$', views.delete_database, name='delete_database'),
    url(r'^clone-database/(?P<id>\d+)/$', views.clone_database, name='clone_database'),
    url(r'^rename-database/(?P<id>\d+)/$', views.rename_database, name='rename_database'),

    url(r'^multiple_upload', multiple_upload, name = 'multiple_upload'), # include('django-jquery-file-upload.urls')), 
#    url(r'^$', lambda x: HttpResponseRedirect('/upload/new/')),
    url(r'^upload/', include('fileupload.urls')),


    url(r'^list/Clear/$', Clear, name='Clear')
]#)
