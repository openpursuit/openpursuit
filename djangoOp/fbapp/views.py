from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.template import RequestContext
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
from django.utils import simplejson

from sets import Set
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
        players_list = FBProfile.objects.order_by('?')[:5]
        opponents_list = [ {'uid': 37419699200 } ,  {'uid': 100000980465757 } ,  {'uid': 100001650755172 } , {'uid': 1403147446 }  ]
        top_contributors_list  = FBProfile.objects.annotate(quiz_n=Count('user__quiz')).order_by('-quiz_n')[:5]

        if uid and uid != '0':
              try:
                fbuser = FBProfile.objects.get(uid=uid)
              except:
                  fbuser = None
                  #return direct_to_template(request, 'fbapp/main.html', extra_context={'fbuser': fbuser})
                  return render_to_response('fbapp/main.html', {'fbuser': fbuser,  'players_list': players_list, 'opponents_list': opponents_list, 'top_contributors_list': top_contributors_list, 'quizcount': Quiz.objects.count() },context_instance=RequestContext(request))
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

    return render_to_response('fbapp/main.html', {'fbuser': fbuser, 'players_list': players_list, 'opponents_list': opponents_list, 'top_contributors_list': top_contributors_list, 'quizcount': Quiz.objects.count()},context_instance=RequestContext(request))
    #return direct_to_template(request, 'fbapp/main.html', extra_context={'fbuser': fbuser})

def save_score(request):
    if request.method == 'POST':
        uid = request.POST.get('uid', None)
        scores = request.POST.getlist('scores[]')
        fbuser = FBProfile.objects.get(uid=uid)
        for e in scores:
            score_new = int(e.split(':')[1])
            score_tag = e.split(':')[0]
            t = Tags.objects.get(tag = score_tag)
            try:
               x = TagsScore.objects.get(user=fbuser, tag=t)
               if x.score < score_new :
                 x.score = score_new 
                 x.save()
            except:
               t = TagsScore(user=fbuser, tag=t, score=score_new )
               t.save()
        score = 0
        tags = TagsScore.objects.filter(user=fbuser)
        for t in tags: 
            score = score + t.score
        # formula for calculating the general score for all the tags
        score = int(float(score) * math.log(tags.count() ) / float(tags.count()))
        fbuser.score = score
        fbuser.save()
    return HttpResponse("Ok")

def play(request):
    return direct_to_template(request, 'fbapp/play.html', extra_context={})



def play2(request):
    return direct_to_template(request, 'fbapp/play2.html', extra_context={})

def play3(request):
    '''
       Chart 
    '''
    general_chart = [] 
    friend_chart = []
    tag_friend_chart = []
    tag_general_chart = { } 
    tags = request.GET.getlist('tag')
    if request.method == 'GET':
        uid = request.GET.get('uid', None)
        if uid and uid != '0':
            general_chart = FBProfile.objects.order_by( '-score')[:50]
            tag_chart = []  
            for t in tags:
                qs = TagsScore.objects.filter(tag__tag=t).order_by( '-score')[:50]
                for q in qs:
                    el = { }
                    el = {'uid': q.user.uid, 'tag' : q.tag, 'score' : q.score, 'first_name': q.user.first_name }
                    tag_chart.append(el)
                tag_general_chart[t] = tag_chart
                tag_chart = [ ]
    if len(tags[0]) == 0:
        tag_general_chart = None
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

def challenge_info(request):
    challenge_id = request.GET.get('challenge_id', None)
    data = { 'winner_tagname': '', 'winner_score': -1000000, 'losers': {}  }
    c = FBChallenge.objects.get(request_id = challenge_id)
    data['quizes'] = c.quizes.tags
    cc = FBChallenge.objects.filter(quizes = c.quizes)
    for challenge in cc:
        if challenge.sender_score != -1000000 and challenge.receiver_score != -1000000:
            # for the sender 
            p = FBProfile.objects.get(pk = challenge.sender)
            tagname = '@[' + str(p.uid) + ':1:'+ p.first_name + ']'
            if challenge.sender_score > data['winner_score']:
                if data['winner_score'] != -1000000 and not data['losers'].has_key(data['winner_tagname']):
                    data['losers'][data['winner_tagname']] = data['winner_score']
                data['winner_score'] = challenge.sender_score
                data['winner_tagname'] = tagname 
            else:
                if not data[losers].has_key(tagname):
                    data['losers'][ tagname ] = challenge.sender_score 
            # for the receiver
            p = FBProfile.objects.get(pk = challenge.receiver)
            tagname = '@[' + str(p.uid) + ':1:'+ p.first_name + ']'
            if challenge.receiver_score > data['winner_score']:
                if data['winner_score'] != -1000000 and not data['losers'].has_key(data['winner_tagname']):
                    data['losers'][data['winner_tagname']] = data['winner_score']
                data['winner_score']= challenge.receiver_score
                data['winner_tagname'] = tagname 
            else:
                if not data['losers'].has_key(tagname):
                    data['losers'][ tagname ] = challenge.receiver_score 
        else:
            data = None
            break

    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def challenge_create(request):
    return direct_to_template(request, 'fbapp/challenge-create.html', extra_context={})

