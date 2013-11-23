---
layout: post
title: Oracle SQL Access Path Examples
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

##Init `SQL*Plus`

    SQL> set timing on
    SQL> set autot on exp
    SQL> set linesize 200

##Full Table Scan

    SQL> select count(1) from bigtab where owner='DEV';

      COUNT(1)
    ----------
          2827

    Elapsed: 00:00:01.85

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2140185107

    -----------------------------------------------------------------------------
    | Id  | Operation	   | Name   | Rows  | Bytes | Cost (%CPU)| Time     |
    -----------------------------------------------------------------------------
    |   0 | SELECT STATEMENT   |	    |	  1 |	  6 | 30445   (1)| 00:06:06 |
    |   1 |  SORT AGGREGATE    |	    |	  1 |	  6 |		 |	    |
    |*  2 |   TABLE ACCESS FULL| BIGTAB |	203K|  1191K| 30445   (1)| 00:06:06 |
    -----------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - filter("OWNER"='DEV')

##Rowid Scan   
   
    SQL> select rowid from bigtab where owner='DEV' and rownum <= 1;

    ROWID
    ------------------
    AAAXKzAAoAAAATVAA+

    Elapsed: 00:00:00.03

    SQL> select count(1) from bigtab where  rowid = 'AAAXKzAAoAAAATVAA+';

      COUNT(1)
    ----------
         1

    Elapsed: 00:00:00.01

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 989695095

    --------------------------------------------------------------------------------------
    | Id  | Operation		    | Name   | Rows  | Bytes | Cost (%CPU)| Time     |
    --------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT	    |	     |	   1 |	  12 |	   1   (0)| 00:00:01 |
    |   1 |  SORT AGGREGATE 	    |	     |	   1 |	  12 |		  |	     |
    |   2 |   TABLE ACCESS BY USER ROWID| BIGTAB |	   1 |	  12 |	   1   (0)| 00:00:01 |
    --------------------------------------------------------------------------------------

create non-unique index
    
    SQL> create index bigtab_idx on bigtab(owner);
    
    Elapsed: 00:00:17.00
    
    SQL> select count(1) from bigtab where owner='DEV';

      COUNT(1)
    ----------
          2827

    Elapsed: 00:00:00.00

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 397841597

    --------------------------------------------------------------------------------
    | Id  | Operation	  | Name       | Rows  | Bytes | Cost (%CPU)| Time     |
    --------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT  |	       |     1 |     6 |   480	 (1)| 00:00:06 |
    |   1 |  SORT AGGREGATE   |	       |     1 |     6 |	    |	       |
    |*  2 |   INDEX RANGE SCAN| BIGTAB_IDX |   203K|  1191K|   480	 (1)| 00:00:06 |
    --------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("OWNER"='DEV')

    SQL> select object_name from bigtab where owner='DEV';
    ... ... 
    Elapsed: 00:00:00.20

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 346967093

    ------------------------------------------------------------------------------------------
    | Id  | Operation		    | Name	 | Rows  | Bytes | Cost (%CPU)| Time	 |
    ------------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT	    |		 |   203K|  6154K|  6143   (1)| 00:01:14 |
    |   1 |  TABLE ACCESS BY INDEX ROWID| BIGTAB	 |   203K|  6154K|  6143   (1)| 00:01:14 |
    |*  2 |   INDEX RANGE SCAN	    | BIGTAB_IDX |   203K|	 |   480   (1)| 00:00:06 |
    ------------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("OWNER"='DEV')

    SQL> select owner from bigtab where owner='DEV';
    ... ...
    Elapsed: 00:00:00.04

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 3859841128

    -------------------------------------------------------------------------------
    | Id  | Operation	 | Name       | Rows  | Bytes | Cost (%CPU)| Time     |
    -------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT |	      |   203K|  1191K|   480	(1)| 00:00:06 |
    |*  1 |  INDEX RANGE SCAN| BIGTAB_IDX |   203K|  1191K|   480	(1)| 00:00:06 |
    -------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       1 - access("OWNER"='DEV')

