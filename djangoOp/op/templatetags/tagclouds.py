from django.template import Library, Node
from djangoOp.op.models import Tags
from django.db.models import Count 
import random

     
register = Library()

maxsize =200 # maximum size of the most popular tag
minsize = 75 # minimum size of the least popular tag



     
class LatestTagsNode(Node):
    def gen_clouds(self):
        p=Tags.objects.annotate(num_quizes=Count('quiz')).order_by('-num_quizes')
        if p.count() == 0:
            return ''
        max1=max([int(myitem.quiz_set.count()) for myitem in p])

        for i in range(p.count()):
            size =int(round(int(p[i].quiz_set.count())*maxsize/max1))
            if size<minsize:
                size=minsize
            cloudsize =str(size) +"%"
            p[i].cloudsize=cloudsize
        return list(p) #.sort(key=cloudsize)  #.sort(key=cloudsize)

    def render(self, context):
        self.__init__()
        context['content_tagclouds'] = self.gen_clouds()
        return ''

    def get_latest_cloudtag(parser, token):
        return LatestTagsNode()

    get_latest_cloudtag = register.tag(get_latest_cloudtag)
