from django.shortcuts import render
from xml_parser.models import *
from django.shortcuts import render_to_response, get_object_or_404, render#, RequestContext

# Create your views here.

# Print detail of each movie.
#for movie in movies:
#   print "*****Movie*****"
#   if movie.hasAttribute("title"):
#      print "Title: %s" % movie.getAttribute("title")

#   type = movie.getElementsByTagName('type')[0]
#   print "Type: %s" % type.childNodes[0].data
#   format = movie.getElementsByTagName('format')[0]
#   print "Format: %s" % format.childNodes[0].data
#   rating = movie.getElementsByTagName('rating')[0]
#   print "Rating: %s" % rating.childNodes[0].data
#   description = movie.getElementsByTagName('description')[0]
#   print "Description: %s" % description.childNodes[0].data



def database(request):
# prawdopodobnie powinienem to jakos rozbic na kilka viewsow
    # Handle file upload
    print 'database'
    if request.method == 'POST':
        print 'POST'
        print request.POST.get('ExtractHelixTriplets')

        if request.POST.get('Update'):
            DatabaseModel.objects.Update()
        if request.POST.get('Clear'):
            DatabaseModel.objects.all().delete()
            protein.objects.all().delete()
            
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
           print 'ExtractHelixTriplets'
           TMProtein.objects.filter(structure__in=database_model_i.structure_set.all()).ExtractConsecutiveHelixTriplets ()
           print TMProtein.objects.filter(structure__in=database_model_i.structure_set.all())

#           database_model_i. TMProtein.objects

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
#               print Residue.objects.all()
               
               print Residue.objects.filter(AAThreeLetter=AAThreeLetterI)
               print Residue.objects.filter(AAThreeLetter=AAThreeLetterI).values_list('Z')
     #          quit()
               HistogramPlot(Residue.objects.filter(AAThreeLetter=AAThreeLetterI).values_list('Z'),'AminoAcidZPreference_'+AAThreeLetterI+'.png')
           # to teraz jak to ugryzc

        elif request.POST.get('Download'):
            structure.objects.Download()
            
        elif request.POST.get('Process'):
            database_model_i.Process() # to musi byc ten model, albo z argumentem

        form = TMProteinFileForm(request.POST, request.FILES)            

#            protein.objects.all().delete()
# musze przemyslec to przed zserializowaniem
# cos na kartce napisac itd
# moze sie znowu leb zagotuje
# musze to przekombinowac
    tmproteins = protein.objects.all()   
    return render(request,
        'database.html',
        {'tmproteins': tmproteins}

#,
#        context_instance=RequestContext(request)
    )

def Update (request):

#    TMProtein.objects.all().delete()

    return render_to_response(
        'database.html',
        context_instance=RequestContext(request)
    )

def Clear (request):

    protein.objects.all().delete()

    return render_to_response(
        'database.html',
        context_instance=RequestContext(request)
    )

def Download (request):

    structure.objects.all().download()

    return render_to_response(
        'database.html',
        context_instance=RequestContext(request)
    )


