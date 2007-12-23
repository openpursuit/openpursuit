# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import newforms as forms
from djangoOp.op.models import * 
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext 
import datetime


def index(request):
    all_questions = Question.objects.all()[:5]
    return render_to_response('index.html', {'all_questions': all_questions},context_instance=RequestContext(request))
	#return HttpResponse("ciao")
#	return render_to_response('index.html')

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
	class PlayForm(forms.Form):
		tags = forms.CharField(max_length=2000)
		
	if request.method == 'POST':
		form = PlayForm(request.POST)
		if form.is_valid():
			res = Question.objects.filter(tag__tag__startswith=request.POST['tags'])
			if res.count() > 0:
				res.order_by('?')
				print res
				quiz = res[0]
				print quiz.right1
				return render_to_response('play.html', {'quiz' : quiz},context_instance=RequestContext(request))
			else:
				return HttpResponse("No QUESTION FOUND FOR THIS TAG")
		else:
			print form.errors
			return HttpResponse("Form Not Valid")
	else:
		form = PlayForm()
		return render_to_response('play.html', {'form': form},context_instance=RequestContext(request))


