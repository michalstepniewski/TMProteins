#python first
#django second
#your apps
#local app
import openpyxl
from django.contrib import messages
from django.conf import settings
#from django.core mail import send_mail

from django.core.mail import send_mail
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, render#, RequestContext
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myapp.models import TMProtein, TMHelixModel, TMHelixPair, TMHelixTriplet, \
Residue, TMProteinManager, XLSFile, Clustering, Cluster

from myapp.models1 import Parameters

from xml_parser.models import DatabaseModel

from myapp.forms import TMProteinFileForm
import os
from PlotToolsModule import HistogramPlot
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required
import matplotlib.pyplot as plt
from django.core.mail import send_mail

# Imaginary function to handle an uploaded file.
from somewhere import handle_uploaded_file

from .forms import NameForm

def get_name(request,id):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        print form.is_valid()
        if form.is_valid():
            print form.cleaned_data
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            db = DatabaseModel.objects.get(pk=id)
            db.name =  form.cleaned_data['your_name']
            db.save()
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})


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
    print tmhelixpair.TMHelix_IDs
    return render(request, 'pair.html', {'tmhelixpair': tmhelixpair})

def triplet(request, tmhelixtriplet_id):
    tmhelixtriplet = get_object_or_404(TMHelixTriplet, pk=tmhelixtriplet_id)
    return render(request, 'triplet.html', {'tmhelixtriplet': tmhelixtriplet})

def tmprotein(request, tmprotein_id):
    tmprotein = get_object_or_404(TMProtein, pk=tmprotein_id)
    return render(request, 'tmprotein.html', {'tmprotein': tmprotein})


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

def multiple_upload(request):
    return render(request, 'fileupload/picture_form.html')

def xml_parser(request):
    return render(request, 'database.html')

def delete_database(request, id):
    database = DatabaseModel.objects.get(pk=id).delete()    
    return HttpResponseRedirect(reverse('list'))

def rename_database(request, id):
#    database = DatabaseModel.objects.get(pk=id).delete()    
    return HttpResponseRedirect(reverse('list'))

def new_database(request):
#    database = DatabaseModel.objects.get(pk=id).delete()
    DatabaseModel.objects.create()    
    return HttpResponseRedirect(reverse('list'))


def clone_database(request, id):
    obj = DatabaseModel.objects.get(pk=id)
    old_obj = DatabaseModel.objects.create()

    for structure_I in obj.structure_set.all():
        old_obj.structure_set.add(structure_I)
    old_obj.save()
    
    return HttpResponseRedirect(reverse('list'))

def clustering(request, clustering_id):
    clustering = get_object_or_404(Clustering, pk=clustering_id)

    return render(request,
        'clustering.html',
        {'clustering':clustering, 'clusters': clustering.cluster_set.all(),\
        'no_triplets':TMHelixTriplet.objects.filter(Cluster__in=clustering.cluster_set.all()).count()},
)
#                  \
#        context_instance=RequestContext(request))

def cluster(request, cluster_id):
    cluster = get_object_or_404(Cluster, pk=cluster_id)

    return render(request,
        'cluster.html',
        {'cluster':cluster,'centroidpk':cluster.Centroidpk, 'tmhelixtriplets': cluster.tmhelixtriplet_set.all(),\
        },
)
#        context_instance=RequestContext(request))

def database(request, database_id):
    database = get_object_or_404(DatabaseModel, pk=database_id)
    
    if request.method == 'POST':

        if request.POST.get('Update'):
            DatabaseModel.objects.Update()

        if request.POST.get('Clear'):
            DatabaseModel.objects.all().delete()
            protein.objects.all().delete()

        if request.POST.get('Download'):
            structure.objects.Download()
            
        if request.POST.get('Process'):
            
            if '10MCcheckbox' in request.POST:
                
                database.Process()

            else:
            
                database.Process() 
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

        elif request.POST.get('ExtractInteractingHelixPairs'):
           # this happens if You push 'ExtractHelixPairs'
           TMProtein.objects.filter(structure__in=database.structure_set.all()).ExtractInteractingHelixPairs ()


        elif request.POST.get('ExtractHelixTriplets'):
           # this happens if You push 'ExtractHelixTriplets'
           TMProtein.objects.filter(structure__in=database.structure_set.all()).ExtractConsecutiveHelixTriplets ()


        elif request.POST.get('ExtractInteractingHelixTriplets'):
           TMProtein.objects.filter(structure__in=database.structure_set.all()).ExtractInteractingHelixTriplets ()

        elif request.POST.get('ClusterHelixTripletsByRMSD'):
                       
           TMHelixTriplet.objects.filter(TMProtein__structure__in=database.structure_set.all()).Cluster()

        elif request.POST.get('CARMSD'):
           TMHelixTriplet.objects.filter(TMProtein__structure__in=database.structure_set.all()).CACluster()

        elif request.POST.get('CalculateAminoAcidZPreferenceHistogram'):
           # this happens if You push 'ExtractHelixTriplets'

           AAThreeLetters = ['ARG','HIS','LYS','ASP','GLU','SER','THR','ASN',\
                             'GLN','CYS','GLY','PRO','ALA','VAL','ILE','LEU',\
                             'MET','PHE','TYR','TRP']
           for AAThreeLetterI in AAThreeLetters:
