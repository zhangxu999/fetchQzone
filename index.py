#-*- coding:utf-8 -*-
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'


from django.core.handlers.wsgi import WSGIHandler
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(WSGIHandler())
