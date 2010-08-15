import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle
from django.db.models import Q
from djangoOp.op.models import Quiz, Tags
from sets import Set

class LangHandler(BaseHandler):
    allowed_methods = ('GET')
    fields = ('lang')
    model = Quiz

    @classmethod
    def content_size(self, blogpost):
        return len(blogpost.content)

    def read(self, request):
        post = Quiz.objects.all()
        return post 


class TagHandler(BaseHandler):
    #allowed_methods = ('GET', 'PUT', 'DELETE')
    allowed_methods = ('GET')
    #fields = ('question','right', 'wrong1','wrong2','wrong3')
        #('title', 'content', ('author', ('username', 'first_name')), 'content_size')
    #exclude = ('id', re.compile(r'^private_'))
    model = Tags

    @classmethod
    def content_size(self, blogpost):
        return len(blogpost.content)

    def read(self, request):
        post = Tags.objects.all()
        return post




class QuizHandler(BaseHandler):
    #allowed_methods = ('GET', 'PUT', 'DELETE')
    allowed_methods = ('GET')
    #fields = ('question','right', 'wrong1','wrong2','wrong3')
    #exclude = ('id', re.compile(r'^private_'))
    model = Quiz 

    @classmethod
    def content_size(self, blogpost):
        return len(blogpost.content)

    def read(self, request):
	#post = Quiz.objects.filter(tags__tag__startswith=tag)[:limit]
	tag = request.GET.get('tag', 'all')
	limit = request.GET.get('limit', 100)
	glang = request.GET.get('lang', 'it')
	post = Quiz.objects.filter(Q(tags__tag__startswith=tag) & Q(lang=glang)) [:limit]
        return post

    @throttle(5, 10*60) # allow 5 times in 10 minutes
    def update(self, request, post_slug):
        post = Blogpost.objects.get(slug=post_slug)

        post.title = request.PUT.get('title')
        post.save()

        return post

    def delete(self, request, post_slug):
        post = Blogpost.objects.get(slug=post_slug)

        if not request.user == post.author:
            return rc.FORBIDDEN # returns HTTP 401

        post.delete()

        return rc.DELETED # returns HTTP 204

#class ArbitraryDataHandler(BaseHandler):
#    methods_allowed = ('GET',)
#
#    def read(self, request, username, data):
#        user = User.objects.get(username=username)
#
#        return { 'user': user, 'data_length': len(data) }
