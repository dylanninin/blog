---
layout: post
title: Privileges in PL/SQL
category : Oracle
tags : [Oracle, Database, DBA]
---

##监控临时段使用

最近一个Web应用后端的数据库经常出现ORA-01652异常，即扩展临时段失败；关键在于该临时段在不久前已经扩展过一次，所以这里不再继续扩展，而是计划监控临时段的使用情况，并从中发现不合理的语句。

	ORA-1652: unable to extend temp segment by 128 in tablespace APPS_TMP 

数据库版本

	DEV> select * from v$version;
		BANNER
	----------------------------------------------------------------------------
		Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production
		PL/SQL Release 11.2.0.1.0 - Production
		CORE	11.2.0.1.0	Production
		TNS for Linux: Version 11.2.0.1.0 - Production
		NLSRTL Version 11.2.0.1.0 - Production


##创建表结构

`TEMP_SEG_USAGE`用于存放临时段使用统计信息，包括使用的用户、SQL语句等。

	DEV> CREATE TABLE TEMP_SEG_USAGE(
	  2         DATE_TIME DATE,
	  3         USERNAME VARCHAR2(30),
	  4         SID VARCHAR2(6),
	  5         SERIAL# VARCHAR2(6),
	  6         OS_USER VARCHAR2(30),
	  7         SPACE_USED NUMBER,
	  8         SQL_TEXT VARCHAR2(1000)
	  9  );
 
	Table created
 
##创建存储过程

`TEMP_SEG_USAGE_P`存储过程处理`INSERT`操作，方便JOB调用。

	DEV> CREATE OR REPLACE PROCEDURE TEMP_SEG_USAGE_P IS
	  2  BEGIN
	  3      INSERT INTO TEMP_SEG_USAGE
	  4          SELECT SYSDATE,
	  5                 A.USERNAME,
	  6                 A.SID,
	  7                 A.SERIAL#,
	  8                 A.OSUSER,
	  9                 B.BLOCKS,
	 10                 C.SQL_TEXT
	 11            FROM V$SESSION A, V$TEMPSEG_USAGE B, V$SQLAREA C
	 12           WHERE B.TABLESPACE = 'TMP'
	 13             AND A.SADDR = B.SESSION_ADDR
	 14             AND C.ADDRESS = A.SQL_ADDRESS
	 15             AND C.HASH_VALUE = A.SQL_HASH_VALUE
	 16             AND B.BLOCKS * 8192 > 1024
	 17           ORDER BY B.TABLESPACE, B.BLOCKS;
	 18      COMMIT;
	 19  END TEMP_SEG_USAGE_P;
	 20  /
	 
	Warning: Procedure created with compilation errors
	 
查询错误信息

	DEV> SELECT UO.OBJECT_NAME NAME,
	  2         UO.OBJECT_TYPE TYPE,
	  3         UE.LINE        LINENO,
	  4         UE.TEXT        ERR
	  5    FROM USER_OBJECTS UO, USER_ERRORS UE
	  6   WHERE UO.STATUS != 'VALID'
	  7     AND UE.NAME = UO.OBJECT_NAME
	  8   ORDER BY UO.OBJECT_NAME, UO.OBJECT_TYPE, UE.LINE;
	 
	NAME                TYPE         LINENO   ERR
	------------------- ------------ -------- -------------------------------
	TEMP_SEG_USAGE_P    PROCEDURE           3 PL/SQL: SQL Statement ignored
	TEMP_SEG_USAGE_P    PROCEDURE          11 PL/SQL: ORA-00942: 表或视图不存在
	 
单独执行

	DEV>  SELECT SYSDATE,
	  2          A.USERNAME,
	  3          A.SID,
	  4          A.SERIAL#,
	  5          A.OSUSER,
	  6          B.BLOCKS,
	  7          C.SQL_TEXT
	  8    FROM V$SESSION A, V$TEMPSEG_USAGE B, V$SQLAREA C
	  9   WHERE B.TABLESPACE = 'TMP'
	 10     AND A.SADDR = B.SESSION_ADDR
	 11     AND C.ADDRESS = A.SQL_ADDRESS
	 12     AND C.HASH_VALUE = A.SQL_HASH_VALUE
	 13     AND B.BLOCKS * 8192 > 1024
	 14  ORDER BY B.TABLESPACE, B.BLOCKS;

	 no rows selected

