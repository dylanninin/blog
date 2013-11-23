---
layout: post
title: Oracle STA Example
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

explain plan

    oracle@oradb ~]$ sqlplus  dev

    `SQL*Plus`: Release 11.2.0.1.0 Production on Fri Jul 26 14:15:15 2013

    Copyright (c) 1982, 2009, Oracle.  All rights reserved.

    Enter password: 

    Connected to:
    Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production
    With the Partitioning, OLAP, Data Mining and Real Application Testing options

    SQL> set timing on
    SQL> set autot on
    SQL> select count(1)
      2  from bigtab a,
      3       smalltab b
      4  where a.object_name = b.table_name
      5  /

      COUNT(1)
    ----------
        389961

    Elapsed: 00:00:04.15

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 3089226980

    --------------------------------------------------------------------------------
    | Id  | Operation	    | Name     | Rows  | Bytes | Cost (%CPU)| Time     |
    --------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT    |	       |     1 |    83 | 30501	 (1)| 00:06:07 |
    |   1 |  SORT AGGREGATE     |	       |     1 |    83 |	    |	       |
    |*  2 |   HASH JOIN	    |	       |  5096K|   403M| 30501	 (1)| 00:06:07 |
    |   3 |    TABLE ACCESS FULL| SMALLTAB |  2986 | 50762 |    35	 (0)| 00:00:01 |
    |   4 |    TABLE ACCESS FULL| BIGTAB   |  7955K|   500M| 30440	 (1)| 00:06:06 |
    --------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("A"."OBJECT_NAME"="B"."TABLE_NAME")

    Note
    -----
       - dynamic sampling used for this statement (level=2)


    Statistics
    ----------------------------------------------------------
         32  recursive calls
          0  db block gets
     112161  consistent gets
     111877  physical reads
          0  redo size
        528  bytes sent via SQL*Net to client
        524  bytes received via SQL*Net from client
          2  SQL*Net roundtrips to/from client
          0  sorts (memory)
          0  sorts (disk)
          1  rows processed

    SQL> 
    
1) create tuning task
    
    SQL> set autot off
    SQL> set timing off
    SQL> declare
      2      my_task_name varchar2(50);
      3      my_sql_text clob;
      4  begin
      5      my_sql_text := 'select count(1) from bigtab a,smalltab b where a.object_name = b.table_name';
      6      my_task_name := dbms_sqltune.create_tuning_task(sql_text => my_sql_text, task_name => 'sql_tuning_advisor_test');
      7      dbms_sqltune.execute_tuning_task(task_name => 'sql_tuning_advisor_test');
      8  end;
      9  /
     
    PL/SQL procedure successfully completed.

2) execute tuning task

    SQL> exec dbms_sqltune.execute_tuning_task('sql_tuning_advisor_test');

    PL/SQL procedure successfully completed.

3) view tuning task status

    SQL> select task_name, status from user_advisor_tasks where task_name = 'sql_tuning_advisor_test';
    
    TASK_NAME		       STATUS
    ------------------------------ -----------
    sql_tuning_advisor_test        COMPLETED

