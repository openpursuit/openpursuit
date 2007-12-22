from django.conf.urls.defaults import *
from djangoOp.OpenPursuit_Base.models import Question 

info_dict = {
    'queryset': Question.objects.all(),
}



urlpatterns = patterns('',
    # Example:
    # (r'^djangoOp/', include('djangoOp.foo.urls')),

    # Uncomment this for admin:
     (r'add', 'djangoOp.OpenPursuit_Base.views.addquestion'),
     (r'prova', 'django.views.generic.list_detail.object_list', info_dict)
)