从以上输出可以看出，以DEV身份单独单独执行存储过程中的关键SQL时没有问题，但编译存储过程时，却提示表或视图不存在。在这个存储过程中，访问到非该用户拥有的表或视图的只有`V$SESSION`，`V$TEMPSEG_USAGE`，`V$SQLAREA`，推测有可能是访问权限不足导致。
	 
单独授权

	SYS> grant select on v_$session  to dev;
	
	Grant succeeded.
	
	SYS> grant select on v_$sort_usage  to dev;
	
	Grant succeeded.
	
	SYS> grant select on v_$sqlarea  to dev;
	
	Grant succeeded.

重新编译

	DEV> alter procedure TEMP_SEG_USAGE_P compile;
	 
	Procedure altered

##提交JOB

	DEV> BEGIN
			DBMS_JOB.ISUBMIT(JOB=>8001,WHAT=> 'TEMP_SEG_USAGE_P;',NEXT_DATE => SYSDATE,INTERVAL  => 'sysdate + (5/1440)');
			COMMIT;
		END;
		/

	PL/SQL procedure successfully completed.

到这里，监控临时段使用情况的任务已经创建完成，监控一段时间时候，即可获取临时段使用的统计信息，进而发现异常的语句。


##遇到的几个问题

###1.权限异常

在存储过程TEMP_SEG_USAGE_P中，使用到了`V$SESSION`，`V$TEMPSEG_USAGE`,`V$SQLAREA`动态性能视图，但查询当前用户授予的直接角色时，已经有系统标准的DBA角色，有权限查询这些视图。但在存储过程编译时，却提示表或视图不存在。

	SQL> SELECT * FROM USER_ROLE_PRIVS;
	
	USERNAME	 GRANTED_ROLE	 ADMIN_OPTION DEFAULT_ROLE OS_GRANTED
	------------ --------------- ------------ ------------ ----------
	DEV			 CONNECT	     NO  		  NO  		   NO
	DEV			 DBA			 NO  		  YES          NO
	DEV			 RESOURCE 		 NO  		  YES          NO

查看文档才知道，授予role的对象权限，仅在用户会话中有效；在用户创建的存储过程，视图等对象中并不能继承这些角色权限，必须单独为此授权才行。

Note : The privileges assigned to a role can be associated with a user session only and cannot be inherited by any objects (views, stored procedures) that are owned by a user who is granted the role. You cannot use the privileges granted via a role while creating a stored PL/SQL object or a view. For this you have to be granted the object privileges directly. Furthermore the object privileges granted through roles cannot be used by the scheduler jobs. 

It is important to note that the privileges acquired via roles can be exercised when running a procedure with invoker's rights but cannot be used when running a procedure with definer's rights.


###2.同义词授权

在创建上监控程序的过程中，出现过授权访问v$session错误的情况，如下：

	SYS> grant select on v$session to dev;
	grant select on v$session to dev
	                *
	ERROR at line 1:
	ORA-02030: can only select from fixed tables/views

通过查询`dba_synonyms`视图，可以知道v$session是动态性能视图v_$session的同义词，它本身并不是表或者视图。

	SYS> select * from dba_synonyms where synonym_name = 'V$SESSION';

	OWNER	   SYNONYM_NAME 	     TABLE_OWNE TABLE_NAME		  DB_LINK
	---------- ------------------------- ---------- ------------------------- ----------
	PUBLIC	   V$SESSION		     SYS	V_$SESSION

故这里应针对V_$SESSION授权，如下：

	SYS> grant select on v_$session to dev;

	Grant succeeded.


注意

在授权访问V_$动态性能视图以及其他数据字典时，也可以直接授予所有权限：

	SYS> grant select any dictionary to username;

这样将给用户足够的权限去访问所有的数据字典。

