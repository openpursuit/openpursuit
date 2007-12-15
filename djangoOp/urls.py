from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^djangoOp/', include('djangoOp.foo.urls')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),

     (r'^base/$', 'djangoOp.OpenPursuit_Base.views.index')
)
