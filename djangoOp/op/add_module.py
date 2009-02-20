from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms
from djangoOp.op.models import *
from djangoOp.settings import MEDIA_ROOT  
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
import datetime
from  django.utils import simplejson
from djangoOp.widgets.autocomplete import AutoCompleteWidget
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse


def addnewquiz(request):
	class QuizForm(forms.Form):
		question = forms.CharField(max_length=2000, label='Inserisci una domanda', widget=forms.TextInput(attrs={'onfocus':'javascript:writehelp("Inserisci una domanda abbastanza corta che abbia una sola risposta giusta");', 'onblur':'javascript:writehelp("");'}))
		rightAnswer = forms.CharField(max_length=2000, label='Inserisci la risposta giusta',widget=forms.TextInput(attrs={'onfocus':'javascript:writehelp("Inserisci la risposta esatta");', 'onblur':'javascript:writehelp("");'}))	
		wrongAnswer1 = forms.CharField(max_length=2000, label='Inserisci una risposta sbagliata',widget=forms.TextInput(attrs={'onfocus':'javascript:writehelp("Inserisci una risposta sbagliata ma verosimile!");', 'onblur':'javascript:writehelp("");'}))	
		wrongAnswer2 = forms.CharField(max_length=2000, label='Inserisci una risposta sbagliata',widget=forms.TextInput(attrs={'onfocus':'javascript:writehelp("Inserisci una risposta sbagliata ma verosimile!");', 'onblur':'javascript:writehelp("");'}))
		wrongAnswer3 = forms.CharField(max_length=2000, label='Inserisci una risposta sbagliata',widget=forms.TextInput(attrs={'onfocus':'javascript:writehelp("Inserisci una risposta sbagliata ma verosimile!");', 'onblur':'javascript:writehelp("");'}))
		difficulty = forms.ChoiceField(choices=DIFFICULTY_LEVEL, label='Scegli il livello di difficolta\' della domanda')
		tags = forms.CharField(required=False, label='Inserisci uno o piu\' tag serparati da uno spazio',widget=forms.TextInput(attrs={'onfocus':'javascript:writehelp("Inserisci una risposta sbagliata ma verosimile!");', 'onblur':'javascript:writehelp("");'}))
		language = forms.ChoiceField(choices=LANGUAGES, label='Scegli la lingua')
		media = forms.ChoiceField(widget=forms.Select(attrs={'onchange':'javascript:changeMedia();'}), choices=MEDIA_TYPE , label='Seleziona il tipo di domanda')
		media_file = forms.Field(widget=forms.FileInput(attrs={'disabled':'true'}), required=False, label='Seleziona il file da allegare alla domanda (solo se la domanda non e\' testuale)')
		reference = forms.URLField(max_length=2000, label='Inserisci un sito web di riferimento',widget=forms.TextInput(attrs={'onfocus':'javascript:writehelp("Inserisci un indirizzo web (ad esempio Wikipedia) dove poter ottenere maggiori informazioni sulla domanda ");', 'onblur':'javascript:writehelp("");'}))       

		def __init__(self,*args, **kwargs ):
			super(QuizForm, self).__init__(*args, **kwargs)
			n_lookup_url = reverse('djangoOp.op.views.tags_ac')  # url to your view
			#n_lookup_url = "http://www.openpursuit.org/base/tag_lookup/"
			# see YUI docs to see what shema is. In general it 
			#describes data returned from your view
			n_schema = '["resultset.results", "tag", "occurrencies" ]' 
			self.fields['tags'].widget = AutoCompleteWidget()
			self.fields['tags'].widget.lookup_url = n_lookup_url
			self.fields['tags'].widget.schema = n_schema

		
	if request.method == 'POST':
		post_data = request.POST.copy()	
		post_data.update(request.FILES)
		form = QuizForm(post_data)
		
		if form.is_valid():
			# Do form processing here...	                
			
			#WARNING --- FIX THIS --- THIS LOGIC DOES NOT WORK
			#split various tag
			relatedtags = []
			relatedtagsid = []
			for t in request.POST['tags'].split(' '):
				t = t.strip()
				t = t.lower()
				if t == '':
					continue
				#Se il tag non esiste lo aggiungo
				try:
					if (relatedtags.count(t) > 0):
						return HttpResponse("ERROR: USE A TAG FOR AT MOST ONE TIME")
					else:
						relatedtags.append(t)
					tx = Tags.objects.get(tag=t)
					relatedtagsid.append(tx)
				except ObjectDoesNotExist:
					tw = Tags.objects.create(tag=t)
					tw.save()
					relatedtagsid.append(tw)
					

			q = Quiz(question = request.POST['question'], right1=request.POST['rightAnswer'] , wrong1=request.POST['wrongAnswer1'], wrong2=request.POST['wrongAnswer2'], wrong3=request.POST['wrongAnswer3'], difficulty = request.POST['difficulty'], date = datetime.datetime.now(), views = 0,reference = request.POST['reference'], lang =request.POST['language'],author=request.user ,quarantine = False, mediatype = request.POST['media'])
			
			isFileOk = False
			mfile = ''
			filename = ''
			extension = ''
			if 'media_file' in request.FILES: 
				mfile = request.FILES['media_file']
				# Other data on the request.FILES dictionary:
				#filesize = len(file['content'])<br /> 
				#filetype = file['content-type']
				filename = mfile['filename']

				extension = filename.rsplit('.',1)[1].lower()
				#extension = filename.rpartition('.')[2].lower()
				isFileOk = checkContentType(mfile['content-type'], request.POST['media'], extension)
				if not isFileOk:
					return HttpResponse("BAD FILE TYPE")
					
					
			q.save() #this is need to create the primary key for thequiz 
			for tt in relatedtagsid:
				q.tags.add(tt)
			new_quiz = q.save()
			if isFileOk:
				fileencname = str(q.id) + '.'+ extension
				fd = open('%s/upload/%s' % (MEDIA_ROOT, fileencname ), 'wb')
				fd.write(mfile['content'])
				fd.close()
			#return HttpResponseRedirect('/url/on_success/')
			#	return HttpResponse("OK QUESTION ADDED")
			return render_to_response('quizadded.html', {'added': 'ok' },context_instance=RequestContext(request))
		else: 
			return render_to_response('addquiz.html', {'form': form},context_instance=RequestContext(request))
	else:
		form = QuizForm()
		return render_to_response('addquiz.html', {'form': form},context_instance=RequestContext(request))

def checkContentType(ctype, mtype, ext):
	""" Check if media type match content type and if the format is valid and if the extension of the file is among the supported extensions"""
	ext_video = ['mpg', 'mpeg', 'avi']
	ext_audio = ['mp3', 'ogg']
	ext_image = ['jpeg', 'jpg', 'gif', 'png']

	mediaName  = MEDIA_TYPE[int(mtype) -1][1]
	#if ctype.partition('/')[0] != mediaName:
	if ctype.split('/')[0] != mediaName:
		return False
	if mediaName == 'audio' and not ext_audio.count(ext) :
		return False
	elif mediaName == 'video' and not ext_video.count(ext):
		return False
	elif mediaName == 'image' and not ext_image.count(ext):
		return False
	else:
		return True
		
