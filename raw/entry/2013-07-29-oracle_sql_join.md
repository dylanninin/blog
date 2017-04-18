---
layout: post
title: Oracle SQL Join Introduction
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

## Joins

Joins are statements that retrieve data from multiple tables. A join is characterized by multiple tables in the  FROM  clause. The existence of a join condition in the  WHERE  clause defines the relationship between the tables. In a join, one row set is called inner, and the other is called outer.

To choose an execution plan for a join statement, the optimizer must make these interrelated decisions:
* Access Paths. As for simple statements, the optimizer must choose an access path to retrieve data from each table in the join statement. 
* Join Method. To join each pair of row sources, Oracle Database must perform a join operation. Join methods include nested loop, sort merge, cartesian, and hash joins.
* Join Order. To execute a statement that joins more than two tables, Oracle Database joins two of the tables and then joins the resulting row source to the next table. This process continues until all tables are joined into the result. 


How the Query Optimizer Chooses Execution Plans for Joins

The query optimizer considers the following when choosing an execution plan: 

* The optimizer first determines whether joining two or more tables definitely results in a row source containing at most one row. The optimizer recognizes such situations based on  UNIQUE  and  PRIMARY KEY  constraints on the tables. If such a situation exists, then the optimizer places these tables first in the join order. The optimizer then optimizes the join of the remaining set of tables. 
* For join statements with outer join conditions, the table with the outer join operator must come after the other table in the condition in the join order. The optimizer does not consider join orders that violate this rule. Similarly, when a subquery has been converted into an antijoin or semijoin, the tables from the subquery must come after those tables in the outer query block to which they were connected or correlated. However, hash antijoins and semijoins are able to override this ordering condition in certain circumstances.

With the query optimizer, the optimizer generates a set of execution plans, according to possible join orders, join methods, and available access paths. The optimizer then estimates the cost of each plan and chooses the one with the lowest cost. The optimizer estimates costs in the following ways: 

* The cost of a nested loops operation is based on the cost of reading each selected row of the outer table and each of its matching rows of the inner table into memory. The optimizer estimates these costs using the statistics in the data dictionary. 
* The cost of a sort merge join is based largely on the cost of reading all the sources into memory and sorting them. 
* The cost of a hash join is based largely on the cost of building a hash table on one of the input sides to the join and using the rows from the other of the join to probe it.

The optimizer also considers other factors when determining the cost of each operation. For example: 

* A smaller sort area size is likely to increase the cost for a sort merge join because sorting takes more CPU time and I/O in a smaller sort area.
* A larger multiblock read count is likely to decrease the cost for a sort merge join in relation to a nested loop join. If the database can read a large number of sequential blocks from disk in a single I/O, then an index on the inner table for the nested loop join is less likely to improve performance over a full table scan. The multiblock read count is specified by the initialization parameter  DB_FILE_ MULTIBLOCK_READ_COUNT . 

You can use the  ORDERED  hint to override the optimizer's choice of join orders. If the ORDERED  hint specifies a join order that violates the rule for an outer join, then the optimizer ignores the hint and chooses the order. Also, you can override the optimizer's choice of join method with hints. 

## Nested Loop Joins

Nested loop joins are useful when the following conditions are true:

* The database joins small subsets of data.
* The join condition is an efficient method of accessing the second table.

It is important to ensure that the inner table is driven from (dependent on) the outer table. If the inner table's access path is independent of the outer table, then the same rows are retrieved for every iteration of the outer loop, degrading performance considerably. In such cases, hash joins joining the two independent row sources perform better.

A nested loop join involves the following steps:

* The optimizer determines the driving table and designates it as the outer table.
* The other table is designated as the inner table.
* For every row in the outer table, Oracle Database accesses all the rows in the inner table. The outer loop is for every row in the outer table and the inner loop is for every row in the inner table. The outer loop appears before the inner loop in the execution plan, as follows:

    NESTED LOOPS 
    outer_loop
    inner_loop
    
When the Optimizer Uses Nested Loop Joins

The optimizer uses nested loop joins when joining small number of rows, with a good driving condition between the two tables. You drive from the outer loop to the inner loop, so the order of tables in the execution plan is important.