##Index Scans

###Index Unique Scans

    SQL> select  * from smalltab where id = 1;
    ... ...
    Elapsed: 00:00:00.01

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2765411029

    ------------------------------------------------------------------------------
    | Id  | Operation	  | Name     | Rows  | Bytes | Cost (%CPU)| Time     |
    ------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT  |	     |	   1 |	 245 |	  35   (0)| 00:00:01 |
    |*  1 |  TABLE ACCESS FULL| SMALLTAB |	   1 |	 245 |	  35   (0)| 00:00:01 |
    ------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       1 - filter("ID"=1)

add primary key
       
    SQL> alter table smalltab add constraint smalltab_pk primary key (id);

    Table altered.

    Elapsed: 00:00:00.17
    SQL> select  * from smalltab where id = 1;
    ... ...
    Elapsed: 00:00:00.02

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 3259460393

    -------------------------------------------------------------------------------------------
    | Id  | Operation		    | Name	  | Rows  | Bytes | Cost (%CPU)| Time	  |
    -------------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT	    |		  |	1 |   245 |	2   (0)| 00:00:01 |
    |   1 |  TABLE ACCESS BY INDEX ROWID| SMALLTAB	  |	1 |   245 |	2   (0)| 00:00:01 |
    |*  2 |   INDEX UNIQUE SCAN	    | SMALLTAB_PK |	1 |	  |	1   (0)| 00:00:01 |
    -------------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("ID"=1)
       
create unique index

    SQL> alter table smalltab drop constraint smalltab_pk;

    Table altered.

    Elapsed: 00:00:00.08
    SQL> create unique index smalltab_idx on smalltab(id);

    Index created.

    Elapsed: 00:00:00.02
    
    SQL> select  * from smalltab where id = 1;
    ... ...
    Elapsed: 00:00:00.00

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 3320624552

    --------------------------------------------------------------------------------------------
    | Id  | Operation		    | Name	   | Rows  | Bytes | Cost (%CPU)| Time	   |
    --------------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT	    |		   |	 1 |   245 |	 2   (0)| 00:00:01 |
    |   1 |  TABLE ACCESS BY INDEX ROWID| SMALLTAB	   |	 1 |   245 |	 2   (0)| 00:00:01 |
    |*  2 |   INDEX UNIQUE SCAN	    | SMALLTAB_IDX |	 1 |	   |	 1   (0)| 00:00:01 |
    --------------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("ID"=1)

###Index Range Scans

    SQL> create index smalltab_owner_idx on smalltab(owner);

    Index created.

    Elapsed: 00:00:00.03
    
`=`
    
    SQL> select * from smalltab where owner = 'dev';

    no rows selected

    Elapsed: 00:00:00.00

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2274244531

    --------------------------------------------------------------------------------------------------
    | Id  | Operation		    | Name		 | Rows  | Bytes | Cost (%CPU)| Time	 |
    --------------------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT	    |			 |    48 | 11760 |     5   (0)| 00:00:01 |
    |   1 |  TABLE ACCESS BY INDEX ROWID| SMALLTAB		 |    48 | 11760 |     5   (0)| 00:00:01 |
    |*  2 |   INDEX RANGE SCAN	    | SMALLTAB_OWNER_IDX |    48 |	 |     1   (0)| 00:00:01 |
    --------------------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("OWNER"='dev')

`<`
       
    SQL> select * from smalltab where owner < 'abc';
    ... ...
    Elapsed: 00:00:12.26

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2765411029

    ------------------------------------------------------------------------------
    | Id  | Operation	  | Name     | Rows  | Bytes | Cost (%CPU)| Time     |
    ------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT  |	     |	3157 |	 755K|	  35   (0)| 00:00:01 |
    |*  1 |  TABLE ACCESS FULL| SMALLTAB |	3157 |	 755K|	  35   (0)| 00:00:01 |
    ------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       1 - filter("OWNER"<'abc')
  
