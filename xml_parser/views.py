from django.shortcuts import render
from xml_parser.models import *
from django.shortcuts import render_to_response, get_object_or_404, render, RequestContext

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
    if request.method == 'POST':

        if request.POST.get('Update'):
            DatabaseModel.objects.Update()
    tmproteins = protein.objects.all()   
    return render_to_response(
        'database.html',
        'tmproteins': tmproteins,
        context_instance=RequestContext(request)
    )

def Update (request):

#    TMProtein.objects.all().delete()

    return render_to_response(
        'database.html',
        context_instance=RequestContext(request)
    )

