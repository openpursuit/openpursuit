from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^djangoOp/', include('djangoOp.foo.urls')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^$', 'djangoOp.OpenPursuit_Base.views.index'),
     (r'^base/$', 'djangoOp.OpenPursuit_Base.views.addquestion')
)
