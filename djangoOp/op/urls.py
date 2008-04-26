from django.conf.urls.defaults import *
from djangoOp.op.models import Quiz 
from djangoOp.op.models import Tags

info_dict = {
    'queryset': Quiz.objects.all(),
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
     (r'autocomplete', 'djangoOp.op.views.autocomplete'),
)
