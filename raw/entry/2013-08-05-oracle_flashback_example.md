---
layout: post
title: Oracle Flashbackup Examples
category : Oracle
tags : [Oracle, Database, DBA]
---

## flashback database

check flashback settings

    SQL> conn /as sysdba
    Connected.
    SQL> show parameter db_recovery

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    db_recovery_file_dest		     string	 /db/oracle/flash_recovery_area
    db_recovery_file_dest_size	     big integer 3882M
    SQL> archive log list;
    Database log mode	       Archive Mode
    Automatic archival	       Enabled
    Archive destination	       /db/oracle/arch
    Oldest online log sequence     1019
    Next log sequence to archive   1021
    Current log sequence	       1021
    SQL> select flashback_on from v$database;

    FLASHBACK_ON
    ------------------
    YES

current scn or time
    
    SQL> select current_scn from v$database;

    CURRENT_SCN
    -----------
       90142039

    SQL> select to_char(sysdate, 'yy-mm-dd hh24:mi:ss') time from dual;

    TIME
    -----------------
    13-08-05 15:53:37

drop table
    
    SQL> select count(1) from dev.test;

      COUNT(1)
    ----------
         73448

    SQL> drop table dev.test;

    Table dropped.

    SQL> commit;

    Commit complete.

flashback database 
    
    SQL> shutdown immediate;
    Database closed.
    Database dismounted.
    ORACLE instance shut down.
    SQL> startup mount;
    ORACLE instance started.

    Total System Global Area 1043886080 bytes
    Fixed Size		    2219952 bytes
    Variable Size		  763363408 bytes
    Database Buffers	  272629760 bytes
    Redo Buffers		    5672960 bytes
    Database mounted.
    
    SQL> flashback database to scn 90142039; 
    -- or flashback database to timestamp to_timestamp('13-08-05 15:53:37','yy-mm-dd hh24:mi:ss');

    Flashback complete.

open database
    
    SQL> alter database open resetlogs; --指定scn 或者timestamp 时间点之后产生的数据统统丢失

    Database altered.

    SQL> select count(1) from dev.test;

      COUNT(1)
    ----------
         73448

         
## flashback drop

recyclebin

    SQL> show parameter recycle

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    buffer_pool_recycle		     string
    db_recycle_cache_size		     big integer 0
    recyclebin			     string	 on
    
    SQL> select original_name, object_name from recyclebin;

    no rows selected

flashback drop test
    
    SQL> select * from test;

    TABLE_NAME
    ------------------------------
    SMALLTAB

    SQL> drop table test;

    Table dropped.

    SQL> select * from test;
    select * from test
                  *
    ERROR at line 1:
    ORA-00942: table or view does not exist

    SQL> select original_name, object_name from recyclebin;

    ORIGINAL_NAME			 OBJECT_NAME
    -------------------------------- ------------------------------
    TEST				 BIN$4y/v6z2YgJXgQB2spFgMLQ==$0

    SQL> flashback table test to before drop;

    Flashback complete.

    SQL> select * from test;

    TABLE_NAME
    ------------------------------
    SMALLTAB

    SQL> select original_name, object_name from recyclebin;

    no rows selected

flashback drop test2
    
    SQL> drop table test;

    Table dropped.

    SQL> create table test as select object_id from dba_objects where rownum <= 1;

    Table created.

    SQL> select * from test;

     OBJECT_ID
    ----------
        20

    SQL> drop table test;

    Table dropped.

    SQL> select original_name, object_name from recyclebin;

    ORIGINAL_NAME			 OBJECT_NAME
    -------------------------------- ------------------------------
    TEST				 BIN$4y/v6z2agJXgQB2spFgMLQ==$0
    TEST				 BIN$4y/v6z2bgJXgQB2spFgMLQ==$0

    SQL> flashback table test to before drop;

    Flashback complete.

    SQL> drop table test;

    Table dropped.

    SQL> flashback table test to before drop;

    Flashback complete.

    SQL> select original_name, object_name from recyclebin;

    ORIGINAL_NAME			 OBJECT_NAME
    -------------------------------- ------------------------------
    TEST				 BIN$4y/v6z2agJXgQB2spFgMLQ==$0

    SQL> select * from test;

     OBJECT_ID
    ----------
        20

    SQL> flashback table test to before drop;
    flashback table test to before drop
    *
    ERROR at line 1:
    ORA-38312: original name is used by an existing object


    SQL> flashback table test to before drop rename to test_t;

    Flashback complete.

    SQL> select * from test_t;

    TABLE_NAME
    ------------------------------
    SMALLTAB
    
    SQL> select original_name, object_name from recyclebin;

    no rows selected

flashback drop test3

    SQL> drop table test;

    Table dropped.

    SQL> select original_name, object_name from recyclebin;

    ORIGINAL_NAME			 OBJECT_NAME
    -------------------------------- ------------------------------
    TEST				 BIN$4y/v6z2dgJXgQB2spFgMLQ==$0

    SQL> flashback table "BIN$4y/v6z2dgJXgQB2spFgMLQ==$0" to before drop;

    Flashback complete.

    SQL> select * from test;

     OBJECT_ID
    ----------
        20

    SQL> select original_name, object_name from recyclebin;

    no rows selected

