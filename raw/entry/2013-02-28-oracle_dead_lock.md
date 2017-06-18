---
layout: post
title: DeadLock in Oracle Database
category : Oracle
tags : [Oracle, Database, DBA]
---

## 死锁

在事务运行高峰期，由于DDL、DML使用锁资源十分频繁，争用时甚至会发生死锁，阻塞的锁可能导致系统延迟，甚至长时间不响应，影响业务系统的正常运行。若死锁频频发生，则有可能是应用设计不当。这里暂且初步整理下锁争用的有关资料。

### 1.锁介绍

#### 概述

锁：并发访问、更新时容易出现

概念：当数据库对象正在被其他进程或用户修改时，可以保护它不被修改 		

结构：“排队”的队列，先到先服务，串行工作

功能：

* 坚持一致性和完整性
* 队列结构管理请求的会话
* 自动处理锁机制
* 锁的持续时间等于被提交事务的长度或处理时间

#### 类型

DDL

* 在修改过程中保护模式对象
* DDL锁，由Oracle自动发布和释放

DML

* 在事务处理过程中保护对象
* 当发布rollback或commit时，认为完成了事务

内部锁

* 由Oracle管理，以保护内部数据库结构，如数据文件

#### 模式

锁模式描述 ...
 
锁模式和DML语句 ...

锁模式和DDL语句 ...

#### 级别

##### 数据库级别

锁定数据库以禁止任何新会话和新事务，可以分为以下三种类型。

	ALTER SYSTEM ENABLE RESTRICTED SESSION
	
	* 使数据库进入限制模式
	* 仅有RESTRICTED SESSION权限用户才能登陆
	* 已经登陆的会话不受此印象
	* 登陆的用户可以正常进行DDL/DML操作
	
	ALTER SYSTEM QUIESCE RESTRICTED
	
	* 使数据库进入静默的限制模式
	* 从用户的活动中锁定数据库，锁定所有操作（处于等待状态），直到UNQUICESCE
	* 不允许非特权用户登陆
	* 特权用户可以正常进行操作
	
	ALTER DATABASE OPEN READ ONLY
	
	* 使数据库以只读模式打开
	* UNDO段处于脱机状态
	* 不允许任何更新、事务操作

##### 表级别

* 通过DML或者LOCK语句发出

##### 行级别

* DML更新一行或多行时
* Oracle支持的最低级别
* SELECT ... FOR UPDATE只锁定返回的行

##### 列级别

* Oracle不支持

#### 锁语句

LOCK语法

	 LOCK TABLE
	   [ schema.]{table | view} [@dblink]
	   [, [schema.]{table | view} [@dblink] ] ...
	 IN lockmode MODE
	   [ NOWAIT]

示例

	* SHARE(S)
	* ROW SHARE(RS)
	* ROW EXCLUSIVE(RX)
	* SHARE ROW EXCLUSIVE(SRX)
	* EXCLUSIVE(X)
	* SELECT ... FOR UPDATE

### 2.死锁日志

#### 警告日志

	Wed Feb 27 09:34:58 2013
	ORA-000060: Deadlock detected. More info in file /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_4513878.trc.

#### 跟踪日志

	... ...
	*** 2013-02-11 03:01:37.846
	*** SESSION ID:(25.18) 2013-02-11 03:01:37.846
	Undo Segment 11 Onlined 
	*** 2013-02-11 08:41:27.866 
	Undo Segment 19 Onlined 
	*** 2013-02-16 08:46:16.482
	Undo Segment 134 Onlined
	*** 2013-02-16 09:55:31.314
	Undo Segment 195 Onlined
	*** 2013-02-27 09:34:58.033
	DEADLOCK DETECTED
	Current SQL statement for this session:
	UPDATE FND_CONCURRENT_REQUESTS SET PP_END_DATE = SYSDATE, POST_REQUEST_STATUS = 'E' WHERE REQUEST_ID = :B1 
	----- PL/SQL Call Stack -----
	  object      			line  		object
	  handle    			number  	name
	700000095f756d0        		67  	package body APPS.FND_CP_OPP_CMD
	70000008caf2ea0         	1  		anonymous block
	The following deadlock is not an ORACLE error. It is a
	deadlock due to user error in the design of an application
	or from issuing incorrect ad-hoc SQL. The following
	information may aid in determining the deadlock:
	Deadlock graph:
	                       ---------Blocker(s)--------  ---------Waiter(s)---------
	Resource Name          process session holds waits  process session holds waits
	TX-0159001e-000075b3        24      25     X             24      25           X
	session 25: DID 0001-0018-00000006	session 25: DID 0001-0018-00000006
	Rows waited on:
	Session 25: obj - rowid = 00009050 - AAAJBQAAmAAAKPzAAG
	  (dictionary objn - 36944, file - 38, block - 41971, slot - 6)
	Information on the OTHER waiting sessions:
	End of information on OTHER waiting sessions.
	... ...