4) display tuning report

    SQL> set long 999999
    SQL> set serveroutput on size 999999
    SQL> set linesize 100
    SQL> select dbms_sqltune.report_tuning_task('sql_tuning_advisor_test') from dual;

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------
    GENERAL INFORMATION SECTION
    -------------------------------------------------------------------------------
    Tuning Task Name   : sql_tuning_advisor_test
    Tuning Task Owner  : DEV
    Workload Type	   : Single SQL Statement
    Execution Count    : 2
    Current Execution  : EXEC_4845
    Execution Type	   : TUNE SQL
    Scope		   : COMPREHENSIVE
    Time Limit(seconds): 1800
    Completion Status  : COMPLETED

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------
    Started at	   : 07/26/2013 14:33:47
    Completed at	   : 07/26/2013 14:34:26

    -------------------------------------------------------------------------------
    Schema Name: DEV
    SQL ID	   : 1fyx6kqg3csfb
    SQL Text   : select count(1) from bigtab a,smalltab b where a.object_name =
             b.table_name

    -------------------------------------------------------------------------------
    FINDINGS SECTION (3 findings)

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------
    -------------------------------------------------------------------------------

    1- Statistics Finding
    ---------------------
      Table "DEV"."SMALLTAB" was not analyzed.

      Recommendation
      --------------
      - Consider collecting optimizer statistics for this table.
        execute dbms_stats.gather_table_stats(ownname => 'DEV', tabname =>
            'SMALLTAB', estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE,
            method_opt => 'FOR ALL COLUMNS SIZE AUTO');

      Rationale
      ---------
        The optimizer requires up-to-date statistics for the table in order to
        select a good execution plan.

    2- Statistics Finding
    ---------------------
      Table "DEV"."BIGTAB" was not analyzed.


    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------
      Recommendation
      --------------
      - Consider collecting optimizer statistics for this table.
        execute dbms_stats.gather_table_stats(ownname => 'DEV', tabname =>
            'BIGTAB', estimate_percent => DBMS_STATS.AUTO_SAMPLE_SIZE,
            method_opt => 'FOR ALL COLUMNS SIZE AUTO');

      Rationale
      ---------
        The optimizer requires up-to-date statistics for the table in order to
        select a good execution plan.

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------

    3- Index Finding (see explain plans section below)
    --------------------------------------------------
      The execution plan of this statement can be improved by creating one or more
      indices.

      Recommendation (estimated benefit: 98.99%)
      ------------------------------------------
      - Consider running the Access Advisor to improve the physical schema design
        or creating the recommended index.
        create index DEV.IDX$$_12540001 on DEV.SMALLTAB("TABLE_NAME");

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------

      - Consider running the Access Advisor to improve the physical schema design
        or creating the recommended index.
        create index DEV.IDX$$_12540002 on DEV.BIGTAB("OBJECT_NAME");

      Rationale
      ---------
        Creating the recommended indices significantly improves the execution plan
        of this statement. However, it might be preferable to run "Access Advisor"
        using a representative SQL workload as opposed to a single statement. This
        will allow to get comprehensive index recommendations which takes into

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------
        account index maintenance overhead and additional space consumption.

    -------------------------------------------------------------------------------
    EXPLAIN PLANS SECTION
    -------------------------------------------------------------------------------

    1- Original
    -----------
    Plan hash value: 3089226980

    --------------------------------------------------------------------------------

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------

    | Id  | Operation	    | Name     | Rows  | Bytes | Cost (%CPU)| Time     |

    --------------------------------------------------------------------------------

    |   0 | SELECT STATEMENT    |	       |     1 |    83 | 30501	 (1)| 00:06:07 |

    |   1 |  SORT AGGREGATE     |	       |     1 |    83 |	    |	       |

    |*  2 |   HASH JOIN	    |	       |  5096K|   403M| 30501	 (1)| 00:06:07 |


    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------
    |   3 |    TABLE ACCESS FULL| SMALLTAB |  2986 | 50762 |    35	 (0)| 00:00:01 |

    |   4 |    TABLE ACCESS FULL| BIGTAB   |  7955K|   500M| 30440	 (1)| 00:06:06 |

    --------------------------------------------------------------------------------


    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("A"."OBJECT_NAME"="B"."TABLE_NAME")

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------

    2- Using New Indices
    --------------------
    Plan hash value: 1674279188

    --------------------------------------------------------------------------------
    ---------
    | Id  | Operation	       | Name		| Rows	| Bytes | Cost (%CPU)| T
    ime	|
    --------------------------------------------------------------------------------
    ---------

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT       |		|     1 |    83 |   306   (9)| 0
    0:00:04 |
    |   1 |  SORT AGGREGATE        |		|     1 |    83 |	     |
        |
    |*  2 |   HASH JOIN	       |		|  5096K|   403M|   306   (9)| 0
    0:00:04 |
    |   3 |    INDEX FAST FULL SCAN| IDX$$_12540001 |  2986 | 50762 |    12   (0)| 0
    0:00:01 |
    |   4 |    INDEX FAST FULL SCAN| IDX$$_12540002 |  7955K|   500M|   269   (1)| 0
    0:00:04 |
    --------------------------------------------------------------------------------

    DBMS_SQLTUNE.REPORT_TUNING_TASK('SQL_TUNING_ADVISOR_TEST')
    --------------------------------------------------------------------------------
    ---------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("A"."OBJECT_NAME"="B"."TABLE_NAME")

    -------------------------------------------------------------------------------


    SQL> 
    