flashback drop test4

    SQL> select * from test;

     OBJECT_ID
    ----------
        20

    SQL> create index test_idx on test(object_id);

    Index created.

    SQL> drop table test;

    Table dropped.

    SQL> select original_name, object_name from recyclebin;

    ORIGINAL_NAME			 OBJECT_NAME
    -------------------------------- ------------------------------
    TEST_IDX			 BIN$4y/v6z2egJXgQB2spFgMLQ==$0
    TEST				 BIN$4y/v6z2fgJXgQB2spFgMLQ==$0

    SQL> select index_name from user_indexes where table_name = 'TEST';

    no rows selected

    SQL> select * from test;
    select * from test
                  *
    ERROR at line 1:
    ORA-00942: table or view does not exist


    SQL> flashback table test to before drop;

    Flashback complete.

    SQL> select original_name, object_name from recyclebin;

    no rows selected

    SQL> select index_name from user_indexes where table_name = 'TEST';

    INDEX_NAME
    ------------------------------
    BIN$4y/v6z2egJXgQB2spFgMLQ==$0

    SQL> alter index "BIN$4y/v6z2egJXgQB2spFgMLQ==$0" rename to test_idx;

    Index altered.

    SQL> select index_name from user_indexes where table_name = 'TEST';

    INDEX_NAME
    ------------------------------
    TEST_IDX
    
## flashback query

nls date format

    SQL> alter session set nls_date_format = 'YYYY-MM-DD hh24:mi:ss';

    Session altered.

flashback query test based on timestamp
    
    SQL> select sysdate from dual;

    SYSDATE
    -------------------
    2013-08-05 16:59:13

    SQL> select * from test;

     OBJECT_ID
    ----------
        20

    SQL> delete from test;

    1 row deleted.

    SQL> commit;

    Commit complete.

    SQL> select * from test;

    no rows selected

    SQL> select * from test as of timestamp sysdate - 5/1440;

    no rows selected

    SQL> select * from test as of timestamp sysdate - 10/1440;

     OBJECT_ID
    ----------
        20

    SQL> select * from test as of timestamp to_timestamp('2013-08-05 16:59:13','YYYY-MM-DD hh24:mi:ss');

     OBJECT_ID
    ----------
        20

flashback query test based on scn
        
    SQL> select dbms_flashback.get_system_change_number from dual;

    GET_SYSTEM_CHANGE_NUMBER
    ------------------------
            90146709

    SQL> select current_scn from v$database;

    CURRENT_SCN
    -----------
       90146895

    SQL> select current_scn from v$database;

    CURRENT_SCN
    -----------
       90146897

    SQL> select * from test_t;

    TABLE_NAME
    ------------------------------
    SMALLTAB

    SQL> delete from test_t;

    1 row deleted.

    SQL> commit;

    Commit complete.

    SQL> select * from test_t;

    no rows selected

    SQL> select * from test_t as of scn 90146897;

    TABLE_NAME
    ------------------------------
    SMALLTAB

    SQL> select * from test_t as of scn 90146709;

    TABLE_NAME
    ------------------------------
    SMALLTAB

    SQL> insert into test_t select * from test_t as of scn 90146709;

    1 row created.

    SQL> commit;

    Commit complete.

    SQL> select * from test_t;

    TABLE_NAME
    ------------------------------
    SMALLTAB

    
    SQL> create or replace function getdate return date
      2  as 
      3      v_date date;
      4  begin
      5      select sysdate into v_date from dual;
      6      return v_date;
      7  end;
      8  /

    Function created.

    SQL> alter session set nls_date_format = 'YYYY-MM-DD hh24:mi:ss';

    Session altered.

    SQL> select getdate() from dual;

    GETDATA()
    -------------------
    2013-08-05 17:10:29

    SQL> select text from dba_source where name='GETDATE' order by line;

    TEXT
    --------------------------------------------------------------------------------
    function getdate return date
    as
        v_date date;
    begin
        select sysdate into v_date from dual;
        return v_date;
    end;

    7 rows selected.

    SQL> drop function getdate;

    Function dropped.

    SQL> select text from dba_source where name='GETDATE' order by line;

    no rows selected

    SQL> select text from dba_source as of timestamp to_timestamp('2013-08-05 17:10:29','YYYY-MM-DD hh24:mi:ss') where name='GETDATE' order by line;
    select text from dba_source as of timestamp to_timestamp('2013-08-05 17:10:29','YYYY-MM-DD hh24:mi:ss') where name='GETDATE' order by line
                     *
    ERROR at line 1:
    ORA-01031: insufficient privileges

    SQL> conn /as sysdba
    Connected.
    SQL> select text from dba_source as of timestamp to_timestamp('2013-08-05 17:10:29','YYYY-MM-DD hh24:mi:ss') where name='GETDATE' order by line;

    TEXT
    --------------------------------------------------------------------------------
    function getdata return date
    as
        v_date date;
    begin
        select sysdate into v_date from dual;
        return v_date;
    end;

    7 rows selected.
    
## flashbak table

    SQL> alter session set nls_date_format = 'YYYY-MM-DD hh24:mi:ss';

    Session altered.

    SQL> select current_scn from v$database;

    CURRENT_SCN
    -----------
       90148131
    
    SQL> select row_movement from user_tables where table_name = 'TEST_T';

    ROW_MOVE
    --------
    DISABLED

    SQL> select * from test_t;

    TABLE_NAME
    ------------------------------
    SMALLTAB

    SQL> delete from test_t;

    1 row deleted.

    SQL> commit;

    Commit complete.

    SQL> select * from test_t;

    no rows selected

    SQL> flashback table test_t to scn 90148131;
    flashback table test_t to scn 90148131
                    *
    ERROR at line 1:
    ORA-08189: cannot flashback the table because row movement is not enabled


    SQL> alter table test_t enable row movement;

    Table altered.

    SQL> flashback table test_t to scn 90148131;

    Flashback complete.

    SQL> select * from test_t;

    TABLE_NAME
    ------------------------------
    SMALLTAB

## Reference

* [Oracle 11gR2 中 Flashback 说明](http://blog.csdn.net/tianlesoftware/article/details/7229802)
* [Oracle Flashback 技术总结](http://blog.csdn.net/tianlesoftware/article/details/4677378)