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

def index(request):
    return render_to_response('index.html', {},context_instance=RequestContext(request))
	#return HttpResponse("ciao")
#	return render_to_response('index.html')

def intro(request):
   return render_to_response('intro.html', {},context_instance=RequestContext(request))
 

def instructions(request):
   return render_to_response('instructions.html', {},context_instance=RequestContext(request))
 
def tagcloud(request):
   return render_to_response('tagcloud.html', {},context_instance=RequestContext(request)) 

def community(request):
   return render_to_response('community.html', {},context_instance=RequestContext(request))


@login_required 
def addquestion(request):

	class QuestionForm(forms.Form):
		question = forms.CharField(max_length=2000, widget=forms.TextInput(attrs={'onfocus':'javascript:writehelp("ciao");', 'onblur':'javascript:writehelp("");'}))
		rightAnswer = forms.CharField(max_length=2000)
		wrongAnswer1 = forms.CharField(max_length=2000)
		wrongAnswer2 = forms.CharField(max_length=2000)
		wrongAnswer3 = forms.CharField(max_length=2000)
		reference = forms.URLField(max_length=2000)
		#difficulty = forms.IntegerField()
		difficulty = forms.ChoiceField(choices=DIFFICULTY_LEVEL)
		#tags = forms.CharField(max_length=2000)
		tags = forms.ChoiceField()
		#lang = forms.CharField(max_length=5)
		language = forms.ChoiceField(choices=LANGUAGES)
		media = forms.ChoiceField(widget=forms.Select(attrs={'onchange':'javascript:changeMedia();'}), choices=MEDIA_TYPE )
		media_file = forms.Field(widget=forms.FileInput(attrs={'disabled':'true'}), required=False)        
	if request.method == 'POST':
		post_data = request.POST.copy()		post_data.update(request.FILES)
		form = QuestionForm(post_data)
		print request.FILES['media_file']
		if form.is_valid():
			# Do form processing here...	                
			
			#WARNING --- FIX THIS --- THIS LOGIC DOES NOT WORK
			
			#Se il tag non esiste lo aggiungo
			try:
				t = Tags.objects.get(tag=request.POST['tags'])

			except ObjectDoesNotExist:
				
				t = Tags.objects.create(tag=request.POST['tags'])
				t.save()

			q = Question(question = request.POST['question'], right1=request.POST['rightAnswer'] , wrong1=request.POST['wrongAnswer1'], wrong2=request.POST['wrongAnswer2'], wrong3=request.POST['wrongAnswer3'], difficulty = request.POST['difficulty'], date = datetime.datetime.now(), views = 0,reference = request.POST['reference'], lang =request.POST['language'], spamfeedback = 0, quarantine = False, mediatype = 'text')
			
			# VERY INSECURE!!!! Parse the file type
			print 'prima if'
			if 'media_file' in request.FILES:  				mfile = request.FILES['media_file']				# Other data on the request.FILES dictionary:  				#filesize = len(file['content'])<br />  				#filetype = file['content-type']   				filename = mfile['filename']
				if mfile['content-type'] != 'audio/mpeg' and mfile['content-type'] !='image/jpeg':
					return HttpResponse("BAD FILE TYPE")				fd = open('%s/%s' % (MEDIA_ROOT, filename), 'wb')				fd.write(mfile['content'])				fd.close()
		
			
			
			
			q.save() #this is need to create the primary key for the question
			q.tag.add(t)
			#q.language.add(lang)
			q.save()

			#return HttpResponseRedirect('/url/on_success/')
			return HttpResponse("OK QUESTION ADDED")
		else: 
			#print form.errors
			#response = HttpResponse()
			#response.write("<p>The form contains some errors:</p>")
			#response.write(form.errors)
			#return response
			form = QuestionForm()
			return render_to_response('form.html', {'form': form},context_instance=RequestContext(request))
	else:
		#template = loader.get_template('form.html')
		form = QuestionForm()
		return render_to_response('form.html', {'form': form},context_instance=RequestContext(request))





def play(request):
	import random
	class PlayForm(forms.Form):
		tags = forms.CharField(max_length=2000)
		
	if request.method == 'POST':
		if request.POST.has_key('action'):
			# the result of the game
			quest = Question.objects.filter(id=request.POST['question_id'])
			if quest.count() > 0:
				if quest[0].right1 == request.POST['answer']:
					return HttpResponse("Hai vinto")
				else:
					return HttpResponse("Hai perso")	
			else:
				return HttpResponse("BAD!")
		else:
			# Show the form with answers and question
			form = PlayForm(request.POST)
			if form.is_valid():
				res = Question.objects.filter(tag__tag__startswith=request.POST['tags'])
				if res.count() > 0:
					res.order_by('?')
					quiz = res[0]
					ansarray = [quiz.right1, quiz.wrong1, quiz.wrong2 ,  quiz.wrong3]
					random.shuffle( ansarray )
					return render_to_response('play.html', {'ansarray' : ansarray, 'quiz' : quiz},context_instance=RequestContext(request))
				else:
					return HttpResponse("No QUESTION FOUND FOR THIS TAG")
			else:
				print form.errors
				# TODO: report form errors in html
				return HttpResponse("Form Not Valid")
	else:
		# Show the form for search for tag
		form = PlayForm()
		return render_to_response('play.html', {'form': form},context_instance=RequestContext(request))

#AJAX


class JsonResponse(HttpResponse):
    def __init__(self, obj):
        self.original_obj = obj
        HttpResponse.__init__(self, self.serialize())
        self["Content-Type"] = "text/javascript"

    def serialize(self):
        return(simplejson.dumps(self.original_obj))

def json_lookup(request, queryset, field, limit=10, login_required=False):
    """
    Method to lookup a model field and return a array. Intended for use 
    in AJAX widgets.
    """
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)
    obj_list = []
    lookup = {
        '%s__istartswith' % field: request.GET['q'],
    }
    for obj in queryset.filter(**lookup)[:limit]:
        obj_list.append([getattr(obj, field), obj.id])
    return JsonResponse(obj_list)
