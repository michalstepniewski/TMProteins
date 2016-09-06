#python first
#django second
#your apps
#local app

from django.contrib import messages
from django.conf import settings
#from django.core mail import send_mail

from django.core.mail import send_mail
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render, RequestContext
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import TMProtein, TMHelixModel, TMHelixPair, TMHelixTriplet
from myproject.myapp.forms import TMProteinFileForm
import os

from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
from somewhere import handle_uploaded_file

def mail(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})

def helix(request, tmhelix_id):
    tmhelix = get_object_or_404(TMHelixModel, pk=tmhelix_id)
    
    return render(request, 'helix.html', {'tmhelix': tmhelix})


def pair(request, tmhelixpair_id):
    tmhelixpair = get_object_or_404(TMHelixPair, pk=tmhelixpair_id)
    return render(request, 'pair.html', {'tmhelixpair': tmhelixpair})

def triplet(request, tmhelixtriplet_id):
    tmhelixtriplet = get_object_or_404(TMHelixTriplet, pk=tmhelixtriplet_id)
    return render(request, 'triplet.html', {'tmhelixtriplet': tmhelixtriplet})

def single_helix_stats(request):
    return render(request, 'single_helix_stats.html')

def aboutapp(request):
    return render(request, 'aboutapp.html')

def aboutme(request):
    return render(request, 'aboutme.html')

def userguide(request):
    return render(request, 'userguide.html')

def contact(request):
    return render(request, 'contact.html')

def helix_pair_stats(request):
    return render(request, 'helix_pair_stats.html')

def helix_triplet_stats(request):
    return render(request, 'helix_triplet_stats.html')

def viewer(request):
    return render(request, 'viewer.html')

def embedding(request):
    return render(request, 'embedding.html')

def handle_uploaded_file(f):

    """saves file but we will need it to create folders as well if not present """
#    mkdir TMProtein.tmproteinfile.name if that works
 
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def Clear (request,post_id):

#    TMProtein.objects.all().delete()

    return render_to_response(
        'list.html',
        {'tmproteins': tmproteins, 'form': form },
        context_instance=RequestContext(request)
    )

def list(request):

    # Handle file upload
    if request.method == 'POST':

        if request.POST.get('Clear'):
            #this happens if You push 'Clear' button
           TMProtein.objects.all().delete()
           TMHelixModel.objects.all().delete() # set relation one to many (Document -> TMHelix)

           os. system('rm -r myproject/myapp/static/myapp/static/media/*') # clear static files in media
           os. system('rm -r myproject/myapp/static/myapp/static/Stats/*') # clear static files in Stats
           #leaves only js files in media
           os. system('rm -r media/*;') #clears previously extracted Transmembrane Segments stored in PDB files

        if request.POST.get('Delete'):
            pass           

#     if request.POST.get("Upload"): #why am I not using this?

        elif request.POST.get('CalculateSingleHelixStats'):
            # this happens if You push 'CalculateSingleHelixStats' button

           TMHelixModel.objects.single_helix_stats ()

        elif request.POST.get('CalculateHelixPairStats'):
            # this happens if You push 'CalculateHelixPairStats' button

           TMHelixPair.objects.helix_pair_stats ()

        elif request.POST.get('CalculateHelixTripletStats'):
            # this happens if You push 'CalculateHelixTripletStats button

           TMHelixTriplet.objects.helix_triplet_stats ()

        elif request.POST.get('ExtractHelixPairs'):
           # this happens if You push 'ExtractHelixPairs'

           TMProtein.objects.ExtractConsecutiveHelixPairs ()

        elif request.POST.get('ExtractHelixTriplets'):
           # this happens if You push 'ExtractHelixTriplets'

           TMProtein.objects.ExtractConsecutiveHelixTriplets ()

        form = TMProteinFileForm(request.POST, request.FILES)

        if form.is_valid():
            #this happens if you want to upload file
                        
            TMProteinI = TMProtein(tmproteinfile = request.FILES['tmproteinfile'] )

#new instance of TMProtein is created from models I guess
            TMProteinI.save()

#            os. system ('mv media/*.pdb media/TMProtein.pdb') #no wlasnie tu trzeba zmienic i utworzyc
# katalog i tam przeniesc ale musze to prawilnie zrobic

            Path = TMProteinI.path
            #now we read helices from PDB file

            TMProteinI. ReadPDB ('media/'+request.FILES['tmproteinfile'].name.split('.')[0]+'/'+request.FILES['tmproteinfile'].name, 'media/TMProtein.db')
# reads PDB to extract TM Helices
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:

        form = TMProteinFileForm() # A empty, unbound form

    # Load documents for the list page
    tmproteins = TMProtein.objects.all ()

    for tmprotein in tmproteins: print tmprotein.atoms

    # Render list page with the documents and the form

    return render_to_response(
        'list.html',
        {'tmproteins': tmproteins, 'form': form },
        context_instance=RequestContext(request)
    )