###3.什么是Fixed Views

Throughout its operation, Oracle maintains a set of virtual tables that record current database activity. These tables are called dynamic performance tables.

Dynamic performance tables are not true tables, and they should not be accessed by 
most users. However, database administrators can query and create views on the 
tables and grant access to those views to other users. These views are sometimes called fixed views because they cannot be altered or removed by the database administrator. 

In most cases, the information available in fixed views persists across instance shutdowns. However, certain fixed view information is reset when the instance is shut down.

SYS owns the dynamic performance tables; their names all begin with V_$(or GV_$). Views are created on these tables, and then public synonyms are created for the views. The synonym names begin with V$(or GV$). For example, the `V$DATAFILE` view contains information about the database’s datafiles, and the `V$FIXED_TABLE` view contains information about all of the dynamic performance tables and views in the database. 

Standard dynamic performance views (V$ fixed views) store information on the local instance. In contrast, global dynamic performance views (GV$ fixed views) store information on all open instances. Each V$ fixed view has a corresponding GV$ fixed view.

动态性能视图

	SYS> select count(1) from v$fixed_table;
	
	  COUNT(1)
	----------
	      1968

###4.什么是Synonym

A synonym is an alias for any table, view, materialized view, sequence, procedure, function, package, type, Java class schema object, user-defined object type, or another synonym. Because a synonym is simply an alias, it requires no storage other than its definition in the data dictionary.

Synonyms allow underlying objects to be renamed or moved, where only the synonym needs to be redefined and applications based on the synonym continue to function without modification.

You can create both public and private synonyms. A public synonym is owned by the special user group named PUBLIC and is accessible to every user in a database. A private synonym is contained in the schema of a specific user and available only to the user and the user's grantees.

创建语法

	DEV> ? create synonym
	
	 CREATE SYNONYM
	 --------------
	
	 Use this command to create a synonym. A synonym is an alternative
	 name for a table, view, sequence, procedure, stored function,
	 package, snapshot, or another synonym.
	
	 CREATE [PUBLIC] SYNONYM [schema.]synonym
	   FOR [schema.]object [@dblink]


创建私有同义词


	DEV> desc role_t;
	 Name			 Null?	  Type
	 ----------------------- -------- ----------------
	 ID				  NUMBER

	DEV> create synonym synonym_role for role_t;
	
	Synonym created.
	
	DEV> select * from synonym_role;
	
	no rows selected

另外一个用户APP访问

	APP> select * from dev.synonym_role;
	select * from dev.synonym_role
	                  *
	ERROR at line 1:
	ORA-01031: insufficient privileges
	

	APP> select * from dev.role_t;
	select * from dev.role_t
	                  *
	ERROR at line 1:
	ORA-01031: insufficient privileges

给APP添加权限

	DEV> grant select on synonym_role to app;

	Grant succeeded.

APP再次访问

	APP> select * from dev.synonym_role;

	no rows selected
	
	APP> select * from dev.role_t;
	
	no rows selected

这里感觉比较奇怪的是同样是同义词，授权却不一样，`grant select on v$session to username；`提示select操作的对象不对（即select仅能在表或视图上操作），这样就只能通过`grant select on v_$session to username；`授权；而`grant select on synonym_role to username;`却可以正常授权。

##小结

在这个监控临时段使用脚本的创建执行过程中，遇到的主要是权限方面的问题，针对动态性能视图，同义词，以及存储过程。不过，即使根据文档解决了这些问题，还是没理解它们为什么会存在，为什么要这样设计。

这里先记录以作备忘：

* Oracle数据库的权限和角色，以及它们的限制；
* 函数、存储过程的授权；
* Job,Database Link中的权限问题；
* 同义词的授权；

##参考

* Oracle Database Concepts
* [Oracle Temp临时表空间](http://blog.csdn.net/tianlesoftware/article/details/4697417)
* [浅谈Job和Database Link的一个特点](http://yangtingkun.itpub.net/post/468/7984)
* [DBMS_JOB用法](http://blog.csdn.net/tianlesoftware/article/details/4703133)