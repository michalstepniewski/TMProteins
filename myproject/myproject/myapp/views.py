# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document, TMHelix
from myproject.myapp.forms import DocumentForm
import os


def detail(request, tmhelix_id):
    tmhelix = get_object_or_404(TMHelix, pk=tmhelix_id)
    return render(request, 'detail.html', {'tmhelix': tmhelix})

def viewer(request):
#    tmhelix = get_object_or_404(TMHelix, pk=tmhelix_id)
    return render(request, 'viewer.html')

def embedding(request):
#    tmhelix = get_object_or_404(TMHelix, pk=tmhelix_id)
    return render(request, 'embedding.html')

def Clear (request,post_id):
    Document.objects.all().delete()

    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form, 'tmhelices': tmhelices },
        context_instance=RequestContext(request)
    )

def list(request):

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            
            os. system ('rm media/*')
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            os. system ('mv media/*.pdb media/TMProtein.pdb')
            TMHelix.objects.all().delete()
            TMHelix.objects.ReadPDB ('media/TMProtein.pdb', 'media/TMProtein.db')
            TMHelix.objects.read_helices_from_given_db ('media/TMProtein.db')

            b = Document.objects.order_by('id')[:Document.objects.count() -1 ]
            for d in b: d. delete () # deletes all but last objects of Document class

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:

        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all ()
    tmhelices = TMHelix.objects.all ()

    # Render list page with the documents and the form

    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form, 'tmhelices': tmhelices },
        context_instance=RequestContext(request)
    )
