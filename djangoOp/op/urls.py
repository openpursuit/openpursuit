from django.conf.urls.defaults import *
from djangoOp.op.models import Question 
from djangoOp.op.models import Tags

info_dict = {
    'queryset': Question.objects.all(),
}

tags_lookup = {	'queryset': Tags.objects.all(),	'field': 'tag', # this is the field which is searched	#'limit': 10, # default is to limit query to 10 results. Increase this if you like.	#'login_required': False, # default is to allow anonymous queries. Set to True if you want authenticated access.}


urlpatterns = patterns('',
    # Example:
    # (r'^djangoOp/', include('djangoOp.foo.urls')),

    # Uncomment this for admin:
     (r'add', 'djangoOp.op.views.addquestion'),
     (r'play', 'djangoOp.op.views.play'),
     (r'instructions', 'djangoOp.op.views.instructions'),
     (r'community', 'djangoOp.op.views.community'),
     (r'tagcloud', 'djangoOp.op.views.tagcloud'),
     (r'^tags_lookup/$', 'djangoOp.op.views.json_lookup', tags_lookup),
)
