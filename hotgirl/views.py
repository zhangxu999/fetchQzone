#-*- coding: UTF-8 -*-
# Create your views here.
from django.views.generic import ListView
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect,HttpResponse
from Form import ContactForm
from hotgirl.models import boygirl
from hotgirl.models import final
from hotgirl.models import titles
from mysite import qiniuImage
import django.db 
from django.middleware import csrf
from django.views.decorators.csrf import csrf_protect
import copy
import time
import csv
from django.views.generic import TemplateView






'''
class index(object):
	"""docstring for index"""
	def __init__(self, arg):
		super(index, self).__init__()
		self.arg = arg
	Template_name=""
	def get(request):
		return render(request,Template_name,{"indexgirl":indexgirl})
'''
def indexView(request):
	return render(request,"hotgirl/index.html")
def UploadImageView(request):
    if request.method=='POST':
        forms=ContactForm(request.POST,request.FILES)
        
        if forms.is_valid():
            
            desc=forms.cleaned_data['desc']
            image=forms.files['image']
            ImgPath=UploadFile(image,desc)

        #    desc=[('desc',desc)]
        else  :
        	return HttpResponse("something wrong...")                
        return render(request,'hotgirl/uploadimage_callback.html',{'desc':desc,'img':ImgPath})
    else:
        # file_data={'mugshot':SimpleUploadedFile('face.jpg',<file data>)}
        forms=ContactForm()
        token=qiniuImage.getToken()
        csrftoken=csrf.get_token(request)
    return render(request,'hotgirl/uploadimage.html',{'form':forms,'token':token,'csrftoken':csrftoken})

def UploadFile(file,desc):
    part='hotgirl/'+str(int(time.time()))+file.name
    full='hotgirl/static/'+part
    f=open(full,'wb')
    f.write(file.read())
    f.close()
    WritePath2db(part,desc)
    return  part


def WritePath2db(path,desc):
   # django.db.close_connection()      
    girl=boygirl(mainmugshot=path,desc=desc,idnum=0)
    girl.save()
def addvotes(imgid):
    p=get_object_or_404(boygirl,pk=imgid)
    p.votes+=1
    p.save()    
#return json ,it's request url('/girl/getnext')
def getnext(request):
    a=request.GET['imgid']
    addvotes(int(a))
    RawSql='select id,votes,mainmugshot from hotgirl_boygirl  order by rand() limit 2'
    return HttpResponse(querynext(frm='ajax',RawSQL=RawSql))

def vote(request):
    #rand() is very mystery
    RawSql='select id,votes,mainmugshot from hotgirl_boygirl  order by rand() limit 2'
    return render(request,'hotgirl/votetest.html',{'girls':querynext(frm='firs',RawSQL=RawSql)})

def Template_test(request):
    RawSql='select id,votes,mainmugshot from hotgirl_boygirl  order by votes;'
    var=querynext('frm',RawSql)
    return render(request,'hotgirl/Template_test.html',{'test':var})
def top(request):
    start=0;num=3;pagenum=num*10;
    if 'start' in request.GET: 
        start=int(request.GET['start'])
        num=int(request.GET['num'])
        pagenum=num*10
    RawSql='select id,votes,mainmugshot from hotgirl_boygirl  order by votes desc limit %s,%s;'%(start,num)
    girls=querynext('top',RawSql)
   # params={'last':(start-start%pagenum-pagenum),'num':num,'next':(start-(start%pagenum)+pagenum)}
    params={'last':start-num,'num':num,'next':start+num}
    fenye=[]
    for x in xrange(10):
        a={}
        a['start']=start-(start%pagenum)+x*num
        a['num']=num
        a['value']=start-start%pagenum+x*num+1;
        if a['start']==start:
            a['strong']=True
        fenye.append(a)
    return render(request,'hotgirl/top.html',{'girls':girls,'fenye':fenye,'params':params})

def querynext(frm,RawSQL):
    
    #I am confused about the resulte,maybe it was becasue python lanuage.
    girls=boygirl.objects.raw(RawSQL)
    return genedict(frm,girls)
def genedict(frm,RawQuerySet,):
    if(frm=='ajax'):
        static='http://ncwugirl.qiniudn.com/'
        Suffix='-normal2'
        dicts=[]
        for one in RawQuerySet:
            a=[]
            a.append(one.id)
            a.append(one.votes)
            a.append(one.mainmugshot)
            dicts.append(a)
        return '{"img":[{"imgid":"'+str(dicts[0][0])+'","vote":"'+str(dicts[0][1])+'","src":"'+static+dicts[0][2]+Suffix+'"},{"imgid":"'+str(dicts[1][0])+'","vote":"'+str(dicts[1][1])+'","src":"'+static+dicts[1][2]+Suffix+'"}]}'        
    else:
        dicts=[]
        for one in RawQuerySet:
            a={}
            a['id']=one.id
            a['votes']=one.votes
            a['mainmugshot']=one.mainmugshot
            dicts.append(a)
        return dicts 



