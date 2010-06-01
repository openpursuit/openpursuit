from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

#from myapp.handlers import BlogPostHandler, ArbitraryDataHandler
from handlers import *

#auth = HttpBasicAuthentication(realm="My Realm")
#ad = { 'authentication': auth }

quiz_resource = Resource(handler=QuizHandler) #, **ad)
#arbitrary_resource = Resource(handler=ArbitraryDataHandler, **ad)

urlpatterns = patterns('',
    url(r'^(?P<tag>\w+)/(?P<limit>\d+)/$', quiz_resource, { 'emitter_format': 'xml' } ),
#    url(r'^other/(?P<username>[^/]+)/(?P<data>.+)/$', arbitrary_resource), 
)
