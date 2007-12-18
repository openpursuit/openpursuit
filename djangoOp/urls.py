from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    # Example:
    # (r'^djangoOp/', include('djangoOp.foo.urls')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^$', 'djangoOp.OpenPursuit_Base.views.index'),
     (r'^static/(.*)$', 'django.views.static.serve',
{ 'document_root': settings.MEDIA_ROOT  }), 
     (r'^base/', include('djangoOp.OpenPursuit_Base.urls'))
)
