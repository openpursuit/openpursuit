from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import amf.django

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djangoOp/', include('djangoOp.foo.urls')),

     (r'^admin/(.*)', admin.site.root),
     #(r'^admin/', admin.site.root, ),
     (r'^$', 'djangoOp.op.views.index'),
#     (r'^intro$', 'djangoOp.op.views.intro'),
     (r'^static/(.*)$', 'django.views.static.serve',
{ 'document_root': settings.MEDIA_ROOT  }), 
     (r'^base/', include('djangoOp.op.urls')),
     (r'^accounts/', include('djangoOp.registration.urls')),
     (r'^gateway/getQuiz4Flash/(.*)', 'amf.django.views', {'views':'op.flashview'}), #1
)
