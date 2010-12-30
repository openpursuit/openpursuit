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


class FBQuizForm(forms.Form):
    question = forms.CharField(max_length=200)
    right1 = forms.CharField(max_length=75)
    wrong1 = forms.CharField(max_length=75)
    wrong2 = forms.CharField(max_length=75)
    wrong3 = forms.CharField(max_length=75)
    difficulty = forms.ChoiceField(choices=DIFFICULTY_LEVEL)
    tags = forms.CharField(max_length=100)
    uid = forms.IntegerField(widget=forms.HiddenInput() )
#	reference = forms.URLField(max_length=2000)
	
    def __init__(self,*args, **kwargs ):
        super(FBQuizForm, self).__init__(*args, **kwargs)
        n_lookup_url = reverse('djangoOp.op.views.tags_ac')  # url to your view
        n_schema = '["resultset.results", "tag", "occurrencies" ]'
        self.fields['tags'].widget = AutoCompleteWidget()
        self.fields['tags'].widget.lookup_url = n_lookup_url
        self.fields['tags'].widget.schema = n_schema
