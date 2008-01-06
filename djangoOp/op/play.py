from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import newforms as forms
from djangoOp.op.models import *
from djangoOp.settings import MEDIA_ROOT  
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
import random

def playOnline(request):
	
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
