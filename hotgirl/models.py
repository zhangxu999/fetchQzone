from django.db import models

# Create your models here.
class boygirl(models.Model):
	"""docstring for boygirl"""
	
	idnum=models.IntegerField()
	name=models.CharField(max_length=20)
	gender=models.BooleanField(default=True)
	mainmugshot=models.URLField()
	votes=models.IntegerField(default=0)
	desc=models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

class final(models.Model):
	name=models.CharField(max_length=30)
	idnum=models.IntegerField(primary_key=True)
	title1=models.CharField(max_length=1000)
	teacher1=models.CharField(max_length=30)
	title2=models.CharField(max_length=1000)
	teacher2=models.CharField(max_length=30)
	title3=models.CharField(max_length=1000)
	teacher3=models.CharField(max_length=30)
class titles(models.Model):
	idnum=models.IntegerField(primary_key=True)
	title=models.CharField(max_length=1000)
	teacher=models.CharField(max_length=30)
		
