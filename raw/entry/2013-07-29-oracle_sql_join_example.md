---
layout: post
title: Oracle SQL Join Examples
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

Create tables

    SQL> create table smalltab as select * from user_tables;

    Table created.

    Elapsed: 00:00:00.27

    SQL> create table bigtab as select * from dba_objects;

    Table created.

    Elapsed: 00:00:00.96
    SQL> insert into bigtab select * from dba_objects;

    74472 rows created.

    Commit complete.
    Elapsed: 00:00:00.83
    
Nested Loops
    
    SQL> select count(1)
      2  from smalltab a,
      3       smalltab b
      4  where a.table_name = b.table_name;

      COUNT(1)
    ----------
         4

    Elapsed: 00:00:00.00

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 3911555197

    -----------------------------------------------------------------------------------
    | Id  | Operation	   | Name	  | Rows  | Bytes | Cost (%CPU)| Time	  |
    -----------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT   |		  |	1 |    34 |	1   (0)| 00:00:01 |
    |   1 |  SORT AGGREGATE    |		  |	1 |    34 |	       |	  |
    |   2 |   NESTED LOOPS	   |		  |	4 |   136 |	1   (0)| 00:00:01 |
    |   3 |    INDEX FULL SCAN | SMALLTAB_IDX |	4 |    68 |	1   (0)| 00:00:01 |
    |*  4 |    INDEX RANGE SCAN| SMALLTAB_IDX |	1 |    17 |	0   (0)| 00:00:01 |
    -----------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       4 - access("A"."TABLE_NAME"="B"."TABLE_NAME")
       
Hash Join

    SQL> select count(1)
      2  from smalltab s,
      3       bigtab b
      4  where s.table_name = b.object_name;

      COUNT(1)
    ----------
         7

    Elapsed: 00:00:00.03

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 178863919

    ------------------------------------------------------------------------------------
    | Id  | Operation	    | Name	   | Rows  | Bytes | Cost (%CPU)| Time	   |
    ------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT    |		   |	 1 |	83 |   298   (1)| 00:00:04 |
    |   1 |  SORT AGGREGATE     |		   |	 1 |	83 |		|	   |
    |*  2 |   HASH JOIN	    |		   |	50 |  4150 |   298   (1)| 00:00:04 |
    |   3 |    INDEX FULL SCAN  | SMALLTAB_IDX |	 4 |	68 |	 1   (0)| 00:00:01 |
    |   4 |    TABLE ACCESS FULL| BIGTAB	   | 65625 |  4229K|   297   (1)| 00:00:04 |
    ------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("S"."TABLE_NAME"="B"."OBJECT_NAME")
	   
## Reference

* Oracle Database Performance Tuning Guide