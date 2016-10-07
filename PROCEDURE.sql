亲密度分析 存储过程:
CREATE DEFINER=`root`@`localhost` PROCEDURE `getIntimacy`(userid BIGINT(20),number INT(5))
BEGIN 
CREATE TEMPORARY TABLE IF NOT EXISTS intimacy (qq BIGINT(20),cnt INT(5));
DELETE FROM intimacy;
INSERT INTO intimacy SELECT al.qq,COUNT(1) cnt FROM ((SELECT come_id qq FROM fetchQzone_comment WHERE to_id=userid)
 UNION ALL (SELECT to_id  qq FROM fetchQzone_comment WHERE come_id=userid))al  GROUP BY qq ORDER BY cnt DESC LIMIT number;
SELECT qq,cnt,fetchqzone_nick.nick FROM intimacy JOIN fetchqzone_nick ON qq=guest_id GROUP BY qq ORDER BY cnt DESC;
    END$$
DELIMITER ;
二度人脉分析 存储过程：
CREATE DEFINER=`root`@`localhost` PROCEDURE `SecMai`(userid VARCHAR(20))
BEGIN
   CREATE  TABLE IF NOT EXISTS mate(qq BIGINT(20) );
    DELETE FROM mate;
INSERT INTO mate SELECT DISTINCT qq  FROM (SELECT come_id qq FROM  fetchqzone_comment WHERE `to_id`=userid AND come_id!=to_id  UNION SELECT  `to_id` qq FROM fetchqzone_comment WHERE `come_id`=userid AND come_id!=to_id ) AS fr ;
CREATE TEMPORARY TABLE IF NOT EXISTS Secmate (qq BIGINT(20) );
DELETE FROM Secmate;
INSERT INTO Secmate SELECT DISTINCT come_id qq FROM  fetchqzone_comment WHERE `to_id` IN (SELECT qq FROM mate);  
INSERT INTO Secmate SELECT DISTINCT `to_id` qq FROM fetchqzone_comment WHERE `come_id` IN (SELECT qq FROM mate);
CREATE TEMPORARY TABLE IF NOT EXISTS Secmai(qq BIGINT(20) );
DELETE FROM Secmai;
SELECT DISTINCT qq ,ni.nick FROM Secmate  JOIN fetchqzone_nick ni ON qq=ni.guest_id WHERE  qq NOT IN (SELECT qq FROM mate) GROUP BY  qq ;
    END$$
DELIMITER ;
两人交互分析 存储过程:
sql_comment=" CREATE TEMPORARY TABLE tmp_comment select parent_id,come_id,to_id,info,time,rootID from fetchQzone_comment where (come_id=%s and to_id=%s) OR (come_id=%s and to_id=%s ) order by parent_id,IDinFeed "%(user,friend,friend,user)
 sql_feed=" CREATE TEMPORARY TABLE tmp_feed  SELECT fe.info,UNIX_TIMESTAMP(fe.`time`),userID_id,feedID, ni.`nick` come_nick FROM  fetchQzone_feed fe JOIN tmp_comment    ON  parent_id=feedID JOIN fetchQzone_nick ni ON guest_id=userID_id group by feedID ORDER BY userid_id, fe.`time` DESC LIMIT %s,%s ;"%(start,num)
sql_CommenttoRe="select   parent_id,come_id,to_id,tmp_comment.info,tmp_comment.time,rootID,(select nick from fetchQzone_nick where guest_id=come_id limit 1) as come_nick,(select nick from fetchQzone_nick where  guest_id=to_id  limit 1) as to_nick from tmp_comment,tmp_feed where parent_id=feedID order by feedID;"
sql_FeedtoRe="select * from tmp_feed"

活动时间分析存储过程：


CREATE DEFINER=`root`@`localhost` PROCEDURE `timeanaly`(userid BIGINT(20))
BEGIN
	SELECT ti,SUM(cnt) cnt FROM (SELECT DATE_FORMAT(TIME, ' %H ')  ti,COUNT(*) cnt FROM fetchqzone_feed  WHERE userID_id=userid AND TIME IS NOT NULL GROUP BY DATE_FORMAT(TIME, ' %H ')
	UNION SELECT DATE_FORMAT(comm.TIME, ' %H ')  ti,COUNT(*) cnt FROM fetchqzone_comment  comm WHERE come_id=userid AND comm.TIME IS NOT NULL GROUP BY DATE_FORMAT(comm.TIME, ' %H '))al GROUP BY ti;
    END$$
DELIMITER ;
共同好友分析存储过程：
CREATE DEFINER=`root`@`localhost` PROCEDURE `comFri`(user1 BIGINT(20),user2 BIGINT(20))
BEGIN
CREATE  TABLE IF NOT EXISTS mate(qq BIGINT(20) );
DELETE FROM mate;
INSERT INTO mate SELECT DISTINCT qq  FROM (SELECT come_id qq FROM  fetchqzone_comment WHERE `to_id`=user1 AND come_id!=to_id  UNION SELECT  `to_id` qq FROM fetchqzone_comment WHERE `come_id`=user1 AND come_id!=to_id ) AS fr ;
CREATE TEMPORARY TABLE IF NOT EXISTS Secmate (qq BIGINT(20) );
DELETE FROM Secmate;
INSERT INTO Secmate SELECT DISTINCT to_id qq FROM  fetchqzone_comment WHERE come_id=user2 AND `to_id` IN (SELECT qq FROM mate) ;  
INSERT INTO Secmate SELECT DISTINCT come_id qq FROM fetchqzone_comment WHERE to_id=user2 AND `come_id` IN (SELECT qq FROM mate);
SELECT DISTINCT qq,nick FROM Secmate JOIN fetchqzone_nick ON guest_id=qq WHERE qq!=user1 AND qq!=user2 GROUP BY guest_id ;
    END$$
DELIMITER ;