`>`
  
    SQL> select * from smalltab where owner > 'abc';

    no rows selected

    Elapsed: 00:00:00.00

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2274244531

    --------------------------------------------------------------------------------------------------
    | Id  | Operation		    | Name		 | Rows  | Bytes | Cost (%CPU)| Time	 |
    --------------------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT	    |			 |    61 | 14945 |     7   (0)| 00:00:01 |
    |   1 |  TABLE ACCESS BY INDEX ROWID| SMALLTAB		 |    61 | 14945 |     7   (0)| 00:00:01 |
    |*  2 |   INDEX RANGE SCAN	    | SMALLTAB_OWNER_IDX |    61 |	 |     2   (0)| 00:00:01 |
    --------------------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("OWNER">'abc')
 
`like` 
 
    SQL> select * from smalltab where owner like 'abc%';

    no rows selected

    Elapsed: 00:00:00.01

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2274244531

    --------------------------------------------------------------------------------------------------
    | Id  | Operation		    | Name		 | Rows  | Bytes | Cost (%CPU)| Time	 |
    --------------------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT	    |			 |   102 | 24990 |    10   (0)| 00:00:01 |
    |   1 |  TABLE ACCESS BY INDEX ROWID| SMALLTAB		 |   102 | 24990 |    10   (0)| 00:00:01 |
    |*  2 |   INDEX RANGE SCAN	    | SMALLTAB_OWNER_IDX |   102 |	 |     2   (0)| 00:00:01 |
    --------------------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("OWNER" LIKE 'abc%')
           filter("OWNER" LIKE 'abc%')
       
    SQL> select * from smalltab where owner like '%abc';

    no rows selected

    Elapsed: 00:00:00.01

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2765411029

    ------------------------------------------------------------------------------
    | Id  | Operation	  | Name     | Rows  | Bytes | Cost (%CPU)| Time     |
    ------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT  |	     |	 158 | 38710 |	  35   (0)| 00:00:01 |
    |*  1 |  TABLE ACCESS FULL| SMALLTAB |	 158 | 38710 |	  35   (0)| 00:00:01 |
    ------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       1 - filter("OWNER" LIKE '%abc')
       
### Index Range Scans Descending

    SQL> select /*+index_desc(smalltab smalltab_owner_idx) */ count(1) from smalltab where owner = 'dev';

      COUNT(1)
    ----------
         0

    Elapsed: 00:00:00.01

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 3707260210

    ---------------------------------------------------------------------------------------------------
    | Id  | Operation		     | Name		  | Rows  | Bytes | Cost (%CPU)| Time	  |
    ---------------------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT	     |			  |	1 |	7 |	1   (0)| 00:00:01 |
    |   1 |  SORT AGGREGATE 	     |			  |	1 |	7 |	       |	  |
    |*  2 |   INDEX RANGE SCAN DESCENDING| SMALLTAB_OWNER_IDX |    48 |   336 |	1   (0)| 00:00:01 |
    ---------------------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("OWNER"='dev')
           filter("OWNER"='dev')

### Index Skip Scans

    SQL> create index smalltab_skip_idx on smalltab(owner, tablespace_name);

    Index created.

    Elapsed: 00:00:00.02

    SQL> select * from smalltab where tablespace_name = 'x' ;

    no rows selected

    Elapsed: 00:00:00.00

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2078826789

    -------------------------------------------------------------------------------------------------
    | Id  | Operation		    | Name		| Rows	| Bytes | Cost (%CPU)| Time	|
    -------------------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT	    |			|     1 |   245 |    33   (0)| 00:00:01 |
    |   1 |  TABLE ACCESS BY INDEX ROWID| SMALLTAB		|     1 |   245 |    33   (0)| 00:00:01 |
    |*  2 |   INDEX SKIP SCAN	    | SMALLTAB_SKIP_IDX |     1 |	|    32   (0)| 00:00:01 |
    -------------------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - access("TABLESPACE_NAME"='x')
           filter("TABLESPACE_NAME"='x')

