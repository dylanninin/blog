---
layout: post
title: Oracle Explain Plan Introduction
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

## Execution plan

To execute a SQL statement, Oracle Database may need to perform many steps. Each step either retrieves rows of data physically from the database or prepares them in some way for the user issuing the statement. The combination of the steps that Oracle Database uses to execute a statement is an execution plan. 

An execution plan includes an access path for each table that the statement accesses and an ordering of the tables (the join order) with the appropriate join method.

	PLAN_TABLE --> EXPLAIN PLAN FOR statement --> Displaying PLAN_TABLE Output

These are the basics of using the  EXPLAIN PLAN  statement:

* Use the SQL script  CATPLAN . SQL  to create a sample output table called  PLAN_TABLE in your schema. 
* Include the  EXPLAIN PLAN FOR  clause before the SQL statement. 
* After issuing the  EXPLAIN PLAN  statement, use one of the scripts or package provided by Oracle Database to display the most recent plan table output.
* The execution order in  EXPLAIN PLAN  output begins with the line that is the furthest indented to the right. The next step is the parent of that line. If two lines are indented equally, then the top line is normally executed first.

## Using EXPLAIN PLAN  

This chapter introduces execution plans, describes the SQL statement  `EXPLAIN PLAN` , and explains how to interpret its output. This chapter also provides procedures for managing outlines to control application performance characteristics. This chapter contains the following sections: 

* Understanding EXPLAIN PLAN
* The PLAN_TABLE Output Table
* Running EXPLAIN PLAN
* Displaying PLAN_TABLE Output
* Reading EXPLAIN PLAN Output
* Viewing Parallel Execution with EXPLAIN PLAN
* Viewing Bitmap Indexes with EXPLAIN PLAN
* Viewing Result Cache with EXPLAIN PLAN
* Viewing Partitioned Objects with EXPLAIN PLAN
* PLAN_TABLE Columns

### Understanding EXPLAIN PLAN

The  `EXPLAIN PLAN`  statement displays execution plans chosen by the optimizer for` SELECT` ,  `UPDATE` , `INSERT` , and  `DELETE`  statements. A statement execution plan is the sequence of operations that the database performs to run the statement. 

The row source tree is the core of the execution plan. The tree shows the following information:

* An ordering of the tables referenced by the statement
* An access method for each table mentioned in the statement
* A join method for tables affected by join operations in the statement
* Data operations like filter, sort, or aggregationUnderstanding EXPLAIN PLAN

In addition to the row source tree, the plan table contains information about the following:

* Optimization, such as the cost and cardinality of each operation
* Partitioning, such as the set of accessed partitions
* Parallel execution, such as the distribution method of join inputs

The  `EXPLAIN PLAN`  results let you determine whether the optimizer selects a particular execution plan, such as, nested loops join. The results also help you to understand the optimizer decisions, such as why the optimizer chose a nested loops join instead of a hash join, and lets you understand the performance of a query.

### How Execution Plans Can Change

With the query optimizer, execution plans can and do change as the underlying optimizer inputs change.  EXPLAIN PLAN  output shows how Oracle Database would run the SQL statement when the statement was explained. This plan can differ from the actual execution plan a SQL statement because of differences in the execution environment and explain plan environment

Different Schemas 

* The execution and explain plan occur on different databases.
* The user explaining the statement is different from the user running the statement. Two users might be pointing to different objects in the same database, resulting in different execution plans.
* Schema changes (usually changes in indexes) between the two operations.

Different Costs 

Even if the schemas are the same, the optimizer can choose different execution plans when the costs are different. Some factors that affect the costs include the following:

* Data volume and statistics
* Bind variable types and values
* Initialization parameters set globally or at session level

Minimizing Throw-Away

Examining an explain plan lets you look for throw-away in cases such as the following:

* Full scans
* Unselective range scans
* Late predicate filters
* Wrong join order
* Late filter operations

### Looking Beyond Execution Plans

