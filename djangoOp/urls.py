from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import amf.django
admin.autodiscover()

urlpatterns = patterns('',
    # Example:

     (r'^admin/(.*)', admin.site.root),
     (r'^$', 'djangoOp.op.views.index'),
     (r'^static/(.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT  }), 
     (r'^base/', include('djangoOp.op.urls')),
     (r'^accounts/', include('djangoOp.registration.urls')),
     (r'^gateway/getQuiz4Flash/(.*)', 'amf.django.views', {'views':'op.flashview'}), #1
#     (r'^api/', include('api.urls')),
     (r'^facebook/', include('djangoOp.facebookconnect.urls')),
     (r'^api/getquiz', 'djangoOp.op.views.getquizapi'),
     (r'^fbapp/main', 'fbapp.views.main'), 
     (r'^fbapp/facebook_login', 'fbapp.views.fb_login'), 
     (r'^fbapp/save_score', 'fbapp.views.save_score'), 
     (r'^fbapp/play2', 'fbapp.views.play2'), 
     (r'^fbapp/play3', 'fbapp.views.play3'), 
     (r'^fbapp/play', 'fbapp.views.play'), 
     (r'^fbapp/addquiz', 'fbapp.views.addquiz'), 
     (r'^fbapp/challenge-info', 'fbapp.views.challenge_info'), 
     (r'^fbapp/challenge-menu', 'fbapp.views.challenge_menu'), 
     (r'^fbapp/challenge-end', 'fbapp.views.challenge_end'), 
     (r'^fbapp/challenge-history', 'fbapp.views.challenge_history'), 
     (r'^fbapp/challenge-pending', 'fbapp.views.challenge_pending'), 
     (r'^fbapp/challenge-create', 'fbapp.views.challenge_create'), 
#     (r'^fbapp/xd_proxy.php', 'fbapp.views.channel'),
#     (r'^fbapp/channel.htm', 'fbapp.views.channel'),
     (r'^fbapp/', 'fbapp.views.canvas'),
)