#               print Residue.objects.all()
               
               print Residue.objects.filter(AAThreeLetter=AAThreeLetterI)
               print Residue.objects.filter(AAThreeLetter=AAThreeLetterI).values_list('Z')
     #          quit()
               HistogramPlot(Residue.objects.filter(AAThreeLetter=AAThreeLetterI).values_list('Z'),'AminoAcidZPreference_'+AAThreeLetterI+'.png')
           # to teraz jak to ugryzc

        elif request.POST.get('Download'):
            structure.objects.Download()
            
        elif request.POST.get('Process'):
            database.Process() # to musi byc ten model, albo z argumentem


        form = TMProteinFileForm(request.POST, request.FILES)

        if form.is_valid():
            #this happens if you want to upload file
            
            Parameters.objects.all().delete()
            
            ParametersI = Parameters. objects. create ()
            ParametersI.DatabaseModel = database
            ParametersI. BordersOfThinSlices = form.cleaned_data['BordersOfThinSlices']
            ParametersI.save()
            print form.cleaned_data
#            print subject
            
            if 'UploadXLSFile' in request.POST:
                
                XLSFileI = XLSFile(xlsfile=request.FILES['tmproteinfile'])
                XLSFileI.save()
                XLSFileI.Read('media/'+request.FILES['tmproteinfile'].name.split('.')[0]+'/'+request.FILES['tmproteinfile'].name, database_id )
# trzeba bedzie zmienic funkcje Read zeby wczytywala do danego datasetu
#
#                TMProtein.objects.ReadXLS(XLSFile =  )

            elif 'UploadProteinFile' in request.POST:
            
                if 'checkbox' in request.POST:
                    print 'Checkbox Selected';
                    TMProteinI = TMProtein(tmproteinfile = request.FILES['tmproteinfile'],Set='Reference' )
                else:
                
                    TMProteinI = TMProtein(tmproteinfile = request.FILES['tmproteinfile'],Set='Test' )

#new instance of TMProtein is created from models I guess
                TMProteinI.save()

#            os. system ('mv media/*.pdb media/TMProtein.pdb') #no wlasnie tu trzeba zmienic i utworzyc
# katalog i tam przeniesc ale musze to prawilnie zrobic

                Path = TMProteinI.path
            #now we read helices from PDB file

                TMProteinI. ReadPDB ('media/'+request.FILES['tmproteinfile'].name.split('.')[0]+'/'+request.FILES['tmproteinfile'].name),# 'media/TMProtein.db')
# reads PDB to extract TM Helices
            # Redirect to the document list after POST
                return HttpResponseRedirect(reverse('myapp.views.list'))
    else:

        form = TMProteinFileForm() # A empty, unbound form
    
    
#    return render(request, 'dataset.html', {'structures': database.structure_set.all(),\
#                                            'database_model_i':database})

    Noclusters = Clustering.objects.values_list('no_cluster')
    RMSDs = Clustering.objects.values_list('RMSD')    
    plt.clf()
    
    plt.scatter (Noclusters , RMSDs)    
    plt.savefig ('NoClustersRMSDs.png' ,dpi=320)
    plt.clf()


    return render(request,
        'dataset.html',
        {'structures': database.structure_set.all(),\
         'clusterings':Clustering.objects.all(),\
          'form': form, \
         'database_model_i':database },)
#        context_instance=RequestContext(request))

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

    TMProtein.objects.all().delete()

    return render_to_response(
        'list.html',
        {'tmproteins': tmproteins, 'form': form },
        context_instance=RequestContext(request)
    )
    
#@login_required (redirect_field_name='my_redirect_field',login_url='/accounts/login/')
def list(request):
    print request
    
# prawdopodobnie powinienem to jakos rozbic na kilka viewsow
    # Handle file upload
    if request.method == 'POST':

        if request.POST.get('Clear'):
            #this happens if You push 'Clear' button
           TMProtein.objects.all().delete()
           TMHelixModel.objects.all().delete() # set relation one to many (Document -> TMHelix)

           os. system('rm -r myapp/static/myapp/static/media/*') # clear static files in media
           os. system('rm -r myapp/static/myapp/static/Stats/*') # clear static files in Stats
           #leaves only js files in media
           os. system('rm -r media/*;') #clears previously extracted Transmembrane Segments stored in PDB files
           

