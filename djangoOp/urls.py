from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import amf.django

admin.autodiscover()

urlpatterns = patterns('',
    # Example:

     (r'^admin/(.*)', admin.site.root),
     (r'^$', 'djangoOp.op.views.index'),
     (r'^static/(.*)$', 'django.views.static.serve',
{ 'document_root': settings.MEDIA_ROOT  }), 
     (r'^base/', include('djangoOp.op.urls')),
     (r'^accounts/', include('djangoOp.registration.urls')),
     (r'^gateway/getQuiz4Flash/(.*)', 'amf.django.views', {'views':'op.flashview'}), #1
     (r'^api/', include('api.urls')),
     (r'^fbook/', include('djangoOp.fbapp.urls')),
)

