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

from reportlab.pdfgen import canvas

import add_module, play_module

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

def play(request):
	return play_module.playOnline(request)

def gencardspdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=somefilename.pdf'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response

from widgets.autocomplete import autocomplete_response
def autocomplete(request):
    lastTag = request.POST['text']
    if lastTag.find(',') >= 0:
    	lastTag = lastTag.rpartition(',')[2]
    return autocomplete_response(lastTag, Tags , ('tag') )
