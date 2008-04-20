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
from djangoOp.widgets.autocomplete import AutoCompleteField
import add_module, play_module

# Index, PlayGame, AddQuestion, TheProject, TheCode, Login/Logout

def index(request):
    return render_to_response('index.html', {},context_instance=RequestContext(request))


def intro(request):
   return render_to_response('intro.html', {},context_instance=RequestContext(request))
 

def code(request):
   return render_to_response('code.html', {},context_instance=RequestContext(request))
 


def project(request):
   return render_to_response('project.html', {},context_instance=RequestContext(request))


@login_required 
def addquestion(request):
	return add_module.addnewquestion(request)

def play(request):
	return play_module.playOnline(request)

from widgets.autocomplete import autocomplete_response
def autocomplete(request):
    lastTag = request.POST['text']
    if lastTag.find(',') >= 0:
    	lastTag = lastTag.rpartition(',')[2]
    return autocomplete_response(lastTag, Tags , ('tag') )
