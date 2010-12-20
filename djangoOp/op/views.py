# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django import forms
from djangoOp.op.models import *
from djangoOp.op.add_module import QuizForm
from djangoOp.settings import MEDIA_ROOT  
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
import datetime
from  django.utils import simplejson
from django.template.defaultfilters import escape
from django.http import HttpResponseRedirect
from django.core import serializers

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.db.models import Q
import amf, amf.django
from django.contrib.auth import REDIRECT_FIELD_NAME


import add_module, play_module, genpdf_module

# Index, PlayGame, AddQuestion, TheProject, TheCode, Login/Logout

def index(request):
    return render_to_response('index.html', {},context_instance=RequestContext(request))

def code(request):
   return render_to_response('code.html', {},context_instance=RequestContext(request))
 
def project(request):
   return render_to_response('project.html', {},context_instance=RequestContext(request))
   
def widgets(request):
   return render_to_response('widgets.html', {},context_instance=RequestContext(request))

def faq(request):
   return render_to_response('faq.html', {},context_instance=RequestContext(request))

@login_required 
def addquiz(request):
	return add_module.addnewquiz(request)

def playonline(request):
	return play_module.playOnline(request)

def play(request):
	return render_to_response('play.html', {},context_instance=RequestContext(request))

def jsplay(request):
	return render_to_response('jsgame.html', {},context_instance=RequestContext(request))

def jsplay2(request):
	return render_to_response('jsgame2.html', {},context_instance=RequestContext(request))

def getquizapi(request):
	import random
	query_tags = request.GET.get('tags', None)
	query_limit = request.GET.get('limit', 0 )
	query_limit = int(query_limit)
	query_lang = request.GET.get('lang', None)
	if (query_tags == None) :
		return HttpResponseBadRequest("No tags specified")
	tags = query_tags.split(',')
	qs = []
	for t in tags:
		#qs +=  Quiz.objects.filter(tags__tag__contains = t)[:int(query_limit/len(tags))] if qs == None else qs | Quiz.objects.filter(tags__tag__contains = t)[:int(query_limit/len(tags))]
		qs += list(Quiz.objects.filter(tags__tag__contains = t, lang=query_lang).order_by('?')[:int(query_limit/len(tags))])
		
	data = serializers.serialize('json', qs, fields=('question','right1','wrong1','wrong2','wrong3' ))
	return HttpResponse(data, mimetype="text/json")

def jsplay_fb(request):
	form = QuizForm()
	user = ''
	if request.user.is_authenticated():
		user = request.user.facebook_profile 
	return render_to_response('jsgame.html', {
	'USER_LOGGED_IN': request.user.is_authenticated(),
	'user': user,
	REDIRECT_FIELD_NAME:'/base/jsgame/',
	'form': form
	},
	context_instance=RequestContext(request))

def flash1(request):
	return render_to_response('flash1.html', {},context_instance=RequestContext(request))

def calendar(request):
	return render_to_response('calendar/sample.html', {},context_instance=RequestContext(request))

def generatepdf(request):
	return genpdf_module.genpdf(request)

    
class JsonResponse(HttpResponse):
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = simplejson.dumps(object)
        super(JsonResponse, self).__init__(content, mimetype='application/json')    
    
#@login_required
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



def profile(request):
    page = 'profile'
    user = ''

    if request.user.is_authenticated():
        user = request.user.facebook_profile
        friendList = request.user.facebook_profile.get_friends_profiles()
    else:
        redirect_url = '/facebook/login'
        return HttpResponseRedirect(redirect_url)

    return render_to_response(
        "profile.html",
        {
            'page': page,
            'USER_LOGGED_IN': request.user.is_authenticated(),
            'user': user,
            'friendList': friendList,
        },
        context_instance=RequestContext(request)
    )

