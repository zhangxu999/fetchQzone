# -*- coding:utf8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect,HttpResponse
from fetchQzone.models import comment,feed,people
from django.db import connection

from django import forms
from datetime import datetime
import copy
import time
import json
import urllib
datetime_format = "%Y-%m-%d %H:%M:%S"
# Create your views here.
def upload(request):
    
    shuo=request.POST['shuo']
    shuo=urllib.parse.unquote(shuo)
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
            fe=feed(feedID=x['feedID'],info=x['info'],likeNum=int(x['likeNum']),time=datetime.strptime(x['time'],datetime_format),userID=peo,visitTime=datetime.strptime(x['visitTime'],datetime_format),commentNum=int(x['commentNum']))
            fe.save()
        except Exception as e:
            print("error in save feed")
            raise e

    for x in shuo['comment']:
        fe=feed(feedID=x['parent'])
        peo_come=people(qq=int(x['from']))
        peo_to=people(qq=int(x['to']))
        print(x['time'])
        comm=comment(IDinFeed=x['IDinFeed'],parent=fe,come=peo_come,to=peo_to,rootID=x['rootID'],time=datetime.strptime(x['time'],datetime_format),info=x['info'])
        comm.save()
    return HttpResponse('OKKKKK')
def search(request):

    #处理分页
    start=0;num=5;pagenum=num*10;
    if 'start' in request.GET: 
        start=int(request.GET['start'])
        num=int(request.GET['num'])
        pagenum=num*10
    fenye=[]
    for x in range(10):
        a={}
        a['start']=start-(start%pagenum)+x*num
        a['num']=num
        a['value']=start-start%pagenum+x*num+1
        if a['start']==start:
            a['strong']=True
        fenye.append(a)
    params={'last':start-num,'num':num,'next':start+num}
    #处理user 参数
    try:
        user=int(request.GET['user'])
        params['user']=user
    except :
        info='您的请求有误'
        return HttpResponse(info+'wrong!!!',status=404)
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

def feedDetail(request):
    try:
        feedID=request.GET["feedID"]
    except :
        return HttpResponse("wrong~~~")
    sql_feed="select fetchQzone_feed.info,fetchQzone_feed.time,fetchQzone_feed.userID_id ,fetchQzone_feed.feedID from fetchQzone_feed where fetchQzone_feed.feedID='%s' "% feedID
    sql_comment="select distinct parent_id,come_id,to_id,info,fetchQzone_comment.time,rootID from fetchQzone_comment where parent_id='%s' order by IDinFeed "% feedID
    cursor = connection.cursor()
    cursor.execute(sql_comment)
    comments=cursor.fetchall()
    cursor.execute(sql_feed)
    feeds=cursor.fetchall()
    return render(request,'fetchQzone/base_onefeed.html',{'feeds':feeds,'comments':comments})