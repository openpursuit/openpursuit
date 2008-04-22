from django.db import models
from django.contrib.auth.models import User

DIFFICULTY_LEVEL = (
    (1, 'easy'),
    (2, 'medium'),
    (3, 'hard'),
)

MEDIA_TYPE = (
    (1, 'text'),
    (2, 'image'),
    (3, 'audio'),
    (4, 'video'),
)

SCORE_TYPE = (
	(0, 'negative'),
	(1, 'positive'),

)

gettext_noop = lambda s: s

LANGUAGES = (
    ('it', gettext_noop('Italian')),
    ('ja', gettext_noop('Japanese')),
    ('de', gettext_noop('German')),
    ('el', gettext_noop('Greek')),
    ('en', gettext_noop('English')),
    ('es', gettext_noop('Spanish')),
    ('fr', gettext_noop('French')),
    ('pt', gettext_noop('Portugese')),
    ('nl', gettext_noop('Dutch')),


)


class Tags(models.Model):
	tag = models.CharField(max_length=2000)
	
	def __str__(self):	
		return "%s" % (self.tag)




class Quiz(models.Model):
	"""
	The Quiz data model
	"""
	#Question and right and wrong answers
	question = models.CharField("Question", max_length=2000, blank=True)
	right1 = models.CharField("Right answer", max_length=2000)
	wrong1 = models.CharField("First wrong answer", max_length=2000)	
	wrong2 = models.CharField("Second wrong answer",max_length=2000)	
	wrong3 = models.CharField("Third wrong answer",max_length=2000)
	#Tags (many to many) of the question 
	tags = models.ManyToManyField(Tags)
	#Two char language code ISO 639-1 
	#For more info go to http://www.loc.gov/standards/iso639-2/php/English_list.php
	#Or here : http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
	lang = models.CharField("Language", max_length=5, choices=LANGUAGES) 
	#statistics
	difficulty = models.IntegerField("Difficulty", choices=DIFFICULTY_LEVEL) 
	views = models.IntegerField("Views")
	date = models.DateTimeField("Date of intertion")
	author = models.ForeignKey(User)
	# score
	# referenced back by Score class
	#Spam signalations signalled by "reporter" users, could put the question in quarantine
	quarantine = models.BooleanField("Quarantine status", default=False)

	#For multimedia question
	mediatype = models.IntegerField("Media type", choices=MEDIA_TYPE)
	attachment = models.FileField("Attachment", upload_to='multimedia')
	#Url with a reference of where to find the right answer and more info about the question topic
	reference = models.URLField("A website url with in-depth information about the quiz")
	class Admin:
		date_hierarchy = 'date'
		list_display = ('question', 'author')
		list_filter = ('author','date')
		pass

	def __unicode__(self):
		return "%s" % (self.question)

class Report(models.Model):
	"""
	Abuse / OffTopic ticket to moderators
	"""
	reason = models.TextField("Reason to reporting")
	quiz = models.ForeignKey(Quiz)
	reporter = models.ForeignKey(User)
	date = models.DateTimeField("Date of intertion")
	class Admin:
		date_hierarchy = 'date'
		list_display = ('quiz', 'reporter')
		list_filter = ('quiz', 'reporter')
		pass
	def __unicode__(self):
		return "%s" % (self.quiz)
	
class Score:
	"""
	Users are allowed to vote quiz through positive or negative Score
	"""
	value = models.IntegerField("Score value", choices=SCORE_TYPE)
	voter = models.ForeignKey(User)
	quiz = models.ForeignKey(Quiz)
	date = models.DateTimeField("Date of intertion")
	class Admin:
		pass
	
class UserProfile(models.Model):
	"""
	Some additional field about users
	"""
	user = models.ForeignKey(User, unique=True)
	# more profile info
	# language, personalIcon, website  etc etc could be added later
	#statistic
	trusted_user = models.BooleanField("Trusted user status",default=False) 
	gamescore =  models.IntegerField("User's game score") # for online game score
	class Admin:
		pass
		
	def __unicode__(self):
		return "%s" % (self.user)
