from django.db import models
from django.contrib.auth.models import User

DIFFICULTY_LEVEL = (
    (1, 'Trivial'),
    (2, 'Easy'),
    (3, 'Medium'),
    (4, 'Hard'),
    (5, 'Almost Impossible')
)


class Tags(models.Model):
	tag = models.CharField(max_length=2000)

class Question(models.Model):
	"""
	Basic Question data model
	"""
	#Question and right and wrong answers
	question = models.CharField(max_length=2000)
	right1 = models.CharField(max_length=2000)
	wrong1 = models.CharField(max_length=2000)	
	wrong2 = models.CharField(max_length=2000)	
	wrong3 = models.CharField(max_length=2000)
	#Tags (many to many) of the question 
	tag = models.ManyToManyField(Tags)
	#Two char language code ISO 639-1 
	#For more info go to http://www.loc.gov/standards/iso639-2/php/English_list.php
	#Or here : http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
	lang = models.CharField(max_length=2) 
	#statistics
	difficulty = models.IntegerField(choices=DIFFICULTY_LEVEL)
	views = models.IntegerField()
	date = models.DateTimeField('date inserted')
	#Spam signalations signalled by "reporter" users, could put the question in quarantine
	spamfeedback = models.IntegerField()
	quarantine = models.BooleanField(default=False)
	reporter = models.ManyToManyField(User)
	#For multimedia question
	#mediatype should be something like "text", "image", "audio", "video"
	mediatype = models.CharField(max_length=10)
	attachment = models.FileField(upload_to='multimedia')
	#Url with a reference of where to find the right answer and more info about the question topic
	reference = models.URLField()
	class Admin:
       		pass

class UserProfile(models.Model):
	"""
	This class contains some additional field about users
	"""
	user = models.ForeignKey(User, unique=True)
	# more profile info
	# language, personalIcon, website  etc etc could be added later
	#statistic
	score =  models.IntegerField() # how many question uploaded

