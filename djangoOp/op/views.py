# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import newforms as forms
from djangoOp.op.models import *
from djangoOp.settings import MEDIA_ROOT  
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
import datetime
from  django.utils import simplejson
from django.template.defaultfilters import escape

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.db.models import Q
import amf, amf.django


import add_module, play_module, genpdf_module

# Index, PlayGame, AddQuestion, TheProject, TheCode, Login/Logout

def index(request):
    return render_to_response('index.html', {},context_instance=RequestContext(request))

def code(request):
   return render_to_response('code.html', {},context_instance=RequestContext(request))
 
def project(request):
   return render_to_response('project.html', {},context_instance=RequestContext(request))

@login_required 
def addquiz(request):
	return add_module.addnewquiz(request)

def playonline(request):
	return play_module.playOnline(request)

def play(request):
	return render_to_response('play.html', {},context_instance=RequestContext(request))

def generatepdf(request):
	return genpdf_module.genpdf(request)

    
class JsonResponse(HttpResponse):
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = simplejson.dumps(object)
        super(JsonResponse, self).__init__(content, mimetype='application/json')    
    
@login_required
#@cache_control(no_cache=True)
def tags_ac(request):
    limit = 10
    query = request.GET.get('query', None)
    sep = ' ' # separator
    if query.find(sep) != -1:
        query = query.rsplit(sep, 1)[1]
    qargs = []   
    if query:
        qargs = [Q(tag__contains=query) ]
    tags = Tags.objects.filter(*qargs).order_by('tag')[:limit]
    results = []
    for tag in tags:
        results.append({'id':tag.id,
                        'tag':escape(tag.tag),
                        'occurrencies':escape(tag.quiz_set.all().count())
                        })
    ret_dict = {'resultset':{'totalResultsReturned':len(results),
                             'results':results}}
    return JsonResponse(ret_dict)

def getFlashQuestion(request):
	return Quiz.objects.all()
	
def calculate(request, arg1, arg2): #1
    return arg1 + arg2

