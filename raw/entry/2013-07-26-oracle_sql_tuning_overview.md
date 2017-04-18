---
layout: post
title: Oracle SQL Tuning Overview
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

## Introduction to SQL Tuning

SQL tuning involves the following basic steps:

* Identifying high load or top SQL statements that are responsible for a large share of the application workload and system resources, by reviewing past SQL execution history available in the system
* Verifying that the execution plans produced by the query optimizer for these statements perform reasonably
* Implementing corrective actions to generate better execution plans for poorly performing SQL statements

The previous steps are repeated until the system performance reaches a satisfactory level or no more statements can be tuned.


## Goals

* Reduce the workload. SQL tuning commonly involves finding more efficient ways to process the same workload. It is possible to change the execution plan of the statement without altering the functionality to reduce the resource consumption

* Balance the Workload. Systems often tend to have peak usage in the daytime when real users are connected to the system, and low usage in the nighttime. If you can schedule noncritical reports and batch jobs to run in the nighttime and reduce their concurrency during day time, then the database frees up resources for the more critical programs in the day.

* Parallelize the Workload. Queries that access large amounts of data (typical data warehouse queries) can often run in parallel. Parallelism is extremely useful for reducing response time in a low concurrency data warehouse. However, for OLTP environments, which tend to be high concurrency, parallelism can adversely impact other users by increasing the overall resource usage of the program.


## Identifying High-Load SQL

This section describes the steps involved in identifying and gathering data on high-load SQL statements. High-load SQL are poorly-performing, resource-intensive SQL statements that impact the performance of an Oracle database. The following tools can identify high-load SQL statements:

* Automatic Database Diagnostic Monitor
* Automatic SQL tuning
* Automatic Workload Repository
* V$SQL  view
* Custom Workload
* SQL Trace

### Identifying Resource-Intensive SQL

#### Tuning a Specific Program.

If you are tuning a specific program (GUI or 3GL), then identifying the SQL to examine is a simple matter of looking at the SQL executed within the program. Oracle Enterprise Manager (Enterprise Manager) provides tools for identifying resource intensive SQL statements, generating explain plans, and evaluating SQL performance. If it is not possible to identify the SQL (for example, the SQL is generated dynamically), then use  SQL_TRACE  to generate a trace file that contains the SQL executed, then use  TKPROF  to generate an output file.

The SQL statements in the  TKPROF  output file can be ordered by various parameters, such as the execution elapsed time ( exeela ), which usually assists in the identification by ordering the SQL statements by elapsed time (with highest elapsed time SQL statements at the top of the file). This makes the job of identifying the poorly performing SQL easier if there are many SQL statements in the file.

#### Tuning an Application / Reducing Load.

If the whole application is performing poorly, or if you are attempting to reduce the overall CPU or I/O load on the database server, then identifying resource-intensive SQL involves the following steps:

* Determine which period in the day you would like to examine; typically this is the application's peak processing time.
* Gather operating system and Oracle Database statistics at the beginning and end of that period. The minimum of Oracle Database statistics gathered should be file I/O ( V$FILESTAT ), system statistics ( V$SYSSTAT ), and SQL statistics ( V$SQLAREA , V$SQL , or  V$SQLSTATS ,  V$SQLTEXT ,  V$SQL_PLAN , and  V$SQL_PLAN_STATISTICS ).
* Using the data collected in step two, identify the SQL statements using the most resources. A good way to identify candidate SQL statements is to query V$SQLSTATS .  V$SQLSTATS  contains resource usage information for all SQL statements in the shared pool. The data in  V$SQLSTATS  should be ordered by resource usage. The most common resources are: 

	* Buffer gets ( V$SQLSTATS . BUFFER_GETS , for high CPU using statements) 
	* Disk reads ( V$SQLSTATS . DISK_READS , for high I/O statements) 
	* Sorts ( V$SQLSTATS . SORTS , for many sorts)

One method to identify which SQL statements are creating the highest load is to compare the resources used by a SQL statement to the total amount of that resource used in the period. For  BUFFER_GETS , divide each SQL statement's  BUFFER_GETS  by the total number of buffer gets during the period. The total number of buffer gets in the system is available in the  V$SYSSTAT  table, for the statistic session logical reads. Similarly, it is possible to apportion the percentage of disk reads a statement performs out of the total disk reads performed by the system by dividing  V$SQL_STATS.DISK_ READS  by the value for the  V$SYSSTAT  statistic physical reads. The SQL sections of the Automatic Workload Repository report include this data, so you do not need to 
perform the percentage calculations manually.


### Gathering Data on the SQL Identified

If you are most concerned with CPU, then examine the top SQL statements that performed the most  BUFFER_GETS  during that interval. Otherwise, start with the SQL statement that performed the most  DISK_READS .

