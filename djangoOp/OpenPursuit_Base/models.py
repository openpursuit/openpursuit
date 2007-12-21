from django.db import models

# Create your models here.

class Tags(models.Model):
	tag = models.CharField(max_length=2000)

class Languages(models.Model):
	language = models.CharField(max_length=200)

class Question(models.Model):
	question = models.CharField(max_length=2000)
	difficulty = models.IntegerField()
	score = models.IntegerField()
	date = models.DateTimeField('date inserted')
	tag = models.ManyToManyField(Tags)
	language = models.ManyToManyField(Languages)
	right1 = models.CharField(max_length=2000)	
	wrong1 = models.CharField(max_length=2000)	
	wrong2 = models.CharField(max_length=2000)	
	wrong3 = models.CharField(max_length=2000)
	class Admin:
       		pass


