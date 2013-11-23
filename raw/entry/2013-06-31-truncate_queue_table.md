---
layout: post
title: Truncate Queue Table in Oracle EBS
category : Oracle
tags : [Oracle, Database, DBA, EBS, Excepiton]
---

##Truncate Table

database version

	SQL> select * from v$version;

	BANNER
	-------------------------------------------------------------------------
	Oracle9i Enterprise Edition Release 9.2.0.6.0 - 64bit Production
	PL/SQL Release 9.2.0.6.0 - Production
	CORE    9.2.0.6.0       Production
	TNS for IBM/AIX RISC System/6000: Version 9.2.0.6.0 - Production
	NLSRTL Version 9.2.0.6.0 - Production

truncate table

	truncate table ASO.ASO_ORDER_FEEDBACK_T;
    
segment size

	SELECT DS.OWNER,
	       DS.SEGMENT_NAME,
	       DS.SEGMENT_TYPE,
	       (SUM(BYTES) / 1024 / 1024) "SEGMENT_SIZE(MB)"
	  FROM DBA_SEGMENTS DS
	 WHERE DS.SEGMENT_NAME = UPPER('&segment')
	 GROUP BY DS.OWNER, DS.SEGMENT_NAME, DS.SEGMENT_TYPE;

   	OWNER	SEGMENT_NAME			SEGMENT_TYPE	SEGMENT_SIZE(MB)
    ------ ------------------------ --------------- ------------------------
	ASO		ASO_ORDER_FEEDBACK_T	TABLE			34908
 


##Metalink Note
 
suggested truncate operation 

1.truncate table reuse storage

    Connect as apps

    truncate table ASO.ASO_ORDER_FEEDBACK_T REUSE STORAGE;
    truncate table ASO.AQ$_ASO_ORDER_FEEDBACK_T_I REUSE STORAGE; 
    truncate table ASO.AQ$_ASO_ORDER_FEEDBACK_T_H REUSE STORAGE;
    truncate table ASO.AQ$_ASO_ORDER_FEEDBACK_T_T REUSE STORAGE;

    COMMIT;


2.grant execute privilege

    Connect as sysdba
    
    grant execute on SYS.DBMS_AQADM to ASO WITH GRANT OPTION;
    grant execute on SYS.DBMS_AQADM to APPS WITH GRANT OPTION;
    grant execute on SYS.DBMS_AQ to ASO WITH GRANT OPTION;
    grant execute on SYS.DBMS_AQ to APPS WITH GRANT OPTION;
 
3.execute asoqueue.sql
 
    # su - me
    $ cd $ASO_TOP/patch/115/sql/
    $ pwd
    /u2/TEST/me/testappl/aso/11.5.0/patch/115/sql
    $ ls -l asoqueue.sql
    -rwxr-xr-x   1 me  dba           60010 Jun 16 12:55 asoqueue.sql

    $ sqlplus apps/p0809ad @asoqueue apps p0809ad aso aso system manager
	... ...
    Connected.

    Grant succeeded.

    GRANT EXECUTE ON SYS.DBMS_AQ TO aso
                         *
    ERROR at line 1:
    ORA-04021: timeout occurred while waiting to lock object SYS.DBMS_AQ
	... ...

4.deallocate unused space
 
    ALTER TABLE ASO.ASO_ORDER_FEEDBACK_T DEALLOCATE UNUSED;
    ALTER TABLE ASO.AQ$_ASO_ORDER_FEEDBACK_T_I DEALLOCATE UNUSED;
    ALTER TABLE ASO.AQ$_ASO_ORDER_FEEDBACK_T_H DEALLOCATE UNUSED;
    ALTER TABLE ASO.AQ$_ASO_ORDER_FEEDBACK_T_T DEALLOCATE UNUSED;

##Error Message

ORA-04021: Timeout occurred while waiting to lock object SYS.DBMS_AQADM.

You encounter this error when running the Runtime Repository Assistant. There are two possible resolutions to this issue.

Cause: The Runtime Assistant grants 'Execute' privileges on the SYS user dbms_aq packages to the Runtime Repository users being created. The database server waits for a lock on the dbms_aq package before it can apply this grant. If the package is in use by another user, the Runtime Repository will encounter error ORA-04021 from the database server.

Action: Using Oracle Enterprise Manager, connect to the database server and identify the session that is using the dbms_aq. Exit the application that is holding the lock and then recreate a new set of Warehouse Builder Runtime Repository users.

