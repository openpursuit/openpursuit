from django.conf.urls.defaults import *
from djangoOp.op.models import Question 

info_dict = {
    'queryset': Question.objects.all(),
}



urlpatterns = patterns('',
    # Example:
    # (r'^djangoOp/', include('djangoOp.foo.urls')),

    # Uncomment this for admin:
     (r'add', 'djangoOp.op.views.addquestion'),
     (r'prova', 'django.views.generic.list_detail.object_list', info_dict)
)
