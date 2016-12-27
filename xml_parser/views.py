from django.shortcuts import render
from xml_parser.models import *
from django.shortcuts import render_to_response, get_object_or_404, render#, RequestContext
from myapp.models1 import Parameters
from myapp.models import TMProtein


from celery import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
#from periodically.decorators import *
##@periodic_task(run_every=crontab())
#@every(minutes=1)
def do_every_midnight():
    id=8
    db = DatabaseModel.objects.get(pk=id)
    db.Update()


AAThreeLetters = ['ARG','HIS','LYS','ASP','GLU','SER','THR','ASN',\
                  'GLN','CYS','GLY','PRO','ALA','VAL','ILE','LEU',\
                  'MET','PHE','TYR','TRP']

from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_AT_TIMES = ['22:30']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'xml_parser.my_cron_job'    # a unique code

    def do(self):
        id=8
        f=open('/home/soutys/MyCronJobLog.txt','a')
        f.write('done')
        f.flush()
        f.close()

        db = DatabaseModel.objects.get(pk=id)
        db.Update()
        print 'done'    # do your thing here
        #sprawdzic czy sie na pewno updateuje

class MyCronJob2(CronJobBase):
    RUN_AT_TIMES = ['23:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'xml_parser.my_cron_job2'    # a unique code

    def do(self):
        id=8
        db = DatabaseModel.objects.get(pk=id)
        db.structure_set.Download()
        print 'done'    # do your thing here
        f=open('/home/soutys/MyCronJob2Log.txt','a')
        f.write('done')
        f.flush()
        f.close()
        print 'done'    # do your thing here

class MyCronJob3(CronJobBase):
    RUN_AT_TIMES = ['23:30']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'xml_parser.my_cron_job3'    # a unique code

    def do(self):
        id=8
        db = DatabaseModel.objects.get(pk=id)
        db.Process()
        print 'done'    # do your thing here
        f=open('/home/soutys/MyCronJob3Log.txt','a')
        f.write('done')
        f.flush()
        f.close()
        print 'done'    # do your thing here


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

def CalculateSingleHelixStats(request, ds_id):
    TMHelixModel.objects.single_helix_stats ()
    tmproteins = protein.objects.all()   
    return render(request,
        'database.html',
        {'tmproteins': tmproteins})

def CalculateHelixPairStats(request, ds_id):
    TMHelixPair.objects.helix_pair_stats ()
    tmproteins = protein.objects.all()   
    return render(request,
        'database.html',
        {'tmproteins': tmproteins})

def CalculateHelixTripletStats(request, ds_id):
    TMHelixTriplet.objects.helix_triplet_stats ()
    tmproteins = protein.objects.all()   
    return render(request,
        'database.html',
        {'tmproteins': tmproteins})

def ExtractHelixPairs(request, id):
    # zmienic na if not TMProtein.tmhelixpair.set
    database_model_i = DatabaseModel.objects.get(pk=id)
    TMProtein.objects.filter(structure__in=database_model_i.structure_set.all()).ExtractConsecutiveHelixPairs ()

    tmproteins = protein.objects.all()   
    return render(request,
        'database.html',
        {'tmproteins': tmproteins})

class MyCronJob3(CronJobBase):
    RUN_AT_TIMES = ['0:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)

    code = 'xml_parser.my_cron_job4'    # a unique code

    def do(self):
    # zmienic na if not TMProtein.tmhelixpair.set
        id=8
        database_model_i = DatabaseModel.objects.get(pk=id)
        TMProtein.objects.filter(structure__in=database_model_i.structure_set.all()).ExtractConsecutiveHelixPairs ()
        print 'done'    # do your thing here
        f=open('/home/soutys/MyCronJob4Log.txt','a')
        f.write('done')
        f.flush()
        f.close()
        print 'done'    # do your thing here


def ExtractInteractingHelixPairs(request, ds_id):
    TMProtein.objects.ExtractInteractingHelixPairs ()
    tmproteins = protein.objects.all()   
    return render(request,
        'database.html',
        {'tmproteins': tmproteins})

def ExtractHelixTriplets(request, id):
    database_model_i = DatabaseModel.objects.get(pk=id)
    TMProtein.objects.filter(structure__in=database_model_i.structure_set.all()).ExtractConsecutiveHelixTriplets ()
    print TMProtein.objects.filter(structure__in=database_model_i.structure_set.all())

def ExtractInteractingHelixTriplets(request, ds_id):
    TMProtein.objects.ExtractInteractingHelixTriplets ()


def ClusterHelixTripletsByRMSD(request, id):
    #jakis subset jest potrebny
    from myapp.models import TMHelixTriplet
#    structures=database_model_i.structure_set.all()    
    database_model_i = DatabaseModel.objects.get(pk=id)

    TMHelixTriplet.objects.filter(TMProtein__structure__in=database_model_i.structure_set.all()).Cluster()

def CalculateAminoAcidZPreferenceHistogram(request, ds_id):

    for AAThreeLetterI in AAThreeLetters:
        HistogramPlot(Residue.objects.filter(AAThreeLetter=AAThreeLetterI).values_list('Z'),'AminoAcidZPreference_'+AAThreeLetterI+'.png')

def Download(request, id):
    db = DatabaseModel.objects.get(pk=id)
    structure.objects.Download()

def DownloadResults(request, ds_id):
    return

def DownloadPDBs(request, id):
    db = DatabaseModel.objects.get(pk=id)
    db.structure_set.Download()
        
    return

def Clear(request, ds_id): 
    DatabaseModel.objects.all().delete()
    protein.objects.all().delete()
    TMProtein.objects.all().delete()
    TMHelixModel.objects.all().delete()
    os. system('rm -r myapp/static/myapp/static/media/*') # clear static files in media
    os. system('rm -r myapp/static/myapp/static/Stats/*') # clear static files in Stats
    os. system('rm -r media/*;') #clears previously extracted Transmembrane Segments stored in PDB files

def Update(request, id):
    db = DatabaseModel.objects.get(pk=id)
    db.Update()
    return render(request,
        'database.html')

def Process(request, id):
    database_model_i = DatabaseModel.objects.get(pk=id)
    database_model_i.Process() # to musi byc ten model, albo z argumentem

def AminoAcidPreferencesForPackings(request, ds_id):
    return

def SolventAccessibility(request, ds_id):
    return
    
def database(request):

    if request.method == 'POST':

        form = TMProteinFileForm(request.POST, request.FILES)            
        if form.is_valid():
            #this happens if you want to upload file
            
            Parameters.objects.all().delete()
            
            ParametersI = Parameters. objects. create ()
            ParametersI.DatabaseModel = database
            ParametersI. BordersOfThinSlices = form.cleaned_data['BordersOfThinSlices']
            ParametersI.save()
            print form.cleaned_data

    tmproteins = protein.objects.all()   
    return render(request,
        'database.html',
        {'tmproteins': tmproteins}
    )

#def Update (request):
#
#    TMProtein.objects.all().delete()
#
#    return render_to_response(
#        'database.html',
#        context_instance=RequestContext(request)
#    )

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


