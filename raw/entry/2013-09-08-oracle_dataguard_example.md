---
layout: post
title: Oracle DataGuard Example
category : Oracle
tags : [Oracle, Database, DBA]
---

##Environment

* primary    192.168.1.100    CentOS 6.0 64bit  Oracle 11gR2  primary database
* standby    192.168.2.100    Redhat 5.5 64bit  Oracle 10g    standby database

##Primary Database

force logging

    [root@primary conf]# su - oracle
    [oracle@primary ~]$ sqlplus  /nolog

    SQL*Plus: Release 11.2.0.1.0 Production on Sun Sep 8 14:56:17 2013

    Copyright (c) 1982, 2009, Oracle.  All rights reserved.

    SQL> conn /as sysdba
    Connected.
    SQL> select force_logging from v$database;

    FOR
    ---
    NO

    SQL> alter database force logging;

    Database altered.

enable archivelog
    
    SQL> archive log list;
    Database log mode	       No Archive Mode
    Automatic archival	       Disabled
    Archive destination	       USE_DB_RECOVERY_FILE_DEST
    Oldest online log sequence     634
    Current log sequence	       636
    SQL> shutdown immediate; 
    Database closed.
    Database dismounted.
    ORACLE instance shut down.
    SQL> startup mount; 
    ORACLE instance started.

    Total System Global Area 3290345472 bytes
    Fixed Size		    2217832 bytes
    Variable Size		 2365589656 bytes
    Database Buffers	  905969664 bytes
    Redo Buffers		   16568320 bytes
    Database mounted.
    SQL> alter database archivelog;

    Database altered.

    SQL> alter database open;

    Database altered.

    SQL> archive log list;
    Database log mode	       Archive Mode
    Automatic archival	       Enabled
    Archive destination	       USE_DB_RECOVERY_FILE_DEST
    Oldest online log sequence     634
    Next log sequence to archive   636
    Current log sequence	       636
    SQL> show parameter log_archive

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    log_archive_config		     string
    log_archive_dest		     string	 /db/oracle/arch/
    log_archive_dest_1		     string
    log_archive_dest_10		     string
    log_archive_dest_11		     string
    log_archive_dest_12		     string
    log_archive_dest_13		     string
    log_archive_dest_14		     string
    log_archive_dest_15		     string
    log_archive_dest_16		     string
    log_archive_dest_17		     string

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    log_archive_dest_18		     string
    log_archive_dest_19		     string
    log_archive_dest_2		     string
    log_archive_dest_20		     string
    log_archive_dest_21		     string
    log_archive_dest_22		     string
    log_archive_dest_23		     string
    log_archive_dest_24		     string
    log_archive_dest_25		     string
    log_archive_dest_26		     string
    log_archive_dest_27		     string

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    log_archive_dest_28		     string
    log_archive_dest_29		     string
    log_archive_dest_3		     string
    log_archive_dest_30		     string
    log_archive_dest_31		     string
    log_archive_dest_4		     string
    log_archive_dest_5		     string
    log_archive_dest_6		     string
    log_archive_dest_7		     string
    log_archive_dest_8		     string
    log_archive_dest_9		     string

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    log_archive_dest_state_1	     string	 enable
    log_archive_dest_state_10	     string	 enable
    log_archive_dest_state_11	     string	 enable
    log_archive_dest_state_12	     string	 enable
    log_archive_dest_state_13	     string	 enable
    log_archive_dest_state_14	     string	 enable
    log_archive_dest_state_15	     string	 enable
    log_archive_dest_state_16	     string	 enable
    log_archive_dest_state_17	     string	 enable
    log_archive_dest_state_18	     string	 enable
    log_archive_dest_state_19	     string	 enable

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    log_archive_dest_state_2	     string	 enable
    log_archive_dest_state_20	     string	 enable
    log_archive_dest_state_21	     string	 enable
    log_archive_dest_state_22	     string	 enable
    log_archive_dest_state_23	     string	 enable
    log_archive_dest_state_24	     string	 enable
    log_archive_dest_state_25	     string	 enable
    log_archive_dest_state_26	     string	 enable
    log_archive_dest_state_27	     string	 enable
    log_archive_dest_state_28	     string	 enable
    log_archive_dest_state_29	     string	 enable

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    log_archive_dest_state_3	     string	 enable
    log_archive_dest_state_30	     string	 enable
    log_archive_dest_state_31	     string	 enable
    log_archive_dest_state_4	     string	 enable
    log_archive_dest_state_5	     string	 enable
    log_archive_dest_state_6	     string	 enable
    log_archive_dest_state_7	     string	 enable
    log_archive_dest_state_8	     string	 enable
    log_archive_dest_state_9	     string	 enable
    log_archive_duplex_dest 	     string
    log_archive_format		     string	 %t_%s_%r.dbf

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    log_archive_local_first 	     boolean	 TRUE
    log_archive_max_processes	     integer	 4
    log_archive_min_succeed_dest	     integer	 1
    log_archive_start		     boolean	 FALSE
    log_archive_trace		     integer	 0
    
