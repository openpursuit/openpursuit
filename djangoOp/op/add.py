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


def addnewquestion(request):
	class QuestionForm(forms.Form):
		question = forms.CharField(max_length=2000, label='Add the Question', widget=forms.TextInput(attrs={'onfocus':'javascript:writehelp("ciao");', 'onblur':'javascript:writehelp("");'}))
		rightAnswer = forms.CharField(max_length=2000, label='Write the right answer')
		wrongAnswer1 = forms.CharField(max_length=2000, label='Write a wrong answer')
		wrongAnswer2 = forms.CharField(max_length=2000, label='Write a wrong answer')
		wrongAnswer3 = forms.CharField(max_length=2000, label='Write a wrong answer')
		reference = forms.URLField(max_length=2000, label='Provide a valid url (e.g. Wikipedia) where is possible to check the correctness of the answer')
		difficulty = forms.ChoiceField(choices=DIFFICULTY_LEVEL, label='Choose an appropriate difficulty level for the question')
		tags = forms.CharField(required=False, widget=AutoCompleteField(url='/base/autocomplete/') , label='Insert one or more tags, separed by comma')
		language = forms.ChoiceField(choices=LANGUAGES, label='Select the language')
		media = forms.ChoiceField(widget=forms.Select(attrs={'onchange':'javascript:changeMedia();'}), choices=MEDIA_TYPE , label='Select the media type of the question')
		media_file = forms.Field(widget=forms.FileInput(attrs={'disabled':'true'}), required=False, label='If the question is not just textual, select the multimedia resourcess related to the question')        
	
	if request.method == 'POST':
		post_data = request.POST.copy()		post_data.update(request.FILES)
		form = QuestionForm(post_data)
		
		if form.is_valid():
			# Do form processing here...	                
			
			#WARNING --- FIX THIS --- THIS LOGIC DOES NOT WORK
			#split various tag
			relatedtags = []
			relatedtagsid = []
			for t in request.POST['tags'].split(','):
				t = t.strip()
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
					

			q = Question(question = request.POST['question'], right1=request.POST['rightAnswer'] , wrong1=request.POST['wrongAnswer1'], wrong2=request.POST['wrongAnswer2'], wrong3=request.POST['wrongAnswer3'], difficulty = request.POST['difficulty'], date = datetime.datetime.now(), views = 0,reference = request.POST['reference'], lang =request.POST['language'], spamfeedback = 0, quarantine = False, mediatype = request.POST['media'])
			
			isFileOk = False
			mfile = ''
			filename = ''
			extension = ''
			if 'media_file' in request.FILES:  				mfile = request.FILES['media_file']				# Other data on the request.FILES dictionary:  				#filesize = len(file['content'])<br />  				#filetype = file['content-type']   				filename = mfile['filename']
				extension = filename.rpartition('.')[2].lower()
				isFileOk = checkContentType(mfile['content-type'], request.POST['media'], extension)
				if not isFileOk:
					return HttpResponse("BAD FILE TYPE")
					
					
			q.save() #this is need to create the primary key for the question
			for tt in relatedtagsid:
				q.tag.add(tt)
			new_question = q.save()
			if isFileOk:
				fileencname = str(q.id) + '.'+ extension
				fd = open('%s/upload/%s' % (MEDIA_ROOT, fileencname ), 'wb')				fd.write(mfile['content'])				fd.close()
			#return HttpResponseRedirect('/url/on_success/')
			return HttpResponse("OK QUESTION ADDED")
		else: 
			return render_to_response('form.html', {'form': form},context_instance=RequestContext(request))
	else:
		form = QuestionForm()
		return render_to_response('form.html', {'form': form},context_instance=RequestContext(request))

def checkContentType(ctype, mtype, ext):
	""" Check if media type match content type and if the format is valid and if the extension of the file is among the supported extensions"""
	ext_video = ['mpg', 'mpeg', 'avi']
	ext_audio = ['mp3', 'ogg']
	ext_image = ['jpeg', 'jpg', 'gif', 'png']

	mediaName  = MEDIA_TYPE[int(mtype) -1][1]
	if ctype.partition('/')[0] != mediaName:
		return False
	if mediaName == 'audio' and not ext_audio.count(ext) :
		return False
	elif mediaName == 'video' and not ext_video.count(ext):
		return False
	elif mediaName == 'image' and not ext_image.count(ext):
		return False
	else:
		return True
		