Action: Wait until the application holding the lock finishes running.

From `SQL*Plus`, connect as SYS user and execute the following SQL statements:

    grant execute on sys.dbms_aq to scott;
    grant execute on sys.dbms_aqadm to scott;

When the above statements are successful, execute the following SQL statements:

    revoke execute on sys.dbms_aq from scott;
    revoke execute on sys.dbms_aqadm from scott;

Recreate a new set of Warehouse Builder Runtime Repository users.
Restart the Runtime Platform Service by running the ORACLE_HOME\owb\rtp\sql\start_service.sql script.
    
##Diagnose while re-executing asoqueue.sql
    
    $ whoami
    testora
    $ sqlplus "/ as sysdba"

    SQL*Plus: Release 9.2.0.6.0 - Production on Wed Jul 3 16:25:02 2013

    Copyright (c) 1982, 2002, Oracle Corporation.  All rights reserved.


    Connected to:
    Oracle9i Enterprise Edition Release 9.2.0.6.0 - 64bit Production
    With the Partitioning, OLAP and Oracle Data Mining options
    JServer Release 9.2.0.6.0 - Production
    
    SQL> oradebug setmypid 
    oradebug unlimit 
    oradebug hanganalyze 3 
    Statement processed.
    SQL> Statement processed.
    SQL> Hang Analysis in /u2/TEST/testora/testdb/9.2.0/admin/ERP_erp/udump/erp_ora_1863752.trc
    SQL> 
    SQL> oradebug setmypid 
    oradebug unlimit 
    oradebug hanganalyze 3 
    Statement processed.
    SQL> Statement processed.
    SQL> Hang Analysis in /u2/TEST/testora/testdb/9.2.0/admin/ERP_erp/udump/erp_ora_1863752.trc
    SQL> 
    SQL> select sid,event from v$session_wait;

           SID EVENT
    ---------- ----------------------------------------------------------------
             1 pmon timer
             2 rdbms ipc message
             3 rdbms ipc message
             6 rdbms ipc message
             7 rdbms ipc message
            10 rdbms ipc message
             9 rdbms ipc message
             4 rdbms ipc message
             5 smon timer
            31 library cache pin
            32 library cache pin

           SID EVENT
    ---------- ----------------------------------------------------------------
            38 library cache pin
            46 library cache pin
            92 library cache pin
           114 library cache pin
           157 library cache pin
           184 library cache pin
           190 library cache pin
           186 library cache pin
           170 library cache pin
           127 library cache pin
           106 library cache pin

           SID EVENT
    ---------- ----------------------------------------------------------------
            80 library cache pin
            20 pipe get
            43 pipe get
            63 pipe get
            65 pipe get
           223 pipe get
           210 pipe get
           155 pipe get
           150 pipe get
           144 pipe get
           140 pipe get

           SID EVENT
    ---------- ----------------------------------------------------------------
           126 pipe get
           124 pipe get
           116 pipe get
           113 pipe get
            79 SQL*Net message to client
             8 SQL*Net message from client
            11 SQL*Net message from client
            12 SQL*Net message from client
            21 SQL*Net message from client
            24 SQL*Net message from client
            27 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
            29 SQL*Net message from client
            41 SQL*Net message from client
            40 SQL*Net message from client
            39 SQL*Net message from client
            37 SQL*Net message from client
            36 SQL*Net message from client
            35 SQL*Net message from client
            34 SQL*Net message from client
            33 SQL*Net message from client
            30 SQL*Net message from client
            61 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
            60 SQL*Net message from client
            59 SQL*Net message from client
            58 SQL*Net message from client
            57 SQL*Net message from client
            56 SQL*Net message from client
            54 SQL*Net message from client
            53 SQL*Net message from client
            52 SQL*Net message from client
            97 SQL*Net message from client
            96 SQL*Net message from client
            95 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
            94 SQL*Net message from client
            91 SQL*Net message from client
            90 SQL*Net message from client
            88 SQL*Net message from client
            86 SQL*Net message from client
            84 SQL*Net message from client
           122 SQL*Net message from client
           121 SQL*Net message from client
           120 SQL*Net message from client
           119 SQL*Net message from client
           118 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
           117 SQL*Net message from client
           110 SQL*Net message from client
           109 SQL*Net message from client
           108 SQL*Net message from client
           145 SQL*Net message from client
           143 SQL*Net message from client
           142 SQL*Net message from client
           141 SQL*Net message from client
           139 SQL*Net message from client
           138 SQL*Net message from client
           137 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
           136 SQL*Net message from client
           135 SQL*Net message from client
           227 SQL*Net message from client
           225 SQL*Net message from client
           222 SQL*Net message from client
           221 SQL*Net message from client
           220 SQL*Net message from client
           219 SQL*Net message from client
           218 SQL*Net message from client
           217 SQL*Net message from client
           216 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
           215 SQL*Net message from client
           214 SQL*Net message from client
           213 SQL*Net message from client
           212 SQL*Net message from client
           211 SQL*Net message from client
           209 SQL*Net message from client
           208 SQL*Net message from client
           207 SQL*Net message from client
           205 SQL*Net message from client
           204 SQL*Net message from client
           203 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
           202 SQL*Net message from client
           201 SQL*Net message from client
           199 SQL*Net message from client
           198 SQL*Net message from client
           197 SQL*Net message from client
           196 SQL*Net message from client
           195 SQL*Net message from client
           194 SQL*Net message from client
           193 SQL*Net message from client
           189 SQL*Net message from client
           188 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
           187 SQL*Net message from client
           185 SQL*Net message from client
           183 SQL*Net message from client
           180 SQL*Net message from client
           179 SQL*Net message from client
           178 SQL*Net message from client
           177 SQL*Net message from client
           176 SQL*Net message from client
           175 SQL*Net message from client
           174 SQL*Net message from client
           173 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
           172 SQL*Net message from client
           168 SQL*Net message from client
           167 SQL*Net message from client
           166 SQL*Net message from client
           165 SQL*Net message from client
           164 SQL*Net message from client
           163 SQL*Net message from client
           162 SQL*Net message from client
           161 SQL*Net message from client
           160 SQL*Net message from client
           156 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
           154 SQL*Net message from client
           153 SQL*Net message from client
           152 SQL*Net message from client
           151 SQL*Net message from client
           149 SQL*Net message from client
           148 SQL*Net message from client
           147 SQL*Net message from client
           146 SQL*Net message from client
           134 SQL*Net message from client
           133 SQL*Net message from client
           131 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
           130 SQL*Net message from client
           129 SQL*Net message from client
           128 SQL*Net message from client
           125 SQL*Net message from client
           123 SQL*Net message from client
           105 SQL*Net message from client
           104 SQL*Net message from client
           103 SQL*Net message from client
           102 SQL*Net message from client
           101 SQL*Net message from client
           100 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
            99 SQL*Net message from client
            98 SQL*Net message from client
            83 SQL*Net message from client
            82 SQL*Net message from client
            81 SQL*Net message from client
            77 SQL*Net message from client
            76 SQL*Net message from client
            75 SQL*Net message from client
            74 SQL*Net message from client
            73 SQL*Net message from client
            72 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
            71 SQL*Net message from client
            70 SQL*Net message from client
            69 SQL*Net message from client
            68 SQL*Net message from client
            67 SQL*Net message from client
            66 SQL*Net message from client
            62 SQL*Net message from client
            51 SQL*Net message from client
            50 SQL*Net message from client
            49 SQL*Net message from client
            48 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
            47 SQL*Net message from client
            45 SQL*Net message from client
            44 SQL*Net message from client
            42 SQL*Net message from client
            28 SQL*Net message from client
            26 SQL*Net message from client
            22 SQL*Net message from client
            14 SQL*Net message from client
            16 SQL*Net message from client
            17 SQL*Net message from client
            18 SQL*Net message from client

           SID EVENT
    ---------- ----------------------------------------------------------------
            19 queue messages
           206 queue messages
           171 queue messages
            78 queue messages
            23 wakeup time manager

    203 rows selected.
    
    SQL> select /*+ ordered */ w1.sid  waiting_session,
             h1.sid  holding_session,
             w.kgllktype lock_or_pin,
             w.kgllkhdl address,
             decode(h.kgllkmod,  0, 'None', 1, 'Null', 2, 'Share', 3, 'Exclusive',
                'Unknown') mode_held,
             decode(w.kgllkreq,  0, 'None', 1, 'Null', 2, 'Share', 3, 'Exclusive',
              'Unknown') mode_requested
       from dba_kgllock w, dba_kgllock h, v$session w1, v$session h1
      where
       (((h.kgllkmod != 0) and (h.kgllkmod != 1)
          and ((h.kgllkreq = 0) or (h.kgllkreq = 1)))
        and
          (((w.kgllkmod = 0) or (w.kgllkmod= 1))
          and ((w.kgllkreq != 0) and (w.kgllkreq != 1))))
       and  w.kgllktype      =  h.kgllktype
       and  w.kgllkhdl =  h.kgllkhdl
       and  w.kgllkuse     =   w1.saddr
       and  h.kgllkuse     =   h1.saddr
     /
    WAITING_SESSION HOLDING_SESSION LOCK ADDRESS          MODE_HELD MODE_REQU
    --------------- --------------- ---- ---------------- --------- ---------
                175              38 Pin  07000000ACBBE940 Share     Share
                127              38 Pin  07000000ACBBE940 Share     Share
                114              38 Pin  07000000ACBBE940 Share     Share
                110              38 Pin  07000000ACBBE940 Share     Share
                106              38 Pin  07000000ACBBE940 Share     Share
                 80              38 Pin  07000000ACBBE940 Share     Exclusive
                 46              38 Pin  07000000ACBBE940 Share     Share
                 31              38 Pin  07000000ACBBE940 Share     Share
                 30              38 Pin  07000000ACBBE940 Share     Share
                 28              38 Pin  07000000ACBBE940 Share     Share
                175              78 Pin  07000000ACBBE940 Share     Share

    WAITING_SESSION HOLDING_SESSION LOCK ADDRESS          MODE_HELD MODE_REQU
    --------------- --------------- ---- ---------------- --------- ---------
                127              78 Pin  07000000ACBBE940 Share     Share
                114              78 Pin  07000000ACBBE940 Share     Share
                110              78 Pin  07000000ACBBE940 Share     Share
                106              78 Pin  07000000ACBBE940 Share     Share
                 80              78 Pin  07000000ACBBE940 Share     Exclusive
                 46              78 Pin  07000000ACBBE940 Share     Share
                 31              78 Pin  07000000ACBBE940 Share     Share
                 30              78 Pin  07000000ACBBE940 Share     Share
                 28              78 Pin  07000000ACBBE940 Share     Share
                175              92 Pin  07000000ACBBE940 Share     Share
                127              92 Pin  07000000ACBBE940 Share     Share

    WAITING_SESSION HOLDING_SESSION LOCK ADDRESS          MODE_HELD MODE_REQU
    --------------- --------------- ---- ---------------- --------- ---------
                114              92 Pin  07000000ACBBE940 Share     Share
                110              92 Pin  07000000ACBBE940 Share     Share
                106              92 Pin  07000000ACBBE940 Share     Share
                 80              92 Pin  07000000ACBBE940 Share     Exclusive
                 46              92 Pin  07000000ACBBE940 Share     Share
                 31              92 Pin  07000000ACBBE940 Share     Share
                 30              92 Pin  07000000ACBBE940 Share     Share
                 28              92 Pin  07000000ACBBE940 Share     Share
                175             170 Pin  07000000ACBBE940 Share     Share
                127             170 Pin  07000000ACBBE940 Share     Share
                114             170 Pin  07000000ACBBE940 Share     Share

    WAITING_SESSION HOLDING_SESSION LOCK ADDRESS          MODE_HELD MODE_REQU
    --------------- --------------- ---- ---------------- --------- ---------
                110             170 Pin  07000000ACBBE940 Share     Share
                106             170 Pin  07000000ACBBE940 Share     Share
                 80             170 Pin  07000000ACBBE940 Share     Exclusive
                 46             170 Pin  07000000ACBBE940 Share     Share
                 31             170 Pin  07000000ACBBE940 Share     Share
                 30             170 Pin  07000000ACBBE940 Share     Share
                 28             170 Pin  07000000ACBBE940 Share     Share
                175             184 Pin  07000000ACBBE940 Share     Share
                127             184 Pin  07000000ACBBE940 Share     Share
                114             184 Pin  07000000ACBBE940 Share     Share
                110             184 Pin  07000000ACBBE940 Share     Share

    WAITING_SESSION HOLDING_SESSION LOCK ADDRESS          MODE_HELD MODE_REQU
    --------------- --------------- ---- ---------------- --------- ---------
                106             184 Pin  07000000ACBBE940 Share     Share
                 80             184 Pin  07000000ACBBE940 Share     Exclusive
                 46             184 Pin  07000000ACBBE940 Share     Share
                 31             184 Pin  07000000ACBBE940 Share     Share
                 30             184 Pin  07000000ACBBE940 Share     Share
                 28             184 Pin  07000000ACBBE940 Share     Share

    50 rows selected.
    
    SQL> oradebug setmypid 
    oradebug unlimit 
    oradebug hanganalyze 3 
    Statement processed.
    SQL> Statement processed.
    SQL> Hang Analysis in /u2/TEST/testora/testdb/9.2.0/admin/ERP_erp/udump/erp_ora_1863752.trc
    SQL> host vi /u2/TEST/testora/testdb/9.2.0/admin/ERP_erp/udump/erp_ora_1863752.trc
    "/u2/TEST/testora/testdb/9.2.0/admin/ERP_erp/udump/erp_ora_1863752.trc" 880 lines, 45434 characters Dump file /u2/TEST/testora/testdb/9.2.0/admin/ERP_erp/udump/erp_ora_1863752.trc
    Oracle9i Enterprise Edition Release 9.2.0.6.0 - 64bit Production
    With the Partitioning, OLAP and Oracle Data Mining options
    JServer Release 9.2.0.6.0 - Production
    ORACLE_HOME = /u2/TEST/testora/testdb/9.2.0
    System name:    AIX
    Node name:erp
    Release:3
    Version:5
    Machine:00066345D600
    Instance name: ERP
    Redo thread mounted by this instance: 1
    Oracle process number: 70
    Unix process pid: 1863752, image: oracle@erp (TNS V1-V3)

    *** SESSION ID:(79.3983) 2013-07-03 16:25:16.197
    *** 2013-07-03 16:25:16.197
    ==============
    HANG ANALYSIS:
    ==============
    Open chains found:
    Chain 1 : <cnode/sid/sess_srno/proc_ptr/ospid/wait_event> :
        <0/38/37/0xa87b3b68/2388080/queue messages>
     -- <0/80/7524/0xa879b848/593972/library cache pin>
    Chain 2 : <cnode/sid/sess_srno/proc_ptr/ospid/wait_event> :
        <0/78/1346/0xa87b4ab0/2027618/PL/SQL lock timer>
     -- <0/80/7524/0xa879b848/593972/library cache pin>
    Chain 3 : <cnode/sid/sess_srno/proc_ptr/ospid/wait_event> :
        <0/92/60842/0xa87b4598/2056366/queue messages>
     -- <0/80/7524/0xa879b848/593972/library cache pin>
    Other chains found:
    Chain 4 : <cnode/sid/sess_srno/proc_ptr/ospid/wait_event> :"/u2/TEST/testora/testdb/9.2.0/admin/ERP_erp/udump/erp_ora_1863752.trc" 880 lines, 45434 characters
    
    
    SQL> select username,program,sql_hash_value from v$session where sid=38;

    USERNAME   PROGRAM          SQL_HASH_VALUE
    ---------- ---------------- ---------------------------
    APPS      JDBC Thin Client  4251209219


    SQL> select sql_text from v$sql where hash_value=4251209219;
    SQL_TEXT
    -------------------------------------------------------------------------
    BEGIN FND_CP_GSM_IPC.Get_Message(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10); END;
    
    SQL> select s.sid,p.spid from v$session s,v$process p where s.paddr=p.addr and s.sid in (38,78,92);

           SID SPID
    ---------- ------------
            38 2388080
            92 2056366
            78 2027618

    SQL> host kill -9 2388080

    SQL> host kill -9 2056366

    SQL> host kill -9 2027618
  
##Retest
  
retest and the issue remains

stop apps and asoqueue.sql can be executed successfully.

segment size

	SELECT DS.OWNER,
	       DS.SEGMENT_NAME,
	       DS.SEGMENT_TYPE,
	       (SUM(BYTES) / 1024 / 1024) "SEGMENT_SIZE(MB)"
	  FROM DBA_SEGMENTS DS
	 WHERE DS.SEGMENT_NAME = UPPER('&segment')
	 GROUP BY DS.OWNER, DS.SEGMENT_NAME, DS.SEGMENT_TYPE;

   	OWNER	SEGMENT_NAME			SEGMENT_TYPE	SEGMENT_SIZ
    ------ ------------------------ --------------- -------------------------
    ASO		ASO_ORDER_FEEDBACK_T	TABLE			0.125
   
##Reference:

* Release 11.5.10 / R12 Quoting/Order Capture Order Feedback Queue FAQ [ID 181410.1]