---
layout: post
title: Temp Segment Usage Monitor
category : Oracle
tags : [Oracle, Database, DBA]
---

How to Monitor the usage of temp segment.

create tablespace for dba_test
	
	SQL> conn /as sysdba
	Connected.
	SQL> create tablespace dba_data datafile '/db/oracle/oradata/wxprod/dba_data01.dbf' size 1000M;
	
	Tablespace created.
	
	SQL> create tablespace dba_idx datafile '/db/oracle/oradata/wxprod/dba_idx01.dbf' size 500M;
	
	Tablespace created.
	
	
	SQL> create temporary tablespace dba_tmp tempfile '/db/oracle/oradata/wxprod/dba_tmp01.dbf' size 500M;
	
	Tablespace created.
	
	SQL> alter system switch logfile;
	
	System altered.
	

create user dba_test and grant privileges
	
	SQL> create user dba_test identified by dba_test
	  2  default tablespace dba_data
	  3  temporary tablespace dba_tmp;
	
	User created.
	
	SQL> grant resource,connect,dba to dba_test;
	
	Grant succeeded.
	
	SQL> grant select on v_$session to dba_test;
	
	Grant succeeded.
	
	SQL> grant select on v_$sort_usage to dba_test;
	
	Grant succeeded.
	
	SQL> grant select on v_$sqlarea to dba_test;
	
	Grant succeeded.
	
create table `TEMP_SEG_USAGE` for storing temp segment usage statistics
	
	SQL> conn dba_test
	Enter password: 
	Connected.
	SQL> CREATE TABLE TEMP_SEG_USAGE(
	 2      DATE_TIME DATE,
	 3      USERNAME VARCHAR2(30),
	 4      SID VARCHAR2(6),
	 5      SERIAL# VARCHAR2(6),
	 6      OS_USER VARCHAR2(30),
	 7      SPACE_USED NUMBER,
	 8      SQL_TEXT VARCHAR2(1000)
	 9   );   
	
	Table created.
	
create procudure and submit as a job
	
	SQL> CREATE OR REPLACE PROCEDURE TEMP_SEG_USAGE_P IS
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
	
	Procedure created.
	
	SQL> BEGIN
			DBMS_JOB.ISUBMIT(JOB=>2,WHAT=> 'TEMP_SEG_USAGE_P;',NEXT_DATE => SYSDATE,INTERVAL  => 'sysdate + (5/1440)');
			COMMIT;
		END;
		/

	PL/SQL procedure successfully completed.
	
##Reference

* MOS: How to Monitor the usage of temp segment.
* [Privileges in PL/SQL](http://dylanninin.com/blog/2013/03/07/privileges_in_plsql.html)