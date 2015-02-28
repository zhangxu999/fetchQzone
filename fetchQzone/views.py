# -*- coding:utf8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect,HttpResponse
from fetchQzone.models import comment,feed,people,nick
from django.db import connection
from django import forms
import copy
import time
import json
import urllib2
from fetchQzone import querytool
def upload(request):
    print('1111111111111')
    shuo=request.POST["shuo"]
    shuo=urllib2.unquote(shuo)
    shuo=json.loads(shuo)
    
    print(shuo['feed'][0])
    print(shuo['owner'])
    people(pk=int(shuo['owner'])).save();
    people(pk=int(shuo['visitor'])).save();

   # people.objects.get_or_create(pk=int(shuo['owner']))
   
    notInpeoples=filter(lambda x : not people.objects.filter(pk=x).exists(),shuo['people'])
    allpeople=map(lambda x: people(pk=x),notInpeoples)
    people.objects.bulk_create(allpeople)

    notInfeeds=filter(lambda x:not feed.objects.filter(pk=x["feedID"]).exists(),shuo['feed'])
    allfeed=map(lambda x:feed(feedID=x["feedID"],info=x['info'],likeNum=int(x['likeNum']),time=int(x['time']),userID_id=int(x["userID"]),visitTime=int(x['visitTime']),commentNum=int(x['commentNum'])),notInfeeds)
    feed.objects.bulk_create(allfeed)

    notIncomments=filter(lambda x : not comment.objects.filter(IDinFeed=x['IDinFeed'],parent_id=x['parent'],come_id=x['from'],to_id=x['to']).exists(),shuo['comment'])
    allcomment=map(lambda x:comment(IDinFeed=x['IDinFeed'],parent_id=x['parent'],come_id=int(x['from']),to_id=int(x['to']),rootID=x['rootID'],time=int(x['time']),info=x['info']),notIncomments)
    comment.objects.bulk_create(allcomment)

    

    #若visitor 为0，则用户未登录，此时是用户默认昵称
    visitor=int(shuo['visitor'])
    map(lambda x:people.objects.get_or_create(qq=x[0]),shuo['nick'].items())
    notInnicks=filter(lambda x : not nick.objects.filter(host__pk=visitor,guest__pk=x[0],nick=x[1]).exists(),shuo['nick'].items())
    Innicks=filter(lambda x : nick.objects.filter(host__pk=visitor,guest__pk=x[0]).exists(),shuo['nick'].items())
    allnick=map(lambda x: nick(host_id=visitor,guest_id=x[0],nick=x[1]),notInnicks)
    map(lambda x:nick.objects.filter(host__pk=visitor,guest__pk=x[0]).update(nick=x[1]),Innicks)
    nick.objects.bulk_create(allnick)

    '''
    try:
        host=people.objects.get(qq=owner)
        guest=people.objects.get(qq=int(x))
        ni=nick(host=host,guest=guest,nick=y)
        ni.save()
    except:
        pass
    '''

    return HttpResponse('OKKKKK')
def search(request):

    #处理分页
    start=0;num=5;pagenum=num*10;
    if 'start' in request.GET: 
        start=int(request.GET['start'])
        num=int(request.GET['num'])
        pagenum=num*10
    fenye=[]
    for x in xrange(10):
        a={}
        a['start']=start-(start%pagenum)+x*num
        a['num']=num
        a['value']=start-start%pagenum+x*num+1
        if a['start']==start:
            a['strong']=True
        fenye.append(a)
    params={'last':start-num,'num':num,'next':start+num}
    #处理user,friend参数
    friend=None;
    try:
        user=int(request.GET['user'])
        params['user']=user
    except :
        info='您的请求有误'
        return HttpResponse(info+'wrong!!!',status=404)
    try:
        friend=int(request.GET['friend'])
        params['friend']=friend

    except:
        pass
    if not querytool.validate(user,friend,start,num):
        return HttpResponse("paragrmas wrong !",status=404)
    params['user_nick']=querytool.getNick(guest_id=user)
    params['friend_nick']=querytool.getNick(guest_id=friend)
    reslut=querytool.getResult(user,start,num,friend)
    reslut['fenye']=fenye
    reslut['params']=params
    reslut['m']={'738285867':'qq','b':'ww'}
    '''
    print(reslut['feeds'])
    print(reslut['comments'])
    print(reslut['friend'])
    print(reslut['fenye'])
    print(reslut['params'])
    '''
    if friend==None:
        Template='fetchQzone/base_allfeeds.html'
    else:
        Template='fetchQzone/feedwithfriend.html'
    return render(request,Template,reslut)

def feedDetail(request):
    try:
        feedID=request.GET["feedID"]
    except :
        return HttpResponse("wrong~~~")
    Result=querytool.getFeedDetail(feedID)
    return render(request,'fetchQzone/base_onefeed.html',Result)
def index(request):
    print("index")
    Result={}
    Result['feedtop']=querytool.getFeedTop()
    Result['commenttop']=querytool.getCommentTop()
    Result['peopletop']=querytool.get_peopleTop()
    print(Result)
    return render(request,"fetchQzone/index.html",Result)
def getnick(request):
    '''
    print("befo")
    mm=nick.objects.all()

    print("after")
    cont=" "
    for x in mm:
        cont+=(str(x.host.qq)+" :~~~ "+str(x.guest.qq)+":%%  "+str(x.nick)+"<br>")
    #return HttpResponse(cont)
    '''
    return render(request,'fetchQzone/index.html')