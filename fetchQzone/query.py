from models import people,comment,feed,nick
from django.db import connection
import types
class queryTool(object):
    """docstring for queryTool"""
    def __init__(self):    
        
        sql_tmpfeed="create table tmp_feed select info,time,userID_id,feedID,nick from fetchQzone_feed,fetchQzone_nick limit 5;delete from tmp_feed;"
        sql_tmpcomment="create table tmp_comment select parent_id,come_id,to_id,info,fetchQzone_comment.time,rootID from fetchQzone_comment limit 5;delete from tmp_comment;"
        sql_tmpnick="create table sql_tmpnick "
        for x in (sql_tmpfeed,sql_tmpcomment):
            try:
                cursor.execute(x)
            except :
                pass
    def validate(self,user="not num",friend=1,start=1,num=1):
        if type(user)!=types.IntType and type(user)!=types.LongType:
            return False
        if type(friend)!=types.IntType and type(friend)!=types.LongType and friend!=None :
            return False
        if type(start)!=types.IntType :
            return False
        if type(num)!=types.IntType :
            return False 
        return True
       
    def getResult(self,user,start,num,friend=None):
        Result={}
        cursor = connection.cursor()
        if friend==None:
            sql_feed="insert into tmp_feed select info,time,userID_id,feedID,(select nick from fetchQzone_nick where  guest_id=userID_id group by guest_id) as nick from fetchQzone_feed where userID_id=%s  order by time  desc limit %s,%s ;"%(user,start,num)
            sql_comment=" insert into tmp_comment select parent_id,come_id,to_id,fetchQzone_comment.info,fetchQzone_comment.time,rootID from tmp_feed,fetchQzone_comment where parent_id=feedID  order by IDinFeed "
            sql_nick="insert into tmp_nick select guest_id,nick "
            sql_FeedtoRe="select * from tmp_feed;"
            sql_CommenttoRe="select parent_id,come_id,to_id,info,time,rootID,(select nick from fetchQzone_nick where  guest_id=come_id group by guest_id) as come_nick,(select nick from fetchQzone_nick where  guest_id=to_id group by guest_id) as to_nick from tmp_comment;"
            cursor.execute("delete from tmp_feed;")
            cursor.execute(sql_feed)
            cursor.execute("delete from tmp_comment;")
            cursor.execute(sql_comment)
            
            cursor.execute(sql_FeedtoRe)
            Result["feeds"]=cursor.fetchall()
            cursor.execute(sql_CommenttoRe)
            Result["comments"]=cursor.fetchall()
        else:
            sql_comment=" insert into tmp_comment select parent_id,come_id,to_id,info,time,rootID from fetchQzone_comment where (come_id=%s and to_id=%s) OR (come_id=%s and to_id=%s ) order by parent_id,IDinFeed "%(user,friend,friend,user)
            sql_Feed="insert into tmp_feed select fetchQzone_feed.info,time,userID_id,feedID,(select nick from fetchQzone_nick where  guest_id=userID_id group by guest_id) as come_nick from (select  distinct parent_id   from tmp_comment limit %s,%s )fee,fetchQzone_feed  where parent_id=feedID order by feedID,time"%(start,num)
            sql_CommenttoRe="select parent_id,come_id,to_id,tmp_comment.info,tmp_comment.time,rootID,(select nick from fetchQzone_nick where guest_id=come_id group by guest_id) as come_nick,(select nick from fetchQzone_nick where  guest_id=to_id  group by guest_id) as to_nick from tmp_comment,tmp_feed where parent_id=feedID order by feedID;"
            sql_FeedtoRe="select * from tmp_feed"
            cursor.execute("delete from tmp_comment;")
            cursor.execute(sql_comment)
            cursor.execute("delete from tmp_feed")
            cursor.execute(sql_Feed)
            cursor.execute(sql_CommenttoRe)
            
            Result["comments"]=cursor.fetchall()        

            cursor.execute(sql_FeedtoRe)
            Result["feeds"]=cursor.fetchall()
        sql_FriendtoRe="select uni.qq,count(1)  as cnt,nick  from (select come_id as qq from fetchQzone_comment where to_id=%s union all select to_id  as qq from fetchQzone_comment where come_id=%s )uni,fetchQzone_nick where qq!=%s and (guest_id=uni.qq) group by uni.qq order by cnt desc limit 0,15"%(user,user,user)
        cursor.execute(sql_FriendtoRe)
        Result["friend"]=cursor.fetchall()
        return Result
    def getFeedDetail(self,feedID):
        Result={}
        sql_FeedtoRe="select fetchQzone_feed.info,fetchQzone_feed.time,fetchQzone_feed.userID_id ,fetchQzone_feed.feedID,nick from fetchQzone_feed,fetchQzone_nick where fetchQzone_feed.feedID='%s' and ( host_id=0 and guest_id=userID_id) "% feedID
       # sql_comment="select distinct parent_id,come_id,to_id,info,fetchQzone_comment.time,rootID from fetchQzone_comment where parent_id='%s' order by IDinFeed "% feedID
        sql_CommenttoRe="select parent_id,come_id,to_id,info,time,rootID,(select nick from fetchQzone_nick where guest_id=come_id group by guest_id) AS come_nick,(select nick from fetchQzone_nick where guest_id=to_id group by guest_id) AS to_nick from fetchQzone_comment where parent_id='%s' order by IDinFeed"% feedID
        cursor = connection.cursor()
        cursor.execute(sql_CommenttoRe)
        Result["comments"]=cursor.fetchall()        
        cursor.execute(sql_FeedtoRe)
        Result["feeds"]=cursor.fetchall()
        return Result
    def getNick(self,guest_id,host_id=0):
        try:
            ni=nick.objects.filter(guest_id=guest_id)[0].nick
            return ni
        except:
            return "  "
    def getFeedTop(self,feedNum=5):
        sql_feedTop="select  userID_id qq, count(1) as cnt,(select nick from fetchQzone_nick where guest_id=userID_id limit 1) AS nick  from fetchQzone_feed group by userID_id order by cnt desc limit %s;"%feedNum
        cursor = connection.cursor()
        cursor.execute(sql_feedTop)
        return cursor.fetchall()
    def getCommentTop(self,commentNum=5):
        sql_commentTop=" select  come_id qq, count(1) as cnt,(select nick from fetchQzone_nick where guest_id=come_id limit 1) AS nick from fetchQzone_comment group by come_id order by cnt desc limit %s;"%commentNum
        cursor = connection.cursor()
        cursor.execute(sql_commentTop)
        return cursor.fetchall()
    def get_peopleTop(self,peopleNum=5):
        sql_peopleTop="select userID_id qq,count(1) as cnt,(select nick from fetchQzone_nick where guest_id=userID_id limit 1) AS nick from (select distinct come_id,userID_id from fetchQzone_comment JOIN  fetchQzone_feed ON parent_id=feedID )iner group by userID_id order by cnt desc limit %s;"%peopleNum
        cursor = connection.cursor()
        cursor.execute(sql_peopleTop)
        return cursor.fetchall()

