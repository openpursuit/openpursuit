from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import newforms as forms
from djangoOp.op.models import *
from djangoOp.settings import MEDIA_ROOT  
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from datetime import datetime
import random

def playOnline(request):
	
	class PlayForm(forms.Form):
		tags = forms.CharField(max_length=2000)
		
	if request.method == 'POST':
		if request.POST.has_key('score'):
			q = Quiz.objects.filter(id=request.POST['quiz_id'])
			risp = request.POST['score']
			if risp == "positive" or risp == "negative":
				risp_value = 0
				if risp == 'positive':
					risp_value = 1
				s = Score(value = risp_value, voter=request.user, quiz = q[0], date = datetime.now() )
				s.save()
				return HttpResponse("Done")
			elif risp == "noscore":
				return HttpResponse("no score")
			else:
				return HttpResponse("Invalid score")
				
				
		if request.POST.has_key('action'):
			# the result of the game
			if not request.POST.has_key('answer') :
				return render_to_response('playonline.html', {'noresp': 1}, context_instance=RequestContext(request))
			qid = request.POST['quiz_id']
			quest = Quiz.objects.filter(id=qid)
			if quest.count() > 0:
				if quest[0].right1 == request.POST['answer']:
					return render_to_response('playonline.html', {'youwin': 1, 'quiz_id': qid }, context_instance=RequestContext(request)) 
				else:
					return render_to_response('playonline.html', {'youloose': 1, 'quiz_id': qid }, context_instance=RequestContext(request)) 
			else:
				return HttpResponse("BAD!")
		else:
			# Show the form with answers and question
			form = PlayForm(request.POST)
			if form.is_valid():
				res = Quiz.objects.filter(tags__tag__startswith=request.POST['tags'])
				if res.count() > 0:
					#res.order_by('?')
					a = random.randint(0,res.count()-1)
					quiz = res[a]
					question = quiz.question	
					ansarray = [quiz.right1, quiz.wrong1, quiz.wrong2 ,  quiz.wrong3]
					random.shuffle( ansarray )
					return render_to_response('playonline.html', {'ansarray' : ansarray, 'question' : question, 'quiz' : quiz},context_instance=RequestContext(request))
				else:
					#return HttpResponse("No QUESTION FOUND FOR THIS TAG")
					return render_to_response('playonline.html', {'noquizfound': 1}, context_instance=RequestContext(request)) 
			else:
				print form.errors
				# TODO: report form errors in html
				return HttpResponse("Form Not Valid")
	else:
		# Show the form for search for tag
		form = PlayForm()
		return render_to_response('playonline.html', {'form': form},context_instance=RequestContext(request))