#### Information to Gather During Tuning

The tuning process begins by determining the structure of the underlying tables and indexes. The information gathered includes the following:

* Complete SQL text from  V$SQLTEXT
* Structure of the tables referenced in the SQL statement, usually by describing the table in `SQL*Plus`
* Definitions of any indexes (columns, column orders), and whether the indexes are unique or non-unique
* Optimizer statistics for the segments (including the number of rows each table, selectivity of the index columns), including the date when the segments were last analyzed
* Definitions of any views referred to in the SQL statement
* Repeat steps two, three, and four for any tables referenced in the view definitions 
* Optimizer plan for the SQL statement (either from  EXPLAIN PLAN ,  V$SQL_PLAN , or the  TKPROF  output)
* Any previous optimizer plans for that SQL statement

Note:

It is important to generate and review execution plans for all of the key SQL statements in your application. Doing so lets you compare the optimizer execution plans of a SQL statement when the statement performed well to the plan when that the statement is not performing well. Having the comparison, along with information such as changes in data volumes, can assist in identifying the cause of performance degradation.


## Automatic SQL Tuning Features

Because the manual SQL tuning process poses many challenges to the application developer, the SQL tuning process has been automated by the automatic SQL tuning features of Oracle Database. These features are designed to work equally well for OLTP and Data Warehouse type applications:

* ADDM
* SQL Tuning Advisor
* SQL Tuning Sets
* SQL Access Advisor

The Automatic Database Diagnostic Monitor (ADDM) analyzes the information collected by the AWR for possible performance problems with Oracle Database, including high-load SQL statements.

SQL Tuning Advisor optimizes SQL statements that have been identified as high-load SQL statements. By default, Oracle Database automatically identifies problematic SQL statements and implements tuning recommendations using SQL Tuning Advisor during system maintenance windows as an automated maintenance task, searching for ways to improve the execution plans of the high-load SQL statements. You can also choose to run SQL Tuning Advisor at any time on any given SQL workload to improve performance.

When multiple SQL statements serve as input to ADDM, SQL Tuning Advisor, or SQL Access Advisor, the database constructs and stores a SQL tuning set (STS). The STS includes the set of SQL statements along with their associated execution context and basic execution statistics.

In addition to SQL Tuning Advisor, SQL Access Advisor provides advice on materialized views, indexes, and materialized view logs. SQL Access Advisor helps you achieve performance goals by recommending the proper set of materialized views, materialized view logs, and indexes for a given workload. In general, as the number of materialized views and indexes and the space allocated to them is increased, query performance improves. SQL Access Advisor considers the trade-offs between space usage and query performance, and recommends the most cost-effective configuration of new and existing materialized views and indexes.

## Developing Efficient SQL Statements

This section describes ways you can improve SQL statement efficiency:

* Verifying Optimizer Statistics
* Reviewing the Execution Plan
* Restructuring the SQL Statements
* Restructuring the Indexes
* Modifying or Disabling Triggers and Constraints
* Restructuring the Data
* Maintaining Execution Plans Over Time
* Visiting Data as Few Times as Possible

### Verifying Optimizer Statistics

The query optimizer uses statistics gathered on tables and indexes when determining the optimal execution plan. If these statistics have not been gathered, or if the statistics are no longer representative of the data stored within the database, then the optimizer does not have sufficient information to generate the best plan. Things to check:

* If you gather statistics for some tables in your database, then it is probably best to gather statistics for all tables. This is especially true if your application includes SQL statements that perform joins.

* If the optimizer statistics in the data dictionary are no longer representative of the data in the tables and indexes, then gather new statistics. One way to check whether the dictionary statistics are stale is to compare the real cardinality (row count) of a table to the value of  DBA_TABLES.NUM_ROWS . Additionally, if there is significant data skew on predicate columns, then consider using histograms.

### Reviewing the Execution Plan

When tuning (or writing) a SQL statement in an OLTP environment, the goal is to drive from the table that has the most selective filter. This means that there are fewer rows passed to the next step. If the next step is a join, then this means that fewer rows are joined. Check to see whether the access paths are optimal.

When examining the optimizer execution plan, look for the following:

* The driving table has the best filter.
* The join order in each step returns the fewest number of rows to the next step (that is, the join order should reflect, where possible, going to the best not-yet-used filters).
* The join method is appropriate for the number of rows being returned. For example, nested loop joins through indexes may not be optimal when the statement returns many rows.
* The database uses views efficiently. Look at the  SELECT  list to see whether access to the view is necessary.
* There are any unintentional Cartesian products (even with small tables).
* Each table is being accessed efficiently: Consider the predicates in the SQL statement and the number of rows in the table. Look for suspicious activity, such as a full table scans on tables with large number of rows, which have predicates in the where clause. Determine why an index is not used for such a selective predicate.A full table scan does not mean inefficiency. It might be more efficient to perform a full table scan on a small table, or to perform a full table scan to leverage a better join method (for example, hash_join) for the number of rows returned. If any of these conditions are not optimal, then consider restructuring the SQL statement or the indexes available on the tables.

