from django.conf.urls import  include, url#,patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.views.static import serve

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^myapp/',include('myapp.urls')),
    url(r'^multiple_upload/', include('django-jquery-file-upload.urls')),
    url(r'^xml_parser/', include('xml_parser.urls')),
#    url(r'^$', lambda x: HttpResponseRedirect('/upload/new/')),
    url(r'^upload/', include('fileupload.urls')),

#    url(r'^myapp/',include('myproject.myapp.urls')),
    url(r'^$', RedirectView.as_view(url='/myapp/list/', permanent=True)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from os.path import join, abspath, dirname
urlpatterns += url  (r'^media/(.*)$', serve, {'document_root': join(abspath(dirname(__file__)), 'media')}),
#)