add standby logfile group
    
    SQL> select group#,sequence#,members,archived,status from v$log;

        GROUP#  SEQUENCE#	 MEMBERS ARC STATUS
    ---------- ---------- ---------- --- ----------------
         1	  634	       1 YES INACTIVE
         2	  635	       1 YES INACTIVE
         3	  636	       1 NO  CURRENT

    SQL> alter database add standby logfile group 4 ('/db/oracle/oradata/test/log4a.log','/db/oracle/oradata/test/log4b.log')size 50M;

    Database altered.

    SQL> alter database add standby logfile group 5 ('/db/oracle/oradata/test/log5a.log','/db/oracle/oradata/test/log5b.log')size 50M;

    Database altered.

    SQL> alter database add standby logfile group 6 ('/db/oracle/oradata/test/log6a.log','/db/oracle/oradata/test/log6b.log')size 50M;

    Database altered.

    SQL> alter database add standby logfile group 7 ('/db/oracle/oradata/test/log7a.log','/db/oracle/oradata/test/log7b.log')size 50M;

    Database altered.

    SQL> select group#,thread#,sequence#,archived,status from v$standby_log;

        GROUP#    THREAD#  SEQUENCE# ARC STATUS
    ---------- ---------- ---------- --- ----------
         4	    0	       0 YES UNASSIGNED
         5	    0	       0 YES UNASSIGNED
         6	    0	       0 YES UNASSIGNED
         7	    0	       0 YES UNASSIGNED