#### Restructuring the SQL Statements

Often, rewriting an inefficient SQL statement is easier than modifying it. If you understand the purpose of a given statement, then you might be able to quickly and easily write a new statement that meets the requirement.

* Compose Predicates Using AND and =
* To improve SQL efficiency, use equijoins whenever possible. Statements that perform equijoins on untransformed column values are the easiest to tune. 
* Avoid Transformed Columns in the WHERE Clause
* Write Separate SQL Statements for Specific Tasks. SQL is not a procedural language. Using one piece of SQL to do many different things usually results in a less-than-optimal result for each task. If you want SQL to accomplish different things, then write various statements, rather than writing one statement to do different things depending on the parameters you give it. 

#### Controlling the Access Path and Join Order with Hints

You can influence the optimizer's choices by setting the optimizer approach and goal, and by gathering representative statistics for the query optimizer. Sometimes, the application designer, who has more information about a particular application's data than is available to the optimizer, can choose a more effective way to execute a SQL statement. You can use hints in SQL statements to instruct the optimizer about how the statement should be executed. 

Join order can have a significant effect on performance. The main objective of SQL tuning is to avoid performing unnecessary work to access rows that do not affect the result. This leads to three general rules:
* Avoid a full-table scan if it is more efficient to get the required rows through an index.
* Avoid using an index that fetches 10,000 rows from the driving table if you could instead use another index that fetches 100 rows.
* Choose the join order so as to join fewer rows to tables later in the join order.

Filter conditions dominate the choice of driving table and index. In general, the driving table is the one containing the filter condition that eliminates the highest percentage of the table. 

#### Restructuring the Indexes 

Often, there is a beneficial impact on performance by restructuring indexes. This can involve the following:

* Remove nonselective indexes to speed the DML.
* Index performance-critical access paths.
* Consider reordering columns in existing concatenated indexes.
* Add columns to the index to improve selectivity.

 Do not use indexes as a panacea. Application developers sometimes think that performance improves when they create more indexes. If a single programmer creates an appropriate index, then this index may improve the application's performance. However, if 50 developers each create an index, then application performance will probably be hampered.

#### Modifying or Disabling Triggers and Constraints

Using triggers consumes system resources. If you use too many triggers, then performance may be adversely affected. In this case, you might need to modify or disable the triggers. 

#### Restructuring the Data

After restructuring the indexes and the statement, consider restructuring the data:
* Introduce derived values. Avoid  GROUP BY  in response-critical code.
* Review your data design. Change the design of your system if it can improve performance.

#### Maintaining Execution Plans Over Time

You can maintain the existing execution plan of SQL statements over time either using stored statistics or SQL plan baselines. Storing optimizer statistics for tables will apply to all SQL statements that refer to those tables. Storing an execution plan as a SQL plan baseline maintains the plan for set of SQL statements. If both statistics and a SQL plan baseline are available for a SQL statement, then the optimizer first uses a cost-based search method to build a best-cost plan, and then tries to find a matching plan in the SQL plan baseline. If a match is found, then the optimizer proceeds using this plan. Otherwise, it evaluates the cost of each of the accepted plans in the SQL plan baseline and selects the plan with the lowest cost.

#### Visiting Data as Few Times as Possible 

Applications should try to access each row only once. This reduces network traffic and reduces database load. Consider doing the following:

* Combine Multiples Scans Using CASE Expressions
* Use DML with RETURNING Clause
* Modify All the Data Needed in One Statement


## Building SQL Test Cases

For many SQL-related problems, obtaining a reproducible test case makes it easier to resolve the problem. Starting with the 11g Release 2 (11.2), Oracle Database contains the SQL Test Case Builder, which automates the somewhat difficult and time-consuming process of gathering and reproducing as much information as possible about a problem and the environment in which it occurred.

SQL Test Case Builder captures information pertaining to a SQL-related problem, along with the exact environment under which the problem occurred, so that you can reproduce and test the problem on a separate database. After the test case is ready, you can upload the problem to Oracle Support to enable support personnel to reproduce and troubleshoot the problem.

The information gathered by SQL Test Case Builder includes the query being executed, table and index definitions (but not the actual data), PL/SQL functions, procedures, and packages, optimizer statistics, and initialization parameter settings.

## Reference

* Oracle Database Performance Tuning Guide