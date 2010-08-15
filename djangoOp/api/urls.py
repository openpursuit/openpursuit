from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from handlers import *

#auth = HttpBasicAuthentication(realm="My Realm")
#ad = { 'authentication': auth }

quiz_resource = Resource(handler=QuizHandler) #, **ad)
tag_resource = Resource(handler=TagHandler)
lang_resource = Resource(handler=LangHandler)
#arbitrary_resource = Resource(handler=ArbitraryDataHandler, **ad)

urlpatterns = patterns('',
#    url(r'^(?P<tag>\w+)/(?P<limit>\d+)/$', quiz_resource, { 'emitter_format': 'xml' } ),
     url(r'^getquiz$', quiz_resource, { 'emitter_format': 'xml' } ),
     url(r'^gettag$', tag_resource, { 'emitter_format': 'xml' } ),
     url(r'^getlang$', lang_resource, { 'emitter_format': 'xml' } ),
#    url(r'^other/(?P<username>[^/]+)/(?P<data>.+)/$', arbitrary_resource), 
)