add dataguard configuration in pfile      
         
    SQL> create pfile from spfile;

    File created.

    SQL> shutdown immediate;
    Database closed.
    Database dismounted.
    ORACLE instance shut down.
    SQL> 
  
    [oracle@primary primary]$ cd /db/oracle/product/11.2.0/db_1/dbs/
    [oracle@primary dbs]$ ls -al
    total 9840
    drwxr-xr-x.  2 oracle oinstall     4096 Sep  8 15:01 .
    drwxr-xr-x. 74 oracle oinstall     4096 Jul 19 14:30 ..
    -rw-rw----.  1 oracle oinstall     1544 Sep  8 15:01 hc_primary.dat
    -rw-r--r--.  1 oracle oinstall     2851 May 15  2009 init.ora
    -rw-r--r--.  1 oracle oinstall      993 Sep  8 15:01 initprimary.ora
    -rw-r-----.  1 oracle oinstall       24 Jul 19 14:27 lkprimary
    -rw-r-----.  1 oracle oinstall     1536 Sep  8 14:25 orapwprimary
    -rw-r-----.  1 oracle oinstall 10043392 Sep  8 13:20 snapcf_primary.f
    -rw-r-----.  1 oracle oinstall     3584 Sep  8 14:57 spfileprimary.ora
    [oracle@primary dbs]$ cp initprimary.ora initprimary.ora.dist
    [oracle@primary dbs]$ vim initprimary.ora
    ... ...
    #2013-9-8    dylanninin    settings for primary database
    *.db_unique_name='primary'
    *.log_archive_config='dg_config=(primary,standby)'
    *.log_archive_dest_1='location=/db/oracle/arch valid_for=(all_logfiles,all_roles)'
    *.log_archive_dest_2='service=standby arch async valid_for=(online_logfiles,primary_role) db_unique_name=standby'
    *.log_archive_dest_state_1='enable'
    *.log_archive_dest_state_2='enable'
    *.standby_file_management='auto'
    *.standby_archive_dest='/db/oracle/arch'
    *.fal_client='primary'
    *.fal_server='standby'

    SQL> conn /as sysdba
    Connected to an idle instance.
    SQL> startup pfile=?/dbs/initprimary.ora
    ORACLE instance started.

    Total System Global Area 3290345472 bytes
    Fixed Size		    2217832 bytes
    Variable Size		 2365589656 bytes
    Database Buffers	  905969664 bytes
    Redo Buffers		   16568320 bytes
    Database mounted.
    Database opened.
    SQL> create spfile from pfile; 

    File created.

    SQL> shutdown immediate;
    Database closed.
    Database dismounted.
    ORACLE instance shut down.
    SQL> startup
    ORA-32004: obsolete or deprecated parameter(s) specified for RDBMS instance
    ORACLE instance started.

    Total System Global Area 3290345472 bytes
    Fixed Size		    2217832 bytes
    Variable Size		 2365589656 bytes
    Database Buffers	  905969664 bytes
    Redo Buffers		   16568320 bytes
    Database mounted.
    Database opened.
    SQL> show parameter spfile

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    spfile				     string	 /db/oracle/product/11.2.0/db_1
                             /dbs/spfileprimary.ora
                 
create standby controlfile                 
                     
    SQL> alter database create standby controlfile as '/db/oracle/standby.ctl';

    Database altered.

shutdown database
    
    SQL> shutdown immediate
    Database closed.
    Database dismounted.
    ORACLE instance shut down.

edit listener.ora and tnsnames.ora
    
    [oracle@primary admin]$ pwd
    /db/oracle/product/11.2.0/db_1/network/admin

    [oracle@primary admin]$ cat listener.ora 
    # listener.ora Network Configuration File: /db/oracle/product/11.2.0/db_1/network/admin/listener.ora
    # Generated by Oracle configuration tools.

    LISTENER =
      (DESCRIPTION_LIST =
        (DESCRIPTION =
          (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1521))
          (ADDRESS = (PROTOCOL = TCP)(HOST = primary.egolife.com)(PORT = 1521))
        )
      )

    SID_LIST_LISTENER =
      (SID_LIST =
        (SID_DESC =
          (SID_NAME = PLSExtProc)
          (ORACLE_HOME = /db/oracle/product/11.2.0/db_1)
          (PROGRAM = extproc)
        )
        (SID_DESC =
          (GLOBAL_DBNAME = primary)
          (ORACLE_HOME = /db/oracle/product/11.2.0/db_1)
          (SID_NAME = primary)
        )
      )

    ADR_BASE_LISTENER = /db/oracle


    [oracle@primary admin]$ cat tnsnames.ora
    # tnsnames.ora Network Configuration File: /db/oracle/product/11.2.0/db_1/network/admin/tnsnames.ora
    # Generated by Oracle configuration tools.

    primary =
      (DESCRIPTION =
        (ADDRESS = (PROTOCOL = TCP)(HOST =192.168.1.100)(PORT = 1521))
        (CONNECT_DATA =
          (SERVER = DEDICATED)
          (SERVICE_NAME = primary)
        )
      )

    standby =
      (DESCRIPTION =
        (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.2.100)(PORT = 1521))
        (CONNECT_DATA =
          (SERVER = DEDICATED)
          (SERVICE_NAME = primary)
        )
      )
  
  