def challenge_menu(request):
    uid = request.GET.get('uid', None)
    pendingcount, historycount = 0,0
    if uid:
        pendingcount = FBChallenge.objects.filter(receiver = uid, receiver_score = -1000000 ).count()
        pendingcount += FBChallenge.objects.filter(sender = uid, sender_score = -1000000 ).count()
        historycount = FBChallenge.objects.filter(receiver = uid).exclude(receiver_score = -1000000).count()
    return direct_to_template(request, 'fbapp/challenge-menu.html', extra_context={'pendingcount': pendingcount, 'historycount': historycount})

def challenge_pending(request):
    uid = request.GET.get('uid', None)
    if uid:
        pending = []
        challengepending = FBChallenge.objects.filter(receiver = uid, receiver_score = -1000000 ) | FBChallenge.objects.filter(sender = uid, sender_score = -1000000 ) 
        for challenge in challengepending:
            request_id = challenge.request_id
            tags = challenge.quizes.tags
            userids = Set([]) 
            other_receivers = FBChallenge.objects.filter(quizes = challenge.quizes)
            for o in other_receivers:
                userids.add(o.receiver)
                userids.add(o.sender)
            pending.append({'request_id': request_id, 'tags' : tags, 'userids' : userids })
        return direct_to_template(request, 'fbapp/challenge-pending.html', extra_context={'pending': pending})
    else:
        return HttpResponse("Error")

def challenge_history(request):
    uid = request.GET.get('uid', None)
    if uid:
        challengehistory = FBChallenge.objects.filter(receiver = uid, ).exclude(receiver_score = -1000000).exclude(sender_score = -1000000) | FBChallenge.objects.filter(sender = uid).exclude(receiver_score = -1000000).exclude(sender_score = -1000000)
        history = []
        for challenge in challengehistory:
            tags = challenge.quizes.tags
            other_receivers = FBChallenge.objects.filter(quizes = challenge.quizes).exclude(receiver_score = -1000000).exclude(sender_score = -1000000)
            userids = Set([])
            for o in other_receivers:
                userids.add(o.receiver)
                userids.add(o.sender)
            history.append({'tags' : tags, 'userids' : userids })

        return direct_to_template(request, 'fbapp/challenge-history.html', extra_context={'history': history})
    else:
        return HttpResponse("Error")

def challenge_end(request):
    uid = request.GET.get('uid', None)
    request_ids = request.GET.get('request_ids', None)
    challenge_id = request.GET.get('challenge_id', None)
    score =  request.GET.get('score', None)
    if uid:
        pending = []
        players = []
        if challenge_id:
            # receiver of a challenge
            challenge = FBChallenge.objects.filter(request_id = challenge_id).get()
            if challenge.receiver_score == -1000000:
                challenge.receiver_score = score
                challenge.save()
            for el in FBChallenge.objects.filter(quizes = challenge.quizes):
                if el.receiver_score == -1000000:
                    name = FBProfile.objects.get(uid = el.receiver).first_name
                    pending.append(name)
                else:
                    players.append({'userid': el.receiver, 'score': el.receiver_score}) 

            if challenge.sender_score == -1000000:
                pending.append(challenge.sender)
            else:
                players.append({'userid': challenge.sender, 'score': challenge.sender_score})

        elif request_ids:
            #sender of a challenge
            request_ids = request_ids.split(',')
            challengelist = []
            challenge = None
            for r in request_ids:
                challenge = FBChallenge.objects.filter(request_id = r).get()
                challenge.sender_score = score
                challenge.save()
                challengelist.append(challenge)
            for el in FBChallenge.objects.filter(quizes = challenge.quizes):
                if el.receiver_score == -1000000:
                    try:
                        name = FBProfile.objects.get(uid = el.receiver).first_name
                    except:
                        name = "altre persone"
                    pending.append(name)
                else:
                    players.append({'userid': el.receiver, 'score': el.receiver_score})
        return direct_to_template(request, 'fbapp/challenge-end.html', extra_context={'pending': ', '.join(pending), 'score': score, 'players': players})
    else:
        return HttpResponse("Error")


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
        try:
            user = User.objects.get(username='FB'+uid)
        except:
            user = User(username='FB'+uid, first_name=first_name, last_name=last_name,email=email, password="0", is_staff=False, is_active=True, is_superuser=False)
            user.save()
        #    if os.path.exists(settings.MEDIA_ROOT + 'fbpics/' +uid+ "." +pic_url[-3:]):
        #        u.pic.delete()
        try:
            fbuser = FBProfile.objects.get(uid=uid)
            if fbuser.user != user:
                fbuser.user=user
                fbuser.save()
        except:
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
    return render_to_response('fbapp/canvas.fbml', {},context_instance=RequestContext(request))
    #return direct_to_template(request, 'fbapp/canvas.fbml')#  extra_context={'fbuser': user})

#@facebook.require_login()
def ajax(request):
    return HttpResponse('hello world')