The execution plan operation alone cannot differentiate between well-tuned statements and those that perform poorly. For example, an  EXPLAIN PLAN  output that shows that a statement uses an index does not necessarily mean that the statement runs efficiently. Sometimes indexes are extremely inefficient. In this case, you should examine the following:

* The columns of the index being used
* Their selectivity (fraction of table being accessed)

It is best to use  EXPLAIN PLAN  to determine an access plan, and then later prove that it is the optimal plan through testing. When evaluating a plan, examine the statement's actual resource consumption. 

## Using V$SQL_PLAN Views

In addition to running the  EXPLAIN PLAN  command and displaying the plan, you can use the  V$SQL_PLAN  views to display the execution plan of a SQL statement: After the statement has executed, you can display the plan by querying the  V$SQL_ PLAN  view.  V$SQL_PLAN  contains the execution plan for every statement stored in the shared SQL area.

The advantage of  V$SQL_PLAN  over  EXPLAIN PLAN  is that you do not need to know the compilation environment that was used to execute a particular statement. For  EXPLAIN PLAN , you would need to set up an identical environment to get the same plan when executing the statement.

The  V$SQL_PLAN_STATISTICS  view provides the actual execution statistics for every operation in the plan, such as the number of output rows and elapsed time. All statistics, except the number of output rows, are cumulative. For example, the statistics for a join operation also includes the statistics for its two inputs. The statistics in V$SQL_PLAN_STATISTICS  are available for cursors that have been compiled with the STATISTICS_LEVEL  initialization parameter set to  ALL .

The  V$SQL_PLAN_STATISTICS_ALL  view enables side by side comparisons of the estimates that the optimizer provides for the number of rows and elapsed time. This view combines both  V$SQL_PLAN  and  V$SQL_PLAN_STATISTICS  information for every cursor.

The  PLAN_TABLE  is automatically created as a public synonym to a global temporary table. This temporary table holds the output of  EXPLAIN PLAN  statements for all users. PLAN_TABLE  is the default sample output table into which the  EXPLAIN PLAN  statement inserts rows describing execution plans.

After you have explained the plan, use the following SQL scripts or PL/SQL package 
provided by Oracle Database to display the most recent plan table output:

* UTLXPLS.SQL : This script displays the plan table output for serial processing.

* UTLXPLP.SQL: This script displays the plan table output including parallel execution columns.

* DBMS_XPLAN.DISPLAY  table function: This function accepts options for displaying the plan table output. You can specify:

	* A plan table name if you are using a table different than  PLAN_TABLE
	* A statement ID if you have set a statement ID with the  EXPLAIN PLAN
	* A format option that determines the level of detail:  BASIC ,  SERIAL , and TYPICAL ,  ALL ,

Some examples of the use of  DBMS_XPLAN  to display  PLAN_TABLE  output are:

	SELECT PLAN_TABLE_OUTPUT FROM TABLE(DBMS_XPLAN.DISPLAY());
	
	SELECT PLAN_TABLE_OUTPUT FROM TABLE(DBMS_XPLAN.DISPLAY('MY_PLAN_TABLE', 'st1','TYPICAL'));
  

### Customizing PLAN_TABLE Output

If you have specified a statement identifier, then you can write your own script to query the  PLAN_TABLE . For example:

* Start with ID = 0 and given  STATEMENT_ID .
* Use the  CONNECT BY  clause to walk the tree from parent to child, the join keys being STATEMENT_ID  =  PRIOR STATEMENT_ID  and  PARENT_ID  =  PRIOR ID .
* Use the pseudo-column  LEVEL  (associated with  CONNECT BY ) to indent the children.

sql

	SELECT cardinality "Rows",
	   lpad(' ',level-1)||operation||' '||options||' '||object_name "Plan"
	  FROM PLAN_TABLE
	CONNECT BY prior id = parent_id AND prior statement_id = statement_id
	  START WITH id = 0 AND statement_id = 'st1'
	  ORDER BY id;
	   Rows Plan
	------- ----------------------------------------
			SELECT STATEMENT
			 TABLE ACCESS FULL EMPLOYEES
  
## Reference

* Oracle Database Performance Guide
