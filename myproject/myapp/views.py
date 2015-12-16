# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import TMProtein, TMHelixModel
from myproject.myapp.forms import TMProteinFileForm
import os

#####################################################################################################################################################
#####################################################################################################################################################
#####################################################################################################################################################

def detail(request, tmhelix_id):
    tmhelix = get_object_or_404(TMHelixModel, pk=tmhelix_id)
    return render(request, 'detail.html', {'tmhelix': tmhelix})

#####################################################################################################################################################

def viewer(request):
#    tmhelix = get_object_or_404(TMHelix, pk=tmhelix_id)
    return render(request, 'viewer.html')

#####################################################################################################################################################

def embedding(request):
#    tmhelix = get_object_or_404(TMHelix, pk=tmhelix_id)
    return render(request, 'embedding.html')

#####################################################################################################################################################

def Clear (request,post_id):
    TMProtein.objects.all().delete()

    return render_to_response(
        'list.html',
        {'tmproteins': tmproteins, 'form': form },
        context_instance=RequestContext(request)
    )

#####################################################################################################################################################

def list(request):

    # Handle file upload
    if request.method == 'POST':

        if request.POST.get('Clear'):
           TMProtein.objects.all().delete()
           TMHelixModel.objects.all().delete() # set relation one to many (Document -> TMHelix)

#     if request.POST.get("Upload"):

        form = TMProteinFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            os. system ('rm media/*')
            newtmproteinfile = TMProtein(tmproteinfile = request.FILES['tmproteinfile'])
            newtmproteinfile.save()

            os. system ('mv media/*.pdb media/TMProtein.pdb')
            newtmproteinfile.ReadPDB ('media/TMProtein.pdb', 'media/TMProtein.db')
#            TMHelix.objects.read_helices_from_given_db ('media/TMProtein.db') # this should be connected

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:

        form = TMProteinFileForm() # A empty, unbound form

    # Load documents for the list page
    tmproteins = TMProtein.objects.all ()
#    tmhelices  = TMHelixModel.objects.all ()

    # Render list page with the documents and the form

    return render_to_response(
        'list.html',
        {'tmproteins': tmproteins, 'form': form },
        context_instance=RequestContext(request)
    )

# musze to lepiej passowac