### 3.死锁情形模拟

若在请求锁资源时出现循环等待，则产生死锁现象。如下，以列出顺序先后执行更新操作。

1.获取并保持锁，如LOCK1，且为排他锁，锁定更新行1：
	
	SQL(49,180)>update dt_char set name = '1A' where id = 1;
	
	1 row updated.

2.获取并保持锁，如LOCK2，且为排他锁，锁定更新行2：	

	SQL(462,13)> update dt_char set name = '2B' where id = 2;
	
	1 row updated.

3.请求更新行2，因处于等待，等待锁LOCK2

	SQL(49,180)>update dt_char set name = '2A' where id = 2;
	
4.请求更新行1，因处于等待，等待锁LOCK1
	
	SQL(462,13)> update dt_char set name = '1B' where id = 1;

此时，会话(49,180)和(462,13)在锁资源LOCK1和LOCK2上存在循环等待的情形，故出现死锁,3中的语句终止；此时4中的语句处于等待状态。

	SQL(49,180)>update dt_char set name = '2A' where id = 2;
	update dt_char set name = '2A' where id = 2
	*
	ERROR at line 1:
	ORA-00060: deadlock detected while waiting for resource

出现死锁时，系统会


### 4.死锁解决方案

**ORA-00060 deadlock detected while waiting for resource**

**Cause**:  Your session and another session are waiting for a resource locked by the other. This condition is known as a deadlock. To resolve the deadlock, one or more statements were rolled back for the other session to continue work.

**Action**:  Either:

*  Enter a ROLLBACK statement and re-execute all statements since the last commit or
* Wait until the lock is released, possibly a few minutes, and then re-execute the rolled back statements.

除了执行ROLLBACK，或者等待锁资源释放，并重新执行所需要的语句外；还有一种方案就是清理掉死锁中阻塞的一方的数据库会话。

	--生成kill session脚本，杀掉死锁中阻塞一方的会话
	--ALTER SYSTEM KILL SESSION 'sid,serial#';
	SELECT 'alter system kill session ''' || SID || ',' || SERIAL# || ''';' "Deadlock"
	  FROM V$SESSION
	 WHERE SID IN (SELECT SID FROM V$LOCK WHERE BLOCK = 1);
	
- - -

## DDL Lock

DDL语句在发布时为获取数据对象的内部结构而需要排他锁，如果锁不可用则会更新失败。

### 1.直接发布ALTER TABLE语句

