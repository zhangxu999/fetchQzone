from django.db import models

# Create your models here.
class people(models.Model):
	"""docstring for people"""
	qq=models.BigIntegerField(primary_key=True);
class feed(models.Model):
	"""docstring for feed"""
	feedID=models.CharField(max_length=255,primary_key=True);
	userID=models.ForeignKey(people);
	time=models.BigIntegerField();
<<<<<<< HEAD
	info=models.TextField(null=True,blank=True);
=======
	info=models.TextField();
>>>>>>> fc87b078bf56697fa825af928909cbfee5fe787b
	commentNum=models.IntegerField();
	likeNum=models.IntegerField();
	visitTime=models.BigIntegerField();
class comment(models.Model):
	"""docstring for comment"""

	IDinFeed=models.IntegerField();
	parent=models.ForeignKey(feed);
	rootID=models.IntegerField();
	come=models.ForeignKey(people,related_name='come');
	to=models.ForeignKey(people,related_name='to');
	time=models.BigIntegerField();
<<<<<<< HEAD
	info=models.TextField(null=True,blank=True);
class nick(models.Model):
	"""de"""
	host=models.ForeignKey(people,related_name='host');
	guest=models.ForeignKey(people,related_name='guest');
	nick=models.CharField(max_length=30);
=======
	info=models.TextField();
>>>>>>> fc87b078bf56697fa825af928909cbfee5fe787b
