from django.conf.urls.defaults import *
from djangoOp.op.models import Quiz 
from djangoOp.op.models import Tags

info_dict = {
    'queryset': Quiz.objects.all(),
}

tag_lookup = {
	'queryset': Tags.objects.all(),
	'field': 'tag', # this is the field which is searched
	'limit': 10, # default is to limit query to 10 results. Increase this if you like.
	#'login_required': False, # default is to allow anonymous queries. Set to True if you want authenticated access.
}

urlpatterns = patterns('',
    # Example:

    # Uncomment this for admin:
     (r'add', 'djangoOp.op.views.addquiz'),
     (r'play', 'djangoOp.op.views.play'),
     (r'onlinegame1', 'djangoOp.op.views.playonline'),
     (r'generatepdf', 'djangoOp.op.views.generatepdf'),
     (r'code', 'djangoOp.op.views.code'),
     (r'project', 'djangoOp.op.views.project'),
     (r'^tag_lookup/$', 'djangoOp.op.views.tags_ac'),

)
