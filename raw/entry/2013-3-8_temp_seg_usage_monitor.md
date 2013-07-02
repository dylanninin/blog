	[oracle@wxerp ~]$ sqlplus /nolog
	
	SQL*Plus: Release 10.2.0.1.0 - Production on Fri Mar 8 11:34:24 2013
	
	Copyright (c) 1982, 2005, Oracle.  All rights reserved.
	
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
	
	
	SQL> create user xxtp_dba identified by xxtp_dba
	  2  default tablespace dba_data
	  3  temporary tablespace dba_tmp;
	
	User created.
	
	SQL> grant resource,connect,dba to xxtp_dba;
	
	Grant succeeded.
	
	SQL> grant select on v_$session to xxtp_dba;
	
	Grant succeeded.
	
	SQL> grant select on v_$sort_usage to xxtp_dba;
	
	Grant succeeded.
	
	SQL> grant select on v_$sqlarea to xxtp_dba;
	
	Grant succeeded.
	
	SQL> conn xxtp_dba
	Enter password: 
	Connected.
	SQL> CREATE TABLE WXERP_TEMP_SEG_USAGE(
	 2      DATE_TIME DATE,
	 3      USERNAME VARCHAR2(30),
	 4      SID VARCHAR2(6),
	 5      SERIAL# VARCHAR2(6),
	 6      OS_USER VARCHAR2(30),
	 7      SPACE_USED NUMBER,
	 8      SQL_TEXT VARCHAR2(1000)
	 9   );   
	
	Table created.
	
	SQL> CREATE OR REPLACE PROCEDURE WXERP_TEMP_SEG_USAGE_P IS
	  2  BEGIN
	  3      INSERT INTO WXERP_TEMP_SEG_USAGE
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
	 19  END WXERP_TEMP_SEG_USAGE_P;
	 20  /
	
	Procedure created.
	
	SQL> BEGIN
			DBMS_JOB.ISUBMIT(JOB=>2,WHAT=> 'WXERP_TEMP_SEG_USAGE_P;',NEXT_DATE => SYSDATE,INTERVAL  => 'sysdate + (5/1440)');
			COMMIT;
		END;
		/

	PL/SQL procedure successfully completed.