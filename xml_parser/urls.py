# -*- coding: utf-8 -*-
from django.conf.urls import  url, include#, patterns
from . import views
from xml_parser.views import *
from xml_parser import views

urlpatterns = [#patterns('xml_parser.views',
    url(r'^database/$', database, name='database'),
        url(r'^myapp/',include('myapp.urls')),

#    url(r'^t(?P<tmhelixtriplet_id>[0-9]+)/$', views.triplet, name='triplet'),
#    url(r'^p(?P<tmhelixpair_id>[0-9]+)/$', views.pair, name='pair'),
#    url(r'^h(?P<tmhelix_id>[0-9]+)/$', views.helix, name='helix'),
#    url(r'^upload/', include('fileupload.urls')),
#    url(r'^d(?P<database_id>[0-9]+)/$', views.database, name='database'),

    url(r'^calculate-single-helix-stats/(?P<id>\d+)/$', views.CalculateSingleHelixStats, name='calculatesinglehelixstats'),
    url(r'^calculate-helix-pair-stats/(?P<id>\d+)/$', views.CalculateHelixPairStats, name='CalculateHelixPairStats'),
    url(r'^calculate-helix-triplet-stats/(?P<id>\d+)/$', views.CalculateHelixTripletStats, name='CalculateHelixTripletStats'),
    url(r'^extract-helix-pairs/(?P<id>\d+)/$', views.ExtractHelixPairs, name='ExtractHelixPairs'),
    url(r'^extract-interacting-helix-pairs/(?P<id>\d+)/$', views.ExtractInteractingHelixPairs, name='ExtractInteractingHelixPairs'),
    url(r'^extract-helix-triplets/(?P<id>\d+)/$', views.ExtractHelixTriplets, name='ExtractHelixTriplets'),
    url(r'^extract-interacting-helix-triplets/(?P<id>\d+)/$', views.ExtractInteractingHelixTriplets, name='ExtractInteractingHelixTriplets'),
    url(r'^calculate-amino-acid-z-preference-histogram/(?P<id>\d+)/$', views.CalculateAminoAcidZPreferenceHistogram, name='CalculateAminoAcidZPreferenceHistogram'),
    url(r'^cluster-helix-triplets-by-rmsd/(?P<id>\d+)/$', views.ClusterHelixTripletsByRMSD, name='ClusterHelixTripletsByRMSD'),
    url(r'^amino-acid-preferences-for-packings/(?P<id>\d+)/$', views.AminoAcidPreferencesForPackings, name = 'AminoAcidPreferencesForPackings'),
    url(r'^solvent-accessibility/(?P<id>\d+)/$', views.SolventAccessibility, name = 'SolventAccessibility'),
    url(r'^download-results/(?P<id>\d+)/$', views.DownloadResults, name = 'DownloadResults'),
    url(r'^update/(?P<id>\d+)/$', views.Update, name='Update'),
    url(r'^download-pdbs/(?P<id>\d+)/$', views.DownloadPDBs, name ='Download PDBs'),
    url(r'^clear/(?P<id>\d+)/$', views.Clear, name = 'Clear'),
    url(r'^process/(?P<id>\d+)/$', views.Process, name = 'Process'),

#    url(r'^calculatesinglehelixstats/$', CalculateSingleHelixStats, name='calculatesinglehelixstats')

    
]#)