### Full Scans

#### Fast Full Index Scans

    SQL> drop index smalltab_owner_idx;

    Index dropped.

    Elapsed: 00:00:00.02
    
    SQL> create index smalltab_ffs_idx on smalltab(owner,status);

    Index created.

    Elapsed: 00:00:00.03
    
    SQL> select count(1) from smalltab where status = 'VALID' ;

      COUNT(1)
    ----------
          3157

    Elapsed: 00:00:00.01

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2296131484

    -------------------------------------------------------------------------------------------
    | Id  | Operation	      | Name		  | Rows  | Bytes | Cost (%CPU)| Time	  |
    -------------------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT      | 		  |	1 |	6 |	5   (0)| 00:00:01 |
    |   1 |  SORT AGGREGATE       | 		  |	1 |	6 |	       |	  |
    |*  2 |   INDEX FAST FULL SCAN| SMALLTAB_FFS_IDX |  3157 | 18942 |	5   (0)| 00:00:01 |
    -------------------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       2 - filter("STATUS"='VALID')

## Index Joins

Todo ...

## Bitmap Indexes

Todo ...

## Cluster Access

## Hash Access

## Sample Table Scans

    SQL> select * from smalltab where owner = 'dev';

    no rows selected

    Elapsed: 00:00:00.00

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 2765411029

    ------------------------------------------------------------------------------
    | Id  | Operation	  | Name     | Rows  | Bytes | Cost (%CPU)| Time     |
    ------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT  |	     |	  48 | 11760 |	  35   (0)| 00:00:01 |
    |*  1 |  TABLE ACCESS FULL| SMALLTAB |	  48 | 11760 |	  35   (0)| 00:00:01 |
    ------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       1 - filter("OWNER"='dev')

    SQL> select * from smalltab sample block (1) where owner = 'dev';

    no rows selected

    Elapsed: 00:00:00.03

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 1616664914

    --------------------------------------------------------------------------------
    | Id  | Operation	    | Name     | Rows  | Bytes | Cost (%CPU)| Time     |
    --------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT    |	       |     1 |   245 |     2	 (0)| 00:00:01 |
    |*  1 |  TABLE ACCESS SAMPLE| SMALLTAB |     1 |   245 |     2	 (0)| 00:00:01 |
    --------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       1 - filter("OWNER"='dev')

    SQL> select * from smalltab sample block (10) where owner = 'dev';

    no rows selected

    Elapsed: 00:00:00.01

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 1616664914

    --------------------------------------------------------------------------------
    | Id  | Operation	    | Name     | Rows  | Bytes | Cost (%CPU)| Time     |
    --------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT    |	       |     5 |  1225 |     5	 (0)| 00:00:01 |
    |*  1 |  TABLE ACCESS SAMPLE| SMALLTAB |     5 |  1225 |     5	 (0)| 00:00:01 |
    --------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       1 - filter("OWNER"='dev')

    SQL> select * from smalltab sample block (10) where owner = 'DEV';

    no rows selected

    Elapsed: 00:00:00.00

    Execution Plan
    ----------------------------------------------------------
    Plan hash value: 1616664914

    --------------------------------------------------------------------------------
    | Id  | Operation	    | Name     | Rows  | Bytes | Cost (%CPU)| Time     |
    --------------------------------------------------------------------------------
    |   0 | SELECT STATEMENT    |	       |    10 |  2450 |     5	 (0)| 00:00:01 |
    |*  1 |  TABLE ACCESS SAMPLE| SMALLTAB |    10 |  2450 |     5	 (0)| 00:00:01 |
    --------------------------------------------------------------------------------

    Predicate Information (identified by operation id):
    ---------------------------------------------------

       1 - filter("OWNER"='DEV')
	   
##Reference

* Oracle Database Performance Tuning Guide