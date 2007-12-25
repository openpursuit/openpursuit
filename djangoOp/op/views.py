# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import newforms as forms
from djangoOp.op.models import * 
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext 
import datetime


def index(request):
    return render_to_response('index.html', {},context_instance=RequestContext(request))
	#return HttpResponse("ciao")
#	return render_to_response('index.html')

def instructions(request):
   return render_to_response('instructions.html', {},context_instance=RequestContext(request))
 
def community(request):
   return render_to_response('community.html', {},context_instance=RequestContext(request))


def addquestion(request):

	class QuestionForm(forms.Form):
		question = forms.CharField(max_length=2000)
		rightAnswer = forms.CharField(max_length=2000)
		wrongAnswer1 = forms.CharField(max_length=2000)
		wrongAnswer2 = forms.CharField(max_length=2000)
		wrongAnswer3 = forms.CharField(max_length=2000)
		reference = forms.URLField(max_length=2000)
		difficulty = forms.IntegerField()
		tags = forms.CharField(max_length=2000)
		lang = forms.CharField(max_length=5)

	if request.method == 'POST':
        
		form = QuestionForm(request.POST)
	        if form.is_valid():
			# Do form processing here...	                
			
			#WARNING --- FIX THIS --- THIS LOGIC DOES NOT WORK
			
			#Se il tag non esiste lo aggiungo
			try:
				t = Tags.objects.get(tag=request.POST['tags'])

			except ObjectDoesNotExist:
				
				t = Tags.objects.create(tag=request.POST['tags'])
				t.save()

			q = Question(question = request.POST['question'], right1=request.POST['rightAnswer'] , wrong1=request.POST['wrongAnswer1'], wrong2=request.POST['wrongAnswer2'], wrong3=request.POST['wrongAnswer3'], difficulty = request.POST['difficulty'], date = datetime.datetime.now(), views = 0,reference = request.POST['reference'], lang =request.POST['lang'], spamfeedback = 0, quarantine = False, mediatype = 'text', attachment = '');
			
			q.save() #this is need to create the primary key for the question
			q.tag.add(t)
			#q.language.add(lang)
			q.save()

			#return HttpResponseRedirect('/url/on_success/')
			return HttpResponse("OK QUESTION ADDED")
		else: 
			print form.errors
			return HttpResponse("FORM WAS NOT VALIDz")
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


