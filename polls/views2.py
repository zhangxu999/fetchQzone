from django.http import HttpResponse
from django.views.generic import ListView

class MyView(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
	def get(self,request):
		return HttpResponse('result')
		
		



