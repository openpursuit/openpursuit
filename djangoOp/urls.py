from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^djangoOp/', include('djangoOp.foo.urls')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^$', 'djangoOp.op.views.index'),
     (r'^intro$', 'djangoOp.op.views.intro'),
     (r'^static/(.*)$', 'django.views.static.serve',
{ 'document_root': settings.MEDIA_ROOT  }), 
     (r'^base/', include('djangoOp.op.urls')),
     (r'^accounts/', include('registration.urls')),
)
