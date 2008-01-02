from django.template import Library, Node
from djangoOp.op.models import Tags
import random

     
register = Library()

maxsize =220 # maximum size of the most popular tag
minsize = 55 # minimum size of the least popular tag



     
class LatestTagsNode(Node):
	def gen_clouds(self):
		p=Tags.objects.all()
		
		max1=max([int(myitem.question_set.count()) for myitem in p])
		
		for i in range(p.count()):
			size =int(round(int(p[i].question_set.count())*maxsize/max1))
			if size<minsize:
				size=minsize
			cloudsize =str(size) +"%"
			p[i].cloudsize=cloudsize
		return p

	def render(self, context):
		self.__init__()
		context['content_tagclouds'] = self.gen_clouds()
		return ''
    
def get_latest_cloudtag(parser, token):
    	
	return LatestTagsNode()
get_latest_cloudtag= register.tag(get_latest_cloudtag)
