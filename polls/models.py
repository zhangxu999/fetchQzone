from django.utils import timezone
from django.db import models
import datetime


# Create your models here.
class Poll(models.Model):
    question=models.CharField(max_length=200)
    pub_date=models.DateTimeField('data published')
    hello=models.CharField('dajiahao',max_length=20)
    def __unicode__(self):
        return self.question
    def was_published_recently(self):
        now=timezone.now()
        return now-datetime.timedelta(days=1)<=self.pub_date<now
        #return self.pub_date >=timezone.now()-datetime.timedelta(days=1)
    was_published_recently.admin_order_filed='pub_date'
    was_published_recently.boolean=True
    was_published_recently.short_description='Published recently?'
    def hello(self):
        return 'hellos'
    
class Choice(models.Model):
    poll=models.ForeignKey(Poll)
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)
    def __unicode__(self):
        return self.choice_text
