from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import HttpResponseRedirect
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^myapp/',include('myapp.urls')),
    url(r'^multiple_upload/', include('django-jquery-file-upload.urls')),
#    url(r'^$', lambda x: HttpResponseRedirect('/upload/new/')),
    url(r'^upload/', include('fileupload.urls')),

#    url(r'^myapp/',include('myproject.myapp.urls')),
    url(r'^$', RedirectView.as_view(url='/myapp/list/', permanent=True)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from os.path import join, abspath, dirname
urlpatterns += patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': join(abspath(dirname(__file__)), 'media')}),
)