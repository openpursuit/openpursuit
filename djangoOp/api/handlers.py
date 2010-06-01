import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from djangoOp.op.models import Quiz

class QuizHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
    #fields = ('question','right', 'wrong1','wrong2','wrong3')
	#('title', 'content', ('author', ('username', 'first_name')), 'content_size')
    #exclude = ('id', re.compile(r'^private_'))
    model = Quiz 

    @classmethod
    def content_size(self, blogpost):
        return len(blogpost.content)

    def read(self, request, tag, limit):
	post = Quiz.objects.filter(tags__tag__startswith=tag)[:limit]
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