5) implement tuning advisor actions

gather table statistics

    SQL> begin
      2      dbms_stats.gather_table_stats(
      3          ownname => 'DEV',
      4          tabname => 'smalltab',
      5          estimate_percent => dbms_stats.auto_sample_size,
      6          method_opt => 'for all columns size auto'
      7      );
      8  end;
      9  /

    PL/SQL procedure successfully completed.

    SQL> begin
      2      dbms_stats.gather_table_stats(
      3          ownname => 'DEV',
      4          tabname => 'bigtab',
      5          estimate_percent => dbms_stats.auto_sample_size,
      6          method_opt => 'for all columns size auto'
      7      );
      8  end;
      9  /

    PL/SQL procedure successfully completed.
    
create index on smalltab(table_name)

    SQL> create index smalltab_idx on dev.smalltab(table_name);

    Index created.
    
retest

    SQL> set timing on
    SQL> set autot on
    SQL> select count(1)
      2  from bigtab a,
      3       smalltab b
      4  where a.object_name = b.table_name
      5  /

      COUNT(1)
    ----------
        389961

    Elapsed: 00:00:01.46

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 998718878

    ---------------------------------------------------------------------------------------
    | Id  | Operation	       | Name	      | Rows  | Bytes | Cost (%CPU)| Time     |
    ---------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT       |	      |     1 |    45 | 30468	(1)| 00:06:06 |
    |   1 |  SORT AGGREGATE        |	      |     1 |    45 | 	   |	      |
    |*  2 |   HASH JOIN	       |	      |   527K|    22M| 30468	(1)| 00:06:06 |
    |   3 |    INDEX FAST FULL SCAN| SMALLTAB_IDX |  3157 | 63140 |     6	(0)| 00:00:01 |
    |   4 |    TABLE ACCESS FULL   | BIGTAB       |  7521K|   179M| 30438	(1)| 00:06:06 |
    ---------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("A"."OBJECT_NAME"="B"."TABLE_NAME")


    Statistics
    ----------------------------------------------------------
          1  recursive calls
          0  db block gets
         111909  consistent gets
         111891  physical reads
          0  redo size
        528  bytes sent via SQL*Net to client
        524  bytes received via SQL*Net from client
          2  SQL*Net roundtrips to/from client
          0  sorts (memory)
          0  sorts (disk)
          1  rows processed

create index on bigtab(object_name)
    
    SQL> create index bigtab_idx on dev.bigtab(object_name);

    Index created.

retest
    
    SQL> select count(1) 
      2  from bigtab a,
      3       smalltab b
      4  where a.object_name = b.table_name
      5  /

      COUNT(1)
    ----------
        389961

    Elapsed: 00:00:00.32

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 995607616

    ---------------------------------------------------------------------------------------
    | Id  | Operation	       | Name	      | Rows  | Bytes | Cost (%CPU)| Time     |
    ---------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT       |	      |     1 |    45 |  5766	(1)| 00:01:10 |
    |   1 |  SORT AGGREGATE        |	      |     1 |    45 | 	   |	      |
    |   2 |   NESTED LOOPS	       |	      |   527K|    22M|  5766	(1)| 00:01:10 |
    |   3 |    INDEX FAST FULL SCAN| SMALLTAB_IDX |  3157 | 63140 |     6	(0)| 00:00:01 |
    |*  4 |    INDEX RANGE SCAN    | BIGTAB_IDX   |   167 |  4175 |     2	(0)| 00:00:01 |
    ---------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       4 - access("A"."OBJECT_NAME"="B"."TABLE_NAME")


    Statistics
    ----------------------------------------------------------
          1  recursive calls
          0  db block gets
           7310  consistent gets
           3095  physical reads
          0  redo size
        528  bytes sent via SQL*Net to client
        524  bytes received via SQL*Net from client
          2  SQL*Net roundtrips to/from client
          0  sorts (memory)
          0  sorts (disk)
          1  rows processed
    
6) delele sql tuning advisor task record
    
    SQL> exec dbms_sqltune.drop_tuning_task('sql_tuning_advisor_test');
    
    PL/SQL procedure successfully completed.