建立`SQL*Plus`会话(27，0），发出ALTER TABLE语句：

	SQL> SELECT * FROM V$MYSTAT WHERE ROWNUM = 1;

	       SID STATISTIC#	   VALUE
	---------- ---------- ----------
		27	    0	       0

	SQL> desc dt_char;
	 Name					   Null?    Type
	 ----------------------------------------- -------- ----------------------------
	 NAME						    CHAR(10)
	
	SQL> alter table dt_char modify (name varchar(20));
	
	Table altered.
	
	SQL> desc dt_char;
	 Name					   Null?    Type
	 ----------------------------------------- -------- ----------------------------
	 NAME						    VARCHAR2(20)

### 2.有DML更新表数据时发布DDL语句

#### 默认

新开一个`SQL*Plus`会话(513,22540)，发出UPDATE语句：

	SQL> SELECT * FROM V$MYSTAT WHERE ROWNUM = 1;

	       SID STATISTIC#	   VALUE
	---------- ---------- ----------
		513	    22540	       0

	SQL> update dt_char set name = 'DDL Lock';

	0 rows updated.

此时，在会话(27,0)中再次发布ALTER TABLE语句：

	SQL> alter table dt_char modify (name char(10));
	alter table dt_char modify (name char(10))
	            *
	ERROR at line 1:
	ORA-00054: resource busy and acquire with NOWAIT specified or timeout expired

此时，提示要求更新的表结构正处于繁忙状态(被其他会话占用)，因不愿意等待锁释放或者等待超时，故更新失败。

查看哪些对象处于争用之中：

	SQL> SELECT lo.session_id,
       s.serial#,
       lo.oracle_username,
       o.owner,
       o.object_name,
       o.object_type,
       decode(lo.locked_mode,
              0,
              'None', /* Mon Lock equivalent */
              1,
              'Null', /* N */
              2,
              'Row-S (SS)', /* L */
              3,
              'Row-X (SX)', /* R */
              4,
              'Share', /* S */
              5,
              'S/Row-X (SSX)', /* C */
              6,
              'Exclusive', /* X */
              lo.locked_mode) locked_mode
  	FROM v$locked_object lo,
	       dba_objects     o,
	       v$session       s
	 WHERE lo.object_id = o.object_id
	   AND s.sid = lo.session_id;
	
   	SESSION_ID 	  SERIAL# ORACLE_USERNAME		OWNER  OBJECT_NAME  OBJECT_TYPE	LOCKED_MODE
	---------- ---------- ---------------- ---------- ------------ ------------ -----------
		513			22540 DEV			   DEV		  DT_CHAR	   TABLE		Row-X (SX)

从以上查询可以看出，表DEV.DT_CHAR正在被会话(513.22540)占用，锁模式为Row-X，即排他锁，为了更新，在某个事务中锁定了行，则不允许其他事务锁定这个表。

在这个例子中，发布的DML后，已经获取了锁，并锁定了表DEV.DT_CHAR，因没有发布ROLLBACK、COMMIT，该会话一直持有锁资源。

#### 指定TIMEOUT

在会话(27，0）中，发布超时为30s:

	SQL@（27，0）> alter session set ddl_lock_timeout=30;		--DDL_LOCK_TIMEOUT参数值默认为0
	
	Session altered.
	
	SQL@（27，0）> alter table dt_char modify (name char(10));	--处于等待状态，超时30s

此时，若在发布DDL时起30s内，会话(513,22540)释放锁资源，则DDL可以更新成功：

	SQL@(513,22540)> commit;

	Commit complete.

	SQL@（27，0）> alter table dt_char modify (name char(10));	--处于等待状态，超时30s
	
	Table altered.

否则，DDL失败：

	SQL@（27，0）> alter table dt_char modify (name char(10));	--处于等待状态，超时30s
	alter table dt_char modify (name char(10))
	            *
	ERROR at line 1:
	ORA-00054: resource busy and acquire with NOWAIT specified or timeout expired

- - -

## DML Lock

### 1.事务和保存点

原始数据：

	SQL> select * from dt_char;
	
	NAME
	----------
	1
	2
	3
	4
	5
	
更新行：

	SQL> update dt_char set name = '1A' where name = '1';
	
	1 row updated.

	SQL> select * from dt_char;
	
	NAME
	----------
	1A
	2
	3
	4
	5

创建保存点，用来控制事务	

	SQL> savepoint A;
	
	Savepoint created.
	
更新行：

	SQL> update dt_char set name = '2A' where name = '2';
	
	1 row updated.
	
	SQL> select * from dt_char;
	
	NAME
	----------
	1A
	2A
	3
	4
	5

回滚到保存点A，此时在A之前的锁没有释放，在A之后的锁则被释放，更新将会回滚到保存A（若不指定保存点，则回滚到更新的初始状态）：	

	SQL> rollback to savepoint A;
	
	Rollback complete.
	
	SQL> select * from dt_char;
	
	NAME
	----------
	1A
	2
	3
	4
	5

## 常用脚本

查询当前会话ID

	--查询当前会话ID
	SELECT * FROM V$MYSTAT WHERE ROWNUM = 1;

查询会话锁

	--查询会话锁
	SELECT * FROM DBA_LOCKS WHERE SESSION_ID IN (513);
	

检测锁争用

	--request:如果request值非0，则表示在等待一个锁
	--block:如果block为1，则表示此会话持有一个锁，并阻塞别人获得此锁
	SELECT *
	  FROM V$LOCK
	 WHERE BLOCK = 1
	    OR REQUEST > 0;
	
被锁定的对象

	--被锁定的对象
	SELECT * FROM V$LOCKED_OBJECT;
	
仅列出用户所保持的锁

	--仅列出用户所保持的锁
	SELECT S.USERNAME,
	       L.SESSION_ID,
	       L.LOCK_TYPE,
	       L.MODE_HELD,
	       L.MODE_REQUESTED,
	       L.LOCK_ID1,
	       L.LOCK_ID2,
	       L.LAST_CONVERT,
	       L.BLOCKING_OTHERS
	  FROM V$SESSION S, DBA_LOCKS L
	 WHERE S.USERNAME IS NOT NULL
	   AND (S.SID = L.SESSION_ID AND L.MODE_REQUESTED != 'NONE')
	    OR (S.SID = L.SESSION_ID AND L.MODE_REQUESTED = 'NONE' AND
	       L.MODE_HELD != 'Share' AND
	       (LOCK_ID1, LOCK_ID2) IN
	       (SELECT A.LOCK_ID1, A.LOCK_ID2
	           FROM DBA_LOCKS A
	          WHERE A.MODE_REQUESTED != 'NONE'
	            AND A.LOCK_ID1 = L.LOCK_ID1
	            AND A.LOCK_ID2 = L.LOCK_ID2))
	 ORDER BY 6, 7, 5;
	
哪些对象处于争用中

	--v$locked_object
	--哪些对象处于争用中
	SELECT LO.SESSION_ID,
	       S.SERIAL#,
	       LO.ORACLE_USERNAME,
	       S.PROCESS,
	       S.PROGRAM,
	       O.OWNER,
	       O.OBJECT_NAME,
	       O.OBJECT_TYPE,
	       DECODE(LO.LOCKED_MODE,
	              0,
	              'None', /* Mon Lock equivalent */
	              1,
	              'Null', /* N */
	              2,
	              'Row-S (SS)', /* L */
	              3,
	              'Row-X (SX)', /* R */
	              4,
	              'Share', /* S */
	              5,
	              'S/Row-X (SSX)', /* C */
	              6,
	              'Exclusive', /* X */
	              LO.LOCKED_MODE) LOCKED_MODE
	  FROM V$LOCKED_OBJECT LO, DBA_OBJECTS O, V$SESSION S
	 WHERE LO.OBJECT_ID = O.OBJECT_ID
	   AND S.SID = LO.SESSION_ID
	   AND S.SID IN (336, 1360);
	
死锁检测

	--dba_blockers
	--阻塞其他用户的会话的id
	SELECT * FROM DBA_BLOCKERS;
	
	--dba_waiters
	--显示等待将被阻塞会话释放锁的会话id
	SELECT * FROM DBA_WAITERS;

	--使用dba_waiters视图
	信息格式：Blocker|Waiter(sid,serial#,username,sql)
	SELECT 'Blocker(' || BW.HOLDING_SESSION || ':' || SB.USERNAME ||
	       ') - SQL: ' || BQ.SQL_TEXT BLOCKERS,
	       'Waiter(' || BW.WAITING_SESSION || ':' || SW.USERNAME || ') - SQL: ' ||
	       WQ.SQL_TEXT BLOCKERS
	  FROM DBA_WAITERS BW,
	       V$SESSION   SB,
	       V$SESSION   SW,
	       V$SQLAREA   BQ,
	       V$SQLAREA   WQ
	 WHERE BW.HOLDING_SESSION = SB.SID
	   AND BW.WAITING_SESSION = SW.SID
	   AND SB.PREV_SQL_ADDR = BQ.ADDRESS
	   AND SW.SQL_ADDRESS = WQ.ADDRESS
	   AND BW.MODE_HELD <> 'None';

	--使用dba_locks视图
	--信息格式：Blocker|Waiter(sid,serial#,username,sql)
	SELECT DISTINCT 'Blocker(' || LB.SESSION_ID || ',' || SB.SERIAL# || ':' ||
	                SB.USERNAME || ') - SQL: ' || BQ.SQL_TEXT BLOCKERS,
	                'Waiter(' || LW.SESSION_ID || ',' || SW.SERIAL# ||
	                SW.USERNAME || ') - SQL: ' || WQ.SQL_TEXT BLOCKERS
	  FROM DBA_LOCKS LB,
	       V$SESSION SB,
	       DBA_LOCKS LW,
	       V$SESSION SW,
	       V$SQL     BQ,
	       V$SQL     WQ
	 WHERE LB.SESSION_ID = SB.SID
	   AND LW.SESSION_ID = SW.SID
	   AND SB.PREV_SQL_ADDR = BQ.ADDRESS
	   AND SW.SQL_ADDRESS = WQ.ADDRESS
	   AND LB.LOCK_ID1 = LW.LOCK_ID1
	   AND SW.LOCKWAIT IS NOT NULL
	   AND SB.LOCKWAIT IS NULL
	   AND LB.BLOCKING_OTHERS = 'Blocking';


生成kill session脚本

	--生成kill session脚本，杀掉死锁中阻塞一方的会话
	--ALTER SYSTEM KILL SESSION 'sid,serial#';
	SELECT 'alter system kill session ''' || SID || ',' || SERIAL# || ''';' "Deadlock"
	  FROM V$SESSION
	 WHERE SID IN (SELECT SID FROM V$LOCK WHERE BLOCK = 1);


查看导致死锁的SQL	

	--导致死锁的SQL 
	SELECT S.SID, Q.SQL_TEXT
	  FROM V$SQLTEXT Q, V$SESSION S
	 WHERE Q.ADDRESS = S.SQL_ADDRESS
	   AND S.SID = &SID
	 ORDER BY PIECE;

## 延伸阅读

* [锁 死锁 阻塞 Latch 等待](http://blog.csdn.net/tianlesoftware/article/details/5822674)

## Reference

* Database Error Message
* Oracle 9i数据库性能优化与调
