from fetchQzone.models import people,comment,feed,nick
from django.db import connection
import types
import MySQLdb
class queryTool(object):
    """docstring for queryTool"""
    def __init__(self):    
        cursor = connection.cursor()
        sql_tmpfeed="create table tmp_feed select info,time,userID_id,feedID,nick from fetchQzone_feed,fetchQzone_nick limit 5;delete from tmp_feed;"
        sql_tmpcomment="create table tmp_comment select parent_id,come_id,to_id,info,fetchQzone_comment.time,rootID from fetchQzone_comment limit 5;delete from tmp_comment;"

        for x in (sql_tmpfeed,sql_tmpcomment):
            try:
                cursor.execute(x)
            except :
                pass
    #cursor = connection.cursor()
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
    def insertToTable(self,table,rows):
        if not rows:
            return 
        cursor = connection.cursor()
        def addyinhao(obj):
            
            if type(obj)==types.LongType or type(obj)==types.IntType:
                return str(obj)
            else:
                return "\'"+MySQLdb.escape_string(str(obj))+"\'"
        values=[]
        for x in rows:
            one="("+",".join(map(addyinhao,x))+")"
            values.append(one)
        
        sql_insert="insert into "+table+" VALUES "+",".join(values)+";"
        cursor.execute("delete from "+table)
        cursor.execute(sql_insert)
        cursor.close()

    def getResult(self,user,start,num,friend=None):
        Result={}
        cursor = connection.cursor()
        if friend==None:
            sql_feed=" CREATE TEMPORARY TABLE  tmp_feed select info,UNIX_TIMESTAMP(time),userID_id,feedID,(select nick from fetchQzone_nick where  guest_id=userID_id limit 1) as nick from fetchQzone_feed where userID_id=%s  order by time  desc limit %s,%s "%(user,start,num)
            sql_comment=" CREATE TEMPORARY TABLE tmp_comment select parent_id,come_id,to_id,fetchQzone_comment.info,fetchQzone_comment.time,rootID from tmp_feed,fetchQzone_comment where parent_id=feedID  order by IDinFeed "
            
            sql_FeedtoRe="select * from tmp_feed;"
            sql_CommenttoRe="select parent_id,come_id,to_id,info,UNIX_TIMESTAMP(time),rootID,(select nick from fetchQzone_nick where  guest_id=come_id limit 1) as come_nick,(select nick from fetchQzone_nick where  guest_id=to_id limit 1) as to_nick from tmp_comment;"
            cursor.execute(sql_feed)
            #self.insertToTable("tmp_feed",cursor.fetchall())
            cursor.execute(sql_comment)
            #self.insertToTable("tmp_comment",cursor.fetchall())
            

            cursor.execute(sql_FeedtoRe)
            Result["feeds"]=cursor.fetchall()
            cursor.execute(sql_CommenttoRe)
            Result["comments"]=cursor.fetchall()
        else:

            sql_comment=" CREATE TEMPORARY TABLE tmp_comment select parent_id,come_id,to_id,info,time,rootID from fetchQzone_comment where (come_id=%s and to_id=%s) OR (come_id=%s and to_id=%s ) order by parent_id,IDinFeed "%(user,friend,friend,user)
            sql_feed=" CREATE TEMPORARY TABLE tmp_feed  SELECT fe.info,UNIX_TIMESTAMP(fe.`time`),userID_id,feedID, ni.`nick` come_nick FROM  fetchQzone_feed fe JOIN tmp_comment    ON  parent_id=feedID JOIN fetchQzone_nick ni ON guest_id=userID_id group by feedID ORDER BY userid_id, fe.`time` DESC LIMIT %s,%s ;"%(start,num)
            sql_CommenttoRe="select parent_id,come_id,to_id,tmp_comment.info,tmp_comment.time,rootID,(select nick from fetchQzone_nick where guest_id=come_id limit 1) as come_nick,(select nick from fetchQzone_nick where  guest_id=to_id  limit 1) as to_nick from tmp_comment,tmp_feed where parent_id=feedID order by feedID;"
            sql_FeedtoRe="select * from tmp_feed"

            cursor.execute(sql_comment)
            #self.insertToTable("tmp_comment",cursor.fetchall())            
            cursor.execute(sql_feed)
           # self.insertToTable("tmp_feed",cursor.fetchall())

            cursor.execute(sql_CommenttoRe)
            Result["comments"]=cursor.fetchall()        
            cursor.execute(sql_FeedtoRe)
            Result["feeds"]=cursor.fetchall()
        sql_FriendtoRe="CALL getIntimacy(%s,30)"%user
        cursor.execute(sql_FriendtoRe)
        Result["friend"]=cursor.fetchall()
     #   cursor.execute("drop table  tmp_feed")
      #  cursor.execute("drop table tmp_comment")
        #cursor.close()
        return Result
    def getFeedDetail(self,feedID):
        Result={}
        sql_FeedtoRe="select DISTINCT fetchQzone_feed.info,UNIX_TIMESTAMP(fetchQzone_feed.time),fetchQzone_feed.userID_id ,fetchQzone_feed.feedID,nick from fetchQzone_feed join fetchQzone_nick ni on ni.guest_id=userID_id  where fetchQzone_feed.feedID='%s' group by guest_id "% feedID
       # sql_comment="select distinct parent_id,come_id,to_id,info,fetchQzone_comment.time,rootID from fetchQzone_comment where parent_id='%s' order by IDinFeed "% feedID
        sql_CommenttoRe="select  parent_id,come_id,to_id,info,time,rootID,(select nick from fetchQzone_nick where guest_id=come_id limit 1) AS come_nick,(select nick from fetchQzone_nick where guest_id=to_id limit 1) AS to_nick from fetchQzone_comment where parent_id='%s' order by IDinFeed"% feedID

        cursor = connection.cursor()
        cursor.execute(sql_CommenttoRe)
        Result["comments"]=cursor.fetchall()        
        cursor.execute(sql_FeedtoRe)
        Result["feeds"]=cursor.fetchall()
        cursor.close()
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
    def getComfri(self,user1,user2):
        sql="CALL comFri(%s,%s);"%(user1,user2);
        cursor = connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    def getSecrela(self,user):
        sql="CALL secmai(%s)"%user
        cursor=connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    def getTimeAnaly(self,user):
        sql="call timeanaly(%s)"%(user)
        print(sql)
        cursor=connection.cursor()
        cursor.execute(sql)
        al=cursor.fetchall()
        cursor.close()
        ret=[0]*24
        ret1=[0]*12
        for x in al:
            ret[int(x[0])]=int(x[1])

        return ret
    def getIntimacy(self,user,number=20):
        sql="CALL getIntimacy(%s,%s)"%(user,number)
        cursor=connection.cursor()
        cursor.execute(sql)
        return cursor.fetchall()





