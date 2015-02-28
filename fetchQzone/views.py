# -*- coding:utf8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect,HttpResponse
<<<<<<< HEAD
from fetchQzone.models import comment,feed,people,nick
from django.db import connection
=======
from fetchQzone.models import comment,feed,people
from django.db import connection

>>>>>>> fc87b078bf56697fa825af928909cbfee5fe787b
from django import forms
import copy
import time
import json
import urllib2
<<<<<<< HEAD
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

=======
# Create your views here.
def upload(request):
    
    shuo=request.POST['shuo']
    shuo=urllib2.unquote(shuo)
    shuo=json.loads(shuo)
    
    print(shuo['feed'][1])
    print(shuo['owner'])
    peo=people(qq=int(shuo['owner']))
    peo.save()
    for x in shuo['people']:
        ppeo=people(qq=int(x))
        ppeo.save()

    for x in shuo['feed']:
        try:
            peo=people(qq=int(x['userID']))
            fe=feed(feedID=x['feedID'],info=x['info'],likeNum=int(x['likeNum']),time=int(x['time']),userID=peo,visitTime=int(x['visitTime']),commentNum=int(x['commentNum']))
            fe.save()
        except :
            print("error in save feed")

    for x in shuo['comment']:
        fe=feed(feedID=x['parent'])
        peo_come=people(qq=int(x['from']))
        peo_to=people(qq=int(x['to']))
        comm=comment(IDinFeed=x['IDinFeed'],parent=fe,come=peo_come,to=peo_to,rootID=x['rootID'],time=int(x['time']),info=x['info'])
        comm.save()
>>>>>>> fc87b078bf56697fa825af928909cbfee5fe787b
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
<<<<<<< HEAD
    #处理user,friend参数
    friend=None;
=======
    #处理user 参数
>>>>>>> fc87b078bf56697fa825af928909cbfee5fe787b
    try:
        user=int(request.GET['user'])
        params['user']=user
    except :
        info='您的请求有误'
        return HttpResponse(info+'wrong!!!',status=404)
<<<<<<< HEAD
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
=======
    #处理friend 参数
    try:
        friend=int(request.GET['friend'])
        sql_feed="select distinct fetchQzone_feed.info,fetchQzone_feed.time,fetchQzone_feed.userID_id,fetchQzone_feed.feedID from fetchQzone_comment,fetchQzone_feed where  ((come_id=%s AND to_id=%s) OR (come_id=%s AND to_id=%s) ) AND fetchQzone_comment.parent_id=fetchQzone_feed.feedID order by fetchQzone_feed.userID_id,fetchQzone_feed.time desc limit %s,%s"%(user,friend,friend,user,start,num)
        sql_comment="select distinct parent_id,come_id,to_id,info,fetchQzone_comment.time,rootID from fetchQzone_comment where ((come_id=%s AND to_id=%s) OR (come_id=%s AND to_id=%s)) order by fetchQzone_comment.parent_id,fetchQzone_comment.IDinfeed"% (user,friend,friend,user)
        sql_friend="select uni.qq,count(1) as cnt from (select come_id as qq from fetchQzone_comment where to_id=%s union all select to_id  as qq from fetchQzone_comment where come_id=%s )uni where qq!=%s group by uni.qq order by cnt desc limit 0,15"%(user,user,user)
        params['friend']=friend
    except :
        sql_feed="select distinct fetchQzone_feed.info,fetchQzone_feed.time,fetchQzone_feed.userID_id,fetchQzone_feed.feedID from fetchQzone_feed where fetchQzone_feed.userID_id=%s order by fetchQzone_feed.time desc limit %s,%s"%(user,start,num)
        sql_comment="select distinct parent_id,come_id,to_id,fetchQzone_comment.info,fetchQzone_comment.time,rootID from fetchQzone_comment,("+sql_feed+")fe where fetchQzone_comment.parent_id=fe.feedID order by fetchQzone_comment.parent_id,fetchQzone_comment.IDinfeed"
        sql_friend="select uni.qq,count(1) as cnt from (select come_id as qq from fetchQzone_comment where to_id=%s union all select to_id  as qq from fetchQzone_comment where come_id=%s )uni where qq!=%s group by uni.qq order by cnt desc limit 0,15"%(user,user,user)
    cursor = connection.cursor()
    #得到评论List，装配结果
    cursor.execute(sql_comment)
    comments=cursor.fetchall()
    #得到说说List，
    cursor.execute(sql_feed)
    feeds=cursor.fetchall()
    #得到朋友们列表
    cursor.execute(sql_friend)
    friends=cursor.fetchall()
    #return [feeds,comments,sql_feed,sql_comment]
    return render(request,'fetchQzone/base_allfeeds.html',{'feeds':feeds,'comments':comments,'friend':friends,'fenye':fenye,'params':params})
>>>>>>> fc87b078bf56697fa825af928909cbfee5fe787b

def feedDetail(request):
    try:
        feedID=request.GET["feedID"]
    except :
        return HttpResponse("wrong~~~")
<<<<<<< HEAD
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
=======
    sql_feed="select fetchQzone_feed.info,fetchQzone_feed.time,fetchQzone_feed.userID_id ,fetchQzone_feed.feedID from fetchQzone_feed where fetchQzone_feed.feedID='%s' "% feedID
    sql_comment="select distinct parent_id,come_id,to_id,info,fetchQzone_comment.time,rootID from fetchQzone_comment where parent_id='%s' order by IDinFeed "% feedID
    cursor = connection.cursor()
    cursor.execute(sql_comment)
    comments=cursor.fetchall()
    cursor.execute(sql_feed)
    feeds=cursor.fetchall()
    return render(request,'fetchQzone/base_onefeed.html',{'feeds':feeds,'comments':comments})
>>>>>>> fc87b078bf56697fa825af928909cbfee5fe787b
