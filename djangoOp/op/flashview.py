import amf, amf.django
from djangoOp.op.models import *
import random

def calculate(request, arg1, arg2): #1
    return arg1 + arg2

def calculate2(request, obj):       #2
    obj['sum'] = obj['arg1'] + obj['arg2']
    return obj
    
    
def getQuiz4Flash(request, topic):
	quiz = None
	q = Quiz.objects.filter(mediatype = 1, tags__tag__startswith=topic)
	if q.count() > 0:
		a = random.randint(0,q.count()-1)
		quiz = q[a]
	return quiz
