from django.db import connection
import time
cursor = connection.cursor()
def todosth():
    sql_getall="select * from fetchqzone_comment_copy;"
    sql_update="UPDATE `test`.`fetchqzone_comment` SET `time` = %s WHERE `id` = '%s';"
    cursor.execute(sql_getall)
    all=cursor.fetchall()
    for x in all:
        id=x[0];
        time=x[1]
    #    print(feedid,time,visittime)
        sql_toupdate=sql_update%(gettime(time),id)
     #   print(sql_toupdate)
        cursor.execute(sql_toupdate)




def gettime(x):
    if x==(-8888):
        return "NULL"
   # print(x)
    ti=x/1000
    m = time.localtime(ti)
   # print time.strftime('%Y-%m-%d %H:%M:%S',m)
    return "'"+time.strftime('%Y-%m-%d %H:%M:%S',m)+"'"


todosth()