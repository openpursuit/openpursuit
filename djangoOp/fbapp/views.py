from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
#uncomment the following two lines and the one below
#if you dont want to use a decorator instead of the middleware
#from django.utils.decorators import decorator_from_middleware
#from facebook.djangofb import FacebookMiddleware
import urllib
from django.core.files import File
from djangoOp.op.models import *
import os
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import math
# Import the Django helpers
# import facebook.djangofb as facebook
import datetime 
# The User model defined in models.py
#from models import User
from forms import FBQuizForm
from django.db.models import Avg, Min, Max, Count

# We'll require login for our canvas page. This
# isn't necessarily a good idea, as we might want
# to let users see the page without granting our app
# access to their info. See the wiki for details on how
# to do this.



def main(request):
    fbuser = None
    if request.method == 'GET':
        uid = request.GET.get('uid', None)
        bestof = 0
        if uid and uid != '0':
              try:
                fbuser = FBProfile.objects.get(uid=uid)
              except:
                  fbuser = None
                  return direct_to_template(request, 'fbapp/main.html', extra_context={'fbuser': fbuser})
              best_tags = []
              for t in Tags.objects.all():
                  for ts in TagsScore.objects.filter(tag=t).order_by('-score')[:1]:
                         if ts.user == fbuser:
                             best_tags.append(t.tag)
                             bestof = bestof +1
              #try:
              score = 0
              tss = TagsScore.objects.filter(user=fbuser)
              for i in tss:
                  score = score + i.score
              #aggr = TagsScore.objects.filter(user=fbuser).annotate(average=Avg('score'), max=Max('score'), min=Min('score'), count=Count('score'))
              #score = aggr[count] 
              #raise score
              #except:
              fbuser.score = score
              fbuser.bestof = bestof
              if  bestof >  3:
                  fbuser.best_tags = best_tags[:3] + [ " e altri" ]
              else:
                  fbuser.best_tags = best_tags 
    return direct_to_template(request, 'fbapp/main.html', extra_context={'fbuser': fbuser})

def save_score(request):
    if request.method == 'POST':
        uid = request.POST.get('uid', None)
        scores = request.POST.getlist('scores[]')
        fbuser = FBProfile.objects.get(uid=uid)
        for e in scores:
            t = Tags.objects.get(tag=e.split(':')[0])
            try:
               x = TagsScore.objects.get(user=fbuser, tag=t)
               if x.score < e.split(':')[1] :
                 x.score = e.split(':')[1]
                 x.save()
            except:
               t = TagsScore(user=fbuser, tag=t, score=e.split(':')[1])
               t.save()
        score = 0
        tags = TagsScore.objects.filter(user=fbuser)
        for t in tags: 
            score = score + t.score
        score = int(float(score) * math.log(tags.count() ) / float(tags.count()))
        fbuser.score = score
        fbuser.save()
    return HttpResponse("Ok")

def play(request):
    return direct_to_template(request, 'fbapp/play.html', extra_context={})



def play2(request):
    return direct_to_template(request, 'fbapp/play2.html', extra_context={})

def play3(request):
    general_chart = [] 
    friend_chart = []
    tag_friend_chart = []
    tag_general_chart = { } 
    tags = request.GET.getlist('tag')
    if request.method == 'GET':
        uid = request.GET.get('uid', None)
        if uid and uid != '0':
            general_chart = FBProfile.objects.order_by( '-score')[:6]

            tag_chart = []  
            for t in tags:
                qs = TagsScore.objects.filter(tag__tag=t).order_by( '-score')[:6]
                for q in qs:
                    el = { }
                    el = {'uid': q.user.uid, 'tag' : q.tag, 'score' : q.score, 'first_name': q.user.first_name }
                    tag_chart.append(el)
                tag_general_chart[t] = tag_chart
                tag_chart = [ ]
    return direct_to_template(request, 'fbapp/play3.html', extra_context={'general_chart' : general_chart,'tag_general_chart': tag_general_chart })


def addquiz(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = FBQuizForm(post_data)    
        uid = int(form.data['uid'])
        if uid != 0: 
            fbuser = FBProfile.objects.get(uid=uid) 
            relatedtags = []
            relatedtagsid = []
            for t in form.data['tags'].replace(",", " ").split(' '):
                t = t.strip().lower()
                if len(t)>0:
                    try:
                        if (relatedtags.count(t) > 0):
                            return HttpResponse("ERROR: USE A TAG FOR AT MOST ONE TIME")
                        relatedtags.append(t)
                        tx = Tags.objects.get(tag=t)
                        relatedtagsid.append(tx)
                    except ObjectDoesNotExist:
                        tw = Tags.objects.create(tag=t)
                        tw.save()
                        relatedtagsid.append(tw)
            q = Quiz(question=form.data['question'], right1=form.data['right1'], wrong1=form.data['wrong1'], wrong2=form.data['wrong2'], wrong3=form.data['wrong3'], lang='it', views=0, difficulty=form.data['difficulty'], date=datetime.datetime.now() , author=fbuser.user ,mediatype=1)
            q.save()
            q.tags = relatedtagsid
            return HttpResponse('Quiz aggiunto!')
        else:
            return HttpResponse('Errore uid nullo ')
    else:
        form = FBQuizForm()
    return direct_to_template(request, 'fbapp/addquiz.html', extra_context={'form':form})

def challenge(request):
    return direct_to_template(request, 'fbapp/challenge.html', extra_context={})

def fb_login(request):
    if request.method == 'POST':
        uid = request.POST.get('uid', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        pic_url = request.POST.get('pic_url', None)
        email = request.POST.get('email', None)
        content = urllib.urlretrieve(pic_url)
        fbuser = FBProfile()
        fbuser.uid=uid
        fbuser.first_name=first_name
        fbuser.last_name=last_name
        fbuser.pic_url=pic_url
        fbuser.email=email
        fbuser.score = 0
        fbuser.pic=File(name=uid+ "." +pic_url[-3:], file=open(content[0]))
        user = User(username='FB'+uid, first_name=first_name, last_name=last_name,email=email, password="0", is_staff=False, is_active=True, is_superuser=False)
        try:
            u = FBProfile.objects.get(uid=uid)
            w = User.objects.get(username='FB'+uid)
        #    if os.path.exists(settings.MEDIA_ROOT + 'fbpics/' +uid+ "." +pic_url[-3:]):
        #        u.pic.delete()
        except:
            user.save()
            fbuser.user=user
            fbuser.save()
        #fbuser.pic.save(uid+ "." +pic_url[-3:], File(open(content[0])) , save=True)
        return HttpResponse("Ok")
    else:
        return HttpResponse("Non Ok")


#@decorator_from_middleware(FacebookMiddleware)
#@facebook.require_login()
def canvas(request):
    # Get the User object for the currently logged in user
    #user = None
    #user = User.objects.get_current()
    
    # Check if we were POSTed the user's new language of choice
    #if 'language' in request.POST:
    #    user.language = request.POST['language'][:64]
    #    user.save()

    # User is guaranteed to be logged in, so pass canvas.fbml
    # an extra 'fbuser' parameter that is the User object for
    # the currently logged in user.
    return direct_to_template(request, 'fbapp/canvas.fbml')#  extra_context={'fbuser': user})

#@facebook.require_login()
def ajax(request):
    return HttpResponse('hello world')