def qnCallback(request):
    name="name"
    desc="desc"
    name=request.POST['name']
    desc=request.POST['desc']
    bucket=request.POST['bucket']
    mimeType=request.POST['mimeType']
    WritePath2db(path=name,desc=desc)
    return HttpResponse('{"success":true,"name":"'+name+'"}')
def resp(request):
   # print("XXXXXXXXXX:      "+request.GET['m'])
    token=csrf.get_token(request)
    return HttpResponse('{"success":true,"token":"'+token+'"}')
def qncallback_test(request):
    return render(request,"hotgirl/qncallback_test.html")
def finnal(request):
    return render(request,'hotgirl/finalchoose.html');
def procFinal(request):
    idnum=' ';name=' ';title1=' ';teacher1=' ';title2=' ';teacher2=' ';title3=' ';teacher3=' ';
    idnum=request.POST['idnum']
    name=request.POST['yourname']
    title1=request.POST['title1']
    teacher1=request.POST['teacher1']
    title2=request.POST['title2']
    teacher2=request.POST['teacher2']
    title3=request.POST['title3']
    teacher3=request.POST['teacher3']
    #write to database
    onefinal=final(idnum=idnum,name=name,title1=title1,teacher1=teacher1,title2=title2,teacher2=teacher2,title3=title3,teacher3=teacher3)
    onefinal.save()
    return  HttpResponseRedirect("/girl/finalresualt")
def finalResualt(request):
    #RawSql='select id idnum,name,title1,teacher1,title2,teacher2,title3,teacher3 from hotgirl_final '
    try:
        classes=int(request.GET["classes"])
        RawSql='select * from hotgirl_final where idnum>=%s AND idnum<%s order by idnum asc'% (classes*100,classes*100+99)
    except Exception, e:
        RawSql='select * from hotgirl_final order by idnum asc'

    finals=final.objects.raw(RawSql)
    dicts=[]
    tmp=[]
    for one in finals:
        a={}
        a['idnum']=one.idnum
        a['name']=one.name

        tmp=getRealTitle(one.title1)
        a['title1']=tmp[0]
        a['realtitle1']=tmp[1]
        a['teacher1']=one.teacher1
        
        tmp=getRealTitle(one.title2)
        a['title2']=tmp[0]
        a['realtitle2']=tmp[1]
        a['teacher2']=one.teacher2
        
        tmp=getRealTitle(one.title3)
        a['title3']=tmp[0]
        a['realtitle3']=tmp[1]
        a['teacher3']=one.teacher3
        dicts.append(a)
    return render(request,'hotgirl/finalresult.html',{'finals':dicts})
    #return dicts
def gettitles(request):
    try:
        begin=int(request.GET["begin"])
        end=int(request.GET["end"])
        RawSql='select * from hotgirl_titles where idnum>=%s AND idnum<=%s'%(begin,end)
    except Exception, e:
        RawSql='select * from hotgirl_titles'
    alltitles=titles.objects.raw(RawSql)
    dicts=[]
    for one in alltitles:
        a={}
        a['idnum']=one.idnum
        a['title']=one.title
        a['teacher']=one.teacher
        dicts.append(a)
    return render(request,'hotgirl/alltitles.html',{'alltitles':dicts})
def getRealTitle(string):
    realtitle=string
    try :
        num=int(string)
        RawSql="select * from hotgirl_titles where idnum=%s" % num
        title=titles.objects.raw(RawSql)
        try:
            realtitle=title[0].title
        except :
            pass
        return [string,realtitle]
    except Exception, e:
        string="自定"
        return [string,realtitle]
def genecsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="课设题目选择结果.csv"'

    writer = csv.writer(response)

    RawSql='select * from hotgirl_final order by idnum asc'
    finals=final.objects.raw(RawSql)
    writer.writerow(["学号","姓名","毕设1编号","题目","指导老师","毕设2编号","题目","指导老师","毕设3编号","题目","指导老师"])
    for one in finals:
        realtitle1=getRealTitle(one.title1)
        realtitle2=getRealTitle(one.title2)
        realtitle3=getRealTitle(one.title3)
        writer.writerow([one.idnum,one.name,realtitle1[0],realtitle1[1],one.teacher1,realtitle2[0],realtitle2[1],one.teacher2,realtitle3[0],realtitle3[1],one.teacher3])
    return response

class AboutView(TemplateView):
    template_name="hotgirl/about.html"
class gettitlesView(ListView):
    def getqueryset():
        try:
            begin=int(request.GET["begin"])
            end=int(request.GET["end"])
            RawSql='select * from hotgirl_titles where idnum>=%s AND idnum<=%s'%(begin,end)
        except Exception, e:
            RawSql='select * from hotgirl_titles'
        alltitles=titles.objects.raw(RawSql)
        return alltitles
    queryset=getqueryset()
    context_object_name='alltitles'
    template_name='hotgirl/alltitles.html'
