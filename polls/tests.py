"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from polls.models import Poll

    def test_was_published_recently_with_future_poll(self):
        '''was_published_recently() should return False for polls whose pub_date
        '''was_published_recently() should return False for polls whose pub_date
            is in the future
        '''
        future_poll=Poll(pub_date=timezone.now()+datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(),False)

        """t_was_publisheed_recently_with_old_poll(self):
        """
    was_published_recently() should return False for polls whose pub_datwe is       older than 1 day
        """
        old_poll=Poll(pub_date=timezone.now()-datetime.timedelta(days=30))
        self.assertEqual(old_poll.was_published_recently(),False)

    def test_was_pblished_recently_recent_poll(self):
        """
    was_published-recently()should return Ture for polls whise pub_dayte
    is within thelast day
        """
        recent_poll=Poll(pub_date=timezone.now()-datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently().True)

def create_poll(question,day):
    return Poll.objects.create(question=question,pub_date=timezone.now()+datetime.timedelta(days=days))
class PollViewTests(TestCase):
    def test_index_view_no_polls(self):
        response=self.clinet.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self,assertContains(response,"No Polls areavaliable.")
        slef.assertQuertsetEqual(response.context['latest_poll_list'],[])
    def test_index_view_with_a past_poll(self):
        create_poll(question='Past poll",days=-30)
        response=self.client.get(reverse('polls:inde'))
        
    