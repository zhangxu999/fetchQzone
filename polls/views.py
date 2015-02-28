# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from polls.models import Choice,Poll
from django.utils import timezone
from forms import ContactFormWithMugshot
from mysite import settings
from django.core.files.base import File 
from django.views.generic import ListView
from polls.models import Choice
class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name='latest_poll_list'    
    def get_queryset(self):
        """return the last five published polls"""
        return Poll.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
class DetailView(generic.DetailView):
    model=Poll
    template_name='polls/detail.html'
class ResultsView(generic.DetailView):
    model=Poll
    template_name='polls/detail.html'

        
def index(request):
    latest_poll_list=Poll.objects.order_by('-pub_date')[:5]
    #template=loader.get_template('polls/index.html')
    #context=RequestContext(request,{'latest_poll_list':latest_poll_list,})
    #output=','.join([p.question for p in latest_poll_list])
    #return HttpResponse(template.render(context))
    context={'latest_poll_list':latest_poll_list}
    return render(request,'polls/index.html',context)
   
'''
def detail(request,poll_id):
    #return HttpResponse("you're looking at poll%s."%poll_id)
    try:
        poll=Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request,'polls/detail.html',{'poll':poll})
    
def results(request,poll_id):
    poll=get_object_or_404(Poll,pk=poll_id)
    return render(request,'polls/results.html',{'poll':poll})
    '''
def vote(request,poll_id):
    p=get_object_or_404(Poll,pk=poll_id)
    try:
        selected_choice=p.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{
            'poll':p,
            'error_message':'you didnt select a choice.',
            })
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(p.id,)))
def home(request):
    all=[]
    for ob in request.META.items():
        all.append(ob)
        all.append('<br>')
  
    return HttpResponse(all)
from django.core.files.uploadedfile import SimpleUploadedFile
def contact(request):
    if request.method=='POST':
        form=ContactFormWithMugshot(request.POST,request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            gender=form.cleaned_data['gender']
            university=form.cleaned_data['university']
            graduate=form.cleaned_data['graduate']
            mugshot=form.files['mugshot']
            ImgPath=UploadFile(mugshot)

            packege=[('name',name),('gender',gender),('university',university),('graduate',graduate)]

            
                
            return render(request,'polls/form_callback.html',{'packege':packege,'img':ImgPath})
    else:
        # file_data={'mugshot':SimpleUploadedFile('face.jpg',<file data>)}
        form=ContactFormWithMugshot()
    return render(request,'polls/form.html',{'form':form,})
def UploadFile(file):
    part='polls/'+file.name
    full='polls/static/'+part
    f=open(full,'wb')
    f.write(file.read())
    f.close()
    return  part
def hello(request):
    if request.method=='GET':
        return render(request,'polls/hello.html')
    else:
        a=request.POST['name']
        return HttpResponse('hello,'+a)

class genericChoice(ListView):
    """docstring for genericCh"""
    
    model=Choice
    template_name='index.html'


   