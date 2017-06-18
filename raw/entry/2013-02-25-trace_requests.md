---
layout: post
title: Trace Requests in EBS
category : Oracle
tags : [Oracle, DBA, EBS]
---

## Trace File

命名规则：`[oracle_sid]_ora_[server_process_id]_[trace_id].trc` 

* a) oracle_sid：可简单理解为数据库实例id，通过v$instance的instance_name来确定；    
* b) server_process_id：oracle内部标示进程的id，通过v$session的spid来确定；
* c) trace_id：可由`tracefile_identifier`参数指定，通过v$process的traceid来确定，默认为空。

存放路径：由参数 `user_dump_dest`指定，可以通过`show user_dump_dest；`或 
`SELECT NAME, VALUE FROM V$PARAMETER WHERE NAME = 'user_dump_dest';` 来确定。

大小设定：由参数 `max_dump_file_size`指定，以OS block为单位，跟踪时不确定文件大小，可以增加文件大小，或设为 unlimited。

## 跟踪请求会话

**根据request_id查找并发请求信息：**

	SELECT D.VALUE || '/' || LOWER(RTRIM(I.INSTANCE, CHR(0))) || '_ora_' || FCR.ORACLE_PROCESS_ID || '.trc' TRACE_FILE,
	       REQUEST_ID,                                                                                                  
	       OS_PROCESS_ID,                                                                                               
	       ORACLE_PROCESS_ID,                                                                                           
	       ORACLE_SESSION_ID,                                                                                           
	       ACTUAL_START_DATE,                                                                                           
	       ACTUAL_COMPLETION_DATE
	  FROM FND_CONCURRENT_REQUESTS FCR,
	       (SELECT T.INSTANCE
	          FROM V$THREAD T, V$PARAMETER V
	         WHERE V.NAME = 'thread'
	           AND (V.VALUE = 0 OR T.THREAD# = TO_NUMBER(V.VALUE))) I,
	       (SELECT VALUE FROM V$PARAMETER WHERE NAME = 'user_dump_dest') D
	 WHERE FCR.REQUEST_ID = 19584084;
 
**根据SPID查询并发进程的当前会话信息：**

	SELECT S.SID,
	       S.SERIAL#,
	       'exec DBMS_SYSTEM.SET_SQL_TRACE_IN_SESSION(' || S.SID || ',' || S.SERIAL# || ',' || 'TRUE' || ');' START_SQL_TRACE,
	       'exec DBMS_SYSTEM.SET_SQL_TRACE_IN_SESSION(' || S.SID || ',' || S.SERIAL# || ',' || 'FALSE' || ');' END_SQL_TRACE,
	       S.STATUS,
	       S.MODULE,                           
	       S.ACTION,                             
	       S.CLIENT_INFO,
	       S.SQL_HASH_VALUE,
	       P.PGA_USED_MEM,
	       P.PGA_MAX_MEM
	  FROM V$SESSION S, V$PROCESS P
	 WHERE S.PADDR = P.ADDR
	   AND S.PROCESS = '2031636'
	   AND P.SPID = 3199034;
 
**跟踪会话，以 ‘225,27128’ 为例：**

开始跟踪，执行 START_SQL_TRACE即可：

	SQL> exec DBMS_SYSTEM.SET_SQL_TRACE_IN_SESSION(225,27128,TRUE);
	 
	PL/SQL procedure successfully completed.
 
结束跟踪，执行 END_SQL_TRACE即可(注意，对于长会话，记得手动结束跟踪，否则会浪费服务器资源)：

	SQL> exec DBMS_SYSTEM.SET_SQL_TRACE_IN_SESSION(225,27128,FALSE);
	 
	PL/SQL procedure successfully completed.

查看跟踪文件：

	$ ll /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_3199034.trc
	-rw-r--r--   1 prodora  dba          745495 Feb 25 15:20 /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_3199034.trc
 
## 使用tkprof格式化跟踪文件

因sql trace产生的跟踪文件阅读不太友好，Oracle提供了tkprof工具，可以对此格式化，便于阅读。

**用法：**

	$ tkprof 
	Usage: tkprof tracefile outputfile [explain= ] [table= ]
	              [print= ] [insert= ] [sys= ] [sort= ]
	  table=schema.tablename   Use 'schema.tablename' with 'explain=' option.
	  explain=user/password    Connect to ORACLE and issue EXPLAIN PLAN.
	  print=integer    List only the first 'integer' SQL statements.
	  aggregate=yes|no
	  insert=filename  List SQL statements and data inside INSERT statements.
	  sys=no           TKPROF does not list SQL statements run as user SYS.
	  record=filename  Record non-recursive statements found in the trace file.
	  waits=yes|no     Record summary for any wait events found in the trace file.
	  sort=option      Set of zero or more of the following sort options:
	    prscnt  number of times parse was called
	    ... ...

**使用示例：**

	$ tkprof explain=apps/password
	trace = prod_ora_3199034.trc
	output = prod_ora_3199034.out                           
	 
	TKPROF: Release 9.2.0.6.0 - Production on Mon Feb 25 15:58:26 2013
	 
	Copyright (c) 1982, 2002, Oracle Corporation.  All rights reserved.
 
 
	$ ll prod_ora_3199034*        
	-rw-r--r--   1 prodora  dba          150112 Feb 25 15:58 prod_ora_3199034.out
	-rw-r--r--   1 prodora  dba          745495 Feb 25 15:20 prod_ora_3199034.trc

**查看输出：**

	********************************************************************************
	
	SELECT SOURCE_TYPE 
	FROM
	 MTL_SYSTEM_ITEMS_B WHERE ORGANIZATION_ID = :B2 AND INVENTORY_ITEM_ID = :B1 

	call     count       cpu    elapsed       disk      query    current        rows
	------- ------  -------- ---------- ---------- ---------- ----------  ----------
	Parse        0      0.00       0.00          0          0          0           0
	Execute    156      0.00       0.00          0          0          0           0
	Fetch      156      0.00       0.00          0        780          0         156
	------- ------  -------- ---------- ---------- ---------- ----------  ----------
	total      312      0.00       0.00          0        780          0         156
	
	Misses in library cache during parse: 0
	Optimizer goal: CHOOSE
	Parsing user id: 44  (APPS)   (recursive depth: 1)
	
	Rows     Execution Plan
	-------  ---------------------------------------------------
	      0  SELECT STATEMENT   GOAL: CHOOSE
	      0   TABLE ACCESS   GOAL: ANALYZED (BY INDEX ROWID) OF 
	              'MTL_SYSTEM_ITEMS_B'
	      0    INDEX   GOAL: ANALYZED (UNIQUE SCAN) OF 
	               'MTL_SYSTEM_ITEMS_B_U1' (UNIQUE)
	
	********************************************************************************

## 延伸阅读

* [Oracle EBS SQL Trace日志收集的方法](http://blog.csdn.net/pan_tian/article/details/7677120)
* [How to Generate SQL Trace in OAF](http://blog.csdn.net/pan_tian/article/details/8555503)
* [Oracle SQL Trace和10046事件](http://blog.csdn.net/tianlesoftware/article/details/5857023)
* [使用TKProf分析Oracle跟踪文件](http://blog.csdn.net/tianlesoftware/article/details/5632003)
