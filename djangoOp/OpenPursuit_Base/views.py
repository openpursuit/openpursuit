# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import newforms as forms
from djangoOp.OpenPursuit_Base.models import Tags
from djangoOp.OpenPursuit_Base.models import Question 
from djangoOp.OpenPursuit_Base.models import Answers
from django.core.exceptions import ObjectDoesNotExist
import datetime

def index(request):

	class QuestionForm(forms.Form):
		question = forms.CharField(max_length=2000)
		rightAnswer = forms.CharField(max_length=2000)
		wrongAnswer1 = forms.CharField(max_length=2000)
		wrongAnswer2 = forms.CharField(max_length=2000)
		wrongAnswer3 = forms.CharField(max_length=2000)
		difficulty = forms.IntegerField()
		tags = forms.CharField(max_length=2000)


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

			
			q = Question(question = request.POST['question'], difficulty = request.POST['difficulty'], date = datetime.datetime.now(), score = 0);
			
			q.save() #this is need to create the primary key for the question
			q.tag.add(t)
			q.save()
			
			p = Answers(question = q, right1=request.POST['rightAnswer'] , wrong1=request.POST['wrongAnswer1'], wrong2=request.POST['wrongAnswer2'], wrong3=request.POST['wrongAnswer3'])
			p.save()

			#return HttpResponseRedirect('/url/on_success/')
			return HttpResponse("OK QUESTION ADDED")
	else:
		#template = loader.get_template('form.html')
		form = QuestionForm()
		return render_to_response('form.html', {'form': form})