##Copy files to Standby Database
  
scp datafile,pfile/spfile/orapwd,tnsnames,listener to standby database

##Standby Database

edut dataguard configuration in pfile

    [oracle@standby ~]$ cd /db/oracle/product/11.2.0/db_1/dbs/
    [oracle@standby dbs]$ vim initprimary.ora
    ... ...
    *.control_files='/db/oracle/oradata/test/standby.ctl'
    ... ...
    #2013-9-8    dylanninin    settings for primary database
    *.db_unique_name='standby'
    *.log_archive_config='dg_config=(primary,standby)'
    *.log_archive_dest_1='location=/db/oracle/arch valid_for=(all_logfiles,all_roles) db_unique_name=standby'
    *.log_archive_dest_2='service=primary db_unique_name=primary'
    *.log_archive_dest_state_1='enable'
    *.log_archive_dest_state_2='enable'
    *.standby_file_management='auto'
    *.standby_archive_dest='/db/oracle/arch'
    *.fal_client='standby'
    *.fal_server='primary'

mount standby database and start listener

    [oracle@standby ~]$ sqlplus  /nolog

    SQL*Plus: Release 11.2.0.1.0 Production on Sun Sep 8 17:28:26 2013

    Copyright (c) 1982, 2009, Oracle.  All rights reserved.

    SQL> conn /as sysdba
    Connected to an idle instance.
    SQL> startup nomount pfile=?/dbs/initprimary.ora
    ORA-32006: STANDBY_ARCHIVE_DEST initialization parameter has been deprecated
    ORACLE instance started.

    Total System Global Area 1653518336 bytes
    Fixed Size		    2213896 bytes
    Variable Size		  939526136 bytes
    Database Buffers	  704643072 bytes
    Redo Buffers		    7135232 bytes

    SQL> alter database mount standby database;

    Database altered.

    [oracle@standby ~]$ lsnrctl start

start primary database and listener

##test archivelog sync and apply

primary database

    SQL> archive log list;
    Database log mode	       Archive Mode
    Automatic archival	       Enabled
    Archive destination	       /db/oracle/arch
    Oldest online log sequence     638
    Next log sequence to archive   640
    Current log sequence	       640
    SQL> alter system switch logfile;

    System altered.

    SQL> alter system switch logfile;

    System altered.

    SQL> archive log list;
    Database log mode	       Archive Mode
    Automatic archival	       Enabled
    Archive destination	       /db/oracle/arch
    Oldest online log sequence     640
    Next log sequence to archive   642
    Current log sequence	       642


standby database

    SQL> conn /as sysdba
    Connected.
    SQL> archive log list;
    Database log mode	       Archive Mode
    Automatic archival	       Enabled
    Archive destination	       /db/oracle/arch
    Oldest online log sequence     640
    Next log sequence to archive   0
    Current log sequence	       642


##common operations

switch logfile to archive log

    SQL> alter system switch logfile;

views to check logfile,archivelog in primary/standby database
    
    select max(sequence#) from v$archived_log; 
    select max(sequence#) from v$log_history; 
    select group#,sequence#,archived,status from v$log; 
    select name,sequence#,applied from v$archived_log; 

switch between primary/standby database

    
sync failure
    
1）check whether archivelogs are missing; if then to copy and register missing archivelogs manually. 

	--register archivelog
	alter database register logfile '/path/to/the/missing/archivelog';

2）apply archivelog in standby database： 

	--cancel applying archivelog
	alter database recover managed standby database cancel; 

	--apply archivelog
	alter database recover managed standby database disconnect from session; 
	
##Reference

* [如何搭建一个DataGuard环境](http://blog.csdn.net/tianlesoftware/article/details/6195771)
* [David Dave -- DataGuard 专题](http://blog.csdn.net/tianlesoftware/article/category/700326)