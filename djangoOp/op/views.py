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

from widgets.autocomplete import autocomplete_response
def autocomplete(request):
    lastTag = request.POST['text']
    if lastTag.find(',') >= 0:
    	lastTag = lastTag.rpartition(',')[2]
    return autocomplete_response(lastTag, Tags , ('tag') )