The outer loop is the driving row source. It produces a set of rows for driving the join condition. The row source can be a table accessed using an index scan or a full table scan. Also, the rows can be produced from any other operation. For example, the output from a nested loop join can serve as a row source for another nested loop join.

The inner loop is iterated for every row returned from the outer loop, ideally by an index scan. If the access path for the inner loop is not dependent on the outer loop, then you can end up with a Cartesian product; for every iteration of the outer loop, the inner loop produces the same set of rows. Therefore, you should use other join methods when two independent row sources are joined together.

## Hash Joins

The database uses hash joins to join large data sets. The optimizer uses the smaller of two tables or data sources to build a hash table on the join key in memory. It then scans the larger table, probing the hash table to find the joined rows.

This method is best when the smaller table fits in available memory. The cost is then limited to a single read pass over the data for the two tables.

When the Optimizer Uses Hash Joins

The optimizer uses a hash join to join two tables if they are joined using an equijoin and if either of the following conditions are true:

* A large amount of data must be joined.
* A large fraction of a small table must be joined.

## Sort Merge Joins

Sort merge joins can join rows from two independent sources. Hash joins generally perform better than sort merge joins. However, sort merge joins can perform better than hash joins if both of the following conditions exist:

* The row sources are sorted already.
* A sort operation does not have to be done.

However, if a sort merge join involves choosing a slower access method (an index scan as opposed to a full table scan), then the benefit of using a sort merge might be lost. Sort merge joins are useful when the join condition between two tables is an inequality condition such as  < ,  <= ,  > , or  >= . Sort merge joins perform better than nested loop joins for large data sets. You cannot use hash joins unless there is an equality condition. In a merge join, there is no concept of a driving table. The join consists of two steps:

* Sort join operation: Both the inputs are sorted on the join key.
* Merge join operation: The sorted lists are merged together.

If the input is sorted by the join column, then a sort join operation is not performed for that row source. However, a sort merge join always creates a positionable sort buffer for the right side of the join so that it can seek back to the last match in the case where duplicate join key values come out of the left side of the join.

When the Optimizer Uses Sort Merge Joins

The optimizer can choose a sort merge join over a hash join for joining large amounts of data if any of the following conditions are true:

* The join condition between two tables is not an equijoin.
* Because of sorts required by other operations, the optimizer finds it is cheaper to use a sort merge than a hash join.

Sort Merge Join Hints

To instruct the optimizer to use a sort merge join, apply the  USE_MERGE  hint. You might also need to give hints to force an access path. 

There are situations where it makes sense to override the optimizer with the  USE_ MERGE  hint. For example, the optimizer can choose a full scan on a table and avoid a sort operation in a query. However, there is an increased cost because a large table is accessed through an index and single block reads, as opposed to faster access through a full table scan.

## Cartesian Joins

The database uses a Cartesian join when one or more of the tables does not have any join conditions to any other tables in the statement. The optimizer joins every row from one data source with every row from the other data source, creating the Cartesian product of the two sets.

When the Optimizer Uses Cartesian Joins

The optimizer uses Cartesian joins when it is asked to join two tables with no join conditions. In some cases, a common filter condition between the two tables could be picked up by the optimizer as a possible join condition. In other cases, the optimizer may decide to generate a Cartesian product of two very small tables that are both joined to the same large table.

Cartesian Join Hints

Applying the  ORDERED  hint, instructs the optimizer to use a Cartesian join. By specifying a table before its join table is specified, the optimizer does a Cartesian join. 

## Outer Joins

An outer join extends the result of a simple join. An outer join returns all rows that satisfy the join condition and also returns some or all of those rows from one table for which no rows from the other satisfy the join condition.

Nested Loop Outer Joins

The database uses this operation to loop through an outer join between two tables. The outer join returns the outer (preserved) table rows, even when no corresponding rows are in the inner (optional) table. 

In a regular outer join, the optimizer chooses the order of tables (driving and driven) based on the cost. However, in a nested loop outer join, the join condition determines the order of tables. The database uses the outer table, with rows that are being preserved, to drive to the inner table.

The optimizer uses nested loop joins to process an outer join in the following circumstances:

* It is possible to drive from the outer table to inner table.
* Data volume is low enough to make the nested loop method efficient.

## Reference

* Oracle Database Performance Tuning Guide