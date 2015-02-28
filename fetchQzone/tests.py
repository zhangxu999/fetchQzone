from django.test import TestCase
import urllib2
import json
from imp import reload
# Create your tests here.
shuo=[];
def testnick():
    global shuo
    shuo=open("a.txt",'r').read()
    shuo=urllib2.unquote(shuo)
    shuo=json.loads(shuo)
    
    
