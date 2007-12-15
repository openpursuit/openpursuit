# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import newforms as forms
from djangoOp.OpenPursuit_Base.models import Tags
from djangoOp.OpenPursuit_Base.models import Question 
from djangoOp.OpenPursuit_Base.models import Answers

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
			#FIXME
			# Do form processing here...	                
			
			#WARNING --- FIX THIS --- THIS LOGIC DOES NOT WORK
			
			#Se il tag non esiste lo aggiungo
			
			#FIXME: "musica" va cambiato con il TAG passato via POST
			t = Tags.objects.create(tag="musica")
			t.save()
			
			q = Question(question = 'x', difficulty = ' ', score = ' ', date = ' ');
			q.tag.add(t)
			q.save()
			
			p = Answers(question = q, right1='sdfds' , wrong1='sdfsdf', wrong2='cdsfs', wrong3='xx')
			p.save()

			return HttpResponseRedirect('/url/on_success/')
	else:
		#template = loader.get_template('form.html')
		form = QuestionForm()
		return render_to_response('form.html', {'form': form})





