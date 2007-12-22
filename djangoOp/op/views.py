# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import newforms as forms
from djangoOp.OpenPursuit_Base.models import Tags
from djangoOp.OpenPursuit_Base.models import Question 
from djangoOp.OpenPursuit_Base.models import Languages
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
		language = forms.CharField(max_length=200)

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

			#Se non esiste la lingua la aggiungo
			try:
				lang = Languages.objects.get(language=request.POST['language'])

			except ObjectDoesNotExist:
				
				lang = Languages.objects.create(language=request.POST['language'])
				lang.save()
			
			q = Question(question = request.POST['question'], right1=request.POST['rightAnswer'] , wrong1=request.POST['wrongAnswer1'], wrong2=request.POST['wrongAnswer2'], wrong3=request.POST['wrongAnswer3'], difficulty = request.POST['difficulty'], date = datetime.datetime.now(), score = 0,reference = request.POST['reference']);
			
			q.save() #this is need to create the primary key for the question
			q.tag.add(t)
			q.language.add(lang)
			q.save()

			#return HttpResponseRedirect('/url/on_success/')
			return HttpResponse("OK QUESTION ADDED")
		else: return HttpResponse("FORM WAS NOT VALID")
	else:
		#template = loader.get_template('form.html')
		form = QuestionForm()
		return render_to_response('form.html', {'form': form},context_instance=RequestContext(request))