#     if request.POST.get("Upload"): #why am I not using this?

        elif request.POST.get('CalculateSingleHelixStats'):
            # this happens if You push 'CalculateSingleHelixStats' button

           TMHelixModel.objects.single_helix_stats ()

        elif request.POST.get('NewDataset'):
            # zrobic to przez linki np, niech formy beda rozbite na podstrony
            
            DatabaseModel.objects.create()
            # this happens if You push 'CalculateSingleHelixStats' button


        elif request.POST.get('CalculateHelixPairStats'):
            # this happens if You push 'CalculateHelixPairStats' button

           TMHelixPair.objects.helix_pair_stats ()

        elif request.POST.get('CalculateHelixTripletStats'):
            # this happens if You push 'CalculateHelixTripletStats button

           TMHelixTriplet.objects.helix_triplet_stats ()

        elif request.POST.get('ExtractHelixPairs'):
           # this happens if You push 'ExtractHelixPairs'

           TMProtein.objects.ExtractConsecutiveHelixPairs ()

        elif request.POST.get('ExtractInteractingHelixPairs'):
           # this happens if You push 'ExtractHelixPairs'

           TMProtein.objects.ExtractInteractingHelixPairs ()


        elif request.POST.get('ExtractHelixTriplets'):
           # this happens if You push 'ExtractHelixTriplets'

           TMProtein.objects.ExtractConsecutiveHelixTriplets ()

        elif request.POST.get('ExtractInteractingHelixTriplets'):
           # this happens if You push 'ExtractHelixTriplets'

           TMProtein.objects.ExtractInteractingHelixTriplets ()

        elif request.POST.get('ClusterHelixTripletsByRMSD'):
           
           TMHelixTriplet.objects.all().Cluster()
           



        elif request.POST.get('CalculateAminoAcidZPreferenceHistogram'):
           # this happens if You push 'ExtractHelixTriplets'

           AAThreeLetters = ['ARG','HIS','LYS','ASP','GLU','SER','THR','ASN',\
                             'GLN','CYS','GLY','PRO','ALA','VAL','ILE','LEU',\
                             'MET','PHE','TYR','TRP']
           for AAThreeLetterI in AAThreeLetters:
               print Residue.objects.all()
               
               print Residue.objects.filter(AAThreeLetter=AAThreeLetterI)
               print Residue.objects.filter(AAThreeLetter=AAThreeLetterI).values_list('Z')
     #          quit()
               HistogramPlot(Residue.objects.filter(AAThreeLetter=AAThreeLetterI).values_list('Z'),'AminoAcidZPreference_'+AAThreeLetterI+'.png')
           # to teraz jak to ugryzc

        form = TMProteinFileForm(request.POST, request.FILES)
        print form
        print request.POST
        print request.FILES
        print form.is_valid()
        

        if form.is_valid():
            #this happens if you want to upload file
            print request.POST.get('UploadXLSFile')
            if   request.POST.get('UploadXLSFile'):
                print 'Uploading XLS File'
                
                XLSFileI = XLSFile(xlsfile=request.FILES['tmproteinfile'])
                XLSFileI.save()
                xlspath = 'media/'+request.FILES['tmproteinfile'].name.split('.')[0]+'/'+request.FILES['tmproteinfile'].name
                print xlspath
                XLSFileI.Read(xlspath,database_id=1)

#                TMProtein.objects.ReadXLS(XLSFile =  )

            elif 'UploadProteinFile' in request.POST:
            
                if 'checkbox' in request.POST:
                    print 'Checkbox Selected';
                    TMProteinI = TMProtein(tmproteinfile = request.FILES['tmproteinfile'],Set='Reference' )
                else:
                
                    TMProteinI = TMProtein(tmproteinfile = request.FILES['tmproteinfile'],Set='Test' )

#new instance of TMProtein is created from models I guess
                TMProteinI.save()

#            os. system ('mv media/*.pdb media/TMProtein.pdb') #no wlasnie tu trzeba zmienic i utworzyc
# katalog i tam przeniesc ale musze to prawilnie zrobic

                Path = TMProteinI.path
            #now we read helices from PDB file

                TMProteinI. ReadPDB ('media/'+request.FILES['tmproteinfile'].name.split('.')[0]+'/'+request.FILES['tmproteinfile'].name),# 'media/TMProtein.db')
# reads PDB to extract TM Helices
            # Redirect to the document list after POST
                return HttpResponseRedirect(reverse('myapp.views.list'))
    else:

        form = TMProteinFileForm() # A empty, unbound form

    # Load documents for the list page
    tmproteins = TMProtein.objects.all ()
    databases = DatabaseModel.objects.all ()

    # Render list page with the documents and the form

    return render(request,
        'list.html',
        {'tmproteins': tmproteins, 'form': form, 'databases': databases },
#        context_instance=RequestContext(request)
    )

from django.contrib.auth import authenticate, login

'''

def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            ...
    else:
        # Return an 'invalid login' error message.
        ...
'''
        
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    
from django.conf import settings
from django.shortcuts import redirect

def my_view(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
