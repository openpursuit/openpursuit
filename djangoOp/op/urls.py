from django.conf.urls.defaults import *
from djangoOp.op.models import Question 
from djangoOp.op.models import Tags

info_dict = {
    'queryset': Question.objects.all(),
}


urlpatterns = patterns('',
    # Example:
    # (r'^djangoOp/', include('djangoOp.foo.urls')),

    # Uncomment this for admin:
     (r'add', 'djangoOp.op.views.addquestion'),
     (r'play', 'djangoOp.op.views.play'),
     (r'instructions', 'djangoOp.op.views.instructions'),
     (r'community', 'djangoOp.op.views.community'),
     (r'tagcloud', 'djangoOp.op.views.tagcloud'),
     (r'autocomplete', 'djangoOp.op.views.autocomplete'),
)
