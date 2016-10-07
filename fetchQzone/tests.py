from django.test import TestCase
import urllib2
import json
from imp import reload
# Create your tests here.
from models import *
from query import queryTool
qu=queryTool()

class QueryTests(TestCase):
    def test_validate(self):
        """
        gogogog
        """
        user=738285867
        mm='ssss'
        self.assertEqual(qu.validate(user),True)
        self.assertEqual(qu.validate(mm),False)

    
