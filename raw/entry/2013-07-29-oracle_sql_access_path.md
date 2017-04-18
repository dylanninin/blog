---
layout: post
title: Oracle SQL Access Path Introduction
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

## Access Path

Access paths are ways in which data is retrieved from the database. In general, index access paths are useful for statements that retrieve a small subset of table rows, whereas full scans are more efficient when accessing a large portion of the table. Online transaction processing (OLTP) applications, which consist of short-running SQL statements with high selectivity, often are characterized by the use of index access paths. Decision support systems, however, tend to use partitioned tables and perform full scans of the relevant partitions. 

The query optimizer chooses an access path based on the following factors: 

* The available access paths for the statement
* The estimated cost of executing the statement, using each access path or combination of paths

To choose an access path, the optimizer first determines which access paths are available by examining the conditions in the statement's  WHERE  clause and its  FROM clause. The optimizer then generates a set of possible execution plans using available access paths and estimates the cost of each plan, using the statistics for the index, columns, and tables accessible to the statement. Finally, the optimizer chooses the execution plan with the lowest estimated cost. 

When choosing an access path, the query optimizer is influenced by the following:

* Optimizer Hints. You can instruct the optimizer to use a specific access path using a hint, except when the statement's  FROM  clause contains  `SAMPLE`  or  `SAMPLE BLOCK` . 
* Old Statistics. For example, if a table has not been analyzed since it was created, and if it has less than  `DB_FILE_MULTIBLOCK_READ_COUNT` blocks under the high water mark, then the optimizer thinks that the table is small and uses a full table scan. Review the  `LAST_ ANALYZED`  and  `BLOCKS`  columns in the  `ALL_TABLES` table to examine the statistics.

### Full Table Scans

This type of scan reads all rows from a table and filters out those that do not meet the selection criteria. During a full table scan, all blocks in the table that are under the high water mark are scanned. The high water mark indicates the amount of used space, or space that had been formatted to receive data. Each row is examined to determine whether it satisfies the statement's  `WHERE  clause`. 

When Oracle Database performs a full table scan, the blocks are read sequentially. Because the blocks are adjacent, the database can make I/O calls larger than a single block to speed up the process. The size of the read calls range from one block to the number of blocks indicated by the initialization parameter  `DB_FILE_MULTIBLOCK_READ_ COUNT` . Using multiblock reads, the database can perform a full table scan very efficiently. The database reads each block only once. 
 
Full table scans are cheaper than index range scans when accessing a large fraction of the blocks in a table. Full table scans can use larger I/O calls, and making fewer large I/O calls is cheaper than making many smaller calls.

### Rowid Scan

The rowid of a row specifies the data file and data block containing the row and the location of the row in that block. Locating a row by specifying its rowid is the fastest way to retrieve a single row, because the exact location of the row in the database is specified. 

To access a table by rowid, Oracle Database first obtains the rowids of the selected rows, either from the statement's  WHERE  clause or through an index scan of one or more of the table's indexes. Oracle Database then locates each selected row in the table based on its rowid. 

### Index Scans

In this method, a row is retrieved by traversing the index, using the indexed column values specified by the statement. An index scan retrieves data from an index based on the value of one or more columns in the index. To perform an index scan, Oracle Database searches the index for the indexed column values accessed by the statement. If the statement accesses only columns of the index, then Oracle Database reads the indexed column values directly from the index, rather than from the table. 

The index contains not only the indexed value, but also the rowids of rows in the table having that value. Therefore, if the statement accesses other columns in addition to the indexed columns, then Oracle Database can find the rows in the table by using either a table access by rowid or a cluster scan. 

In this method, a row is retrieved by traversing the index, using the indexed column values specified by the statement. An index scan retrieves data from an index based on the value of one or more columns in the index. To perform an index scan, Oracle Database searches the index for the indexed column values accessed by the statement. If the statement accesses only columns of the index, then Oracle Database reads the indexed column values directly from the index, rather than from the table. 

The index contains not only the indexed value, but also the rowids of rows in the table having that value. Therefore, if the statement accesses other columns in addition to the indexed columns, then Oracle Database can find the rows in the table by using either a table access by rowid or a cluster scan. 

* Assessing I/O for Blocks, not Rows
* Index Unique Scans
* Index Range Scans
* Index Range Scans Descending
* Index Skip Scans
* Full Scans
* Fast Full Index Scans
* Index Joins
* Bitmap Indexes

#### I/O Blocks

Oracle Database performs I/O by blocks. Therefore, the optimizer's decision to use full table scans is influenced by the percentage of blocks accessed, not rows. This is called the index clustering factor. If blocks contain single rows, then rows accessed and blocks accessed are the same.

However, most tables have multiple rows in each block. Consequently, the desired number of rows may be clustered in a few blocks or spread out over a larger number of blocks.
 
Although the clustering factor is a property of the index, the clustering factor actually relates to the spread of similar indexed column values within data blocks in the table.
 
A lower clustering factor indicates that the individual rows are concentrated within fewer blocks in the table. Conversely, a high clustering factor indicates that the individual rows are scattered more randomly across blocks in the table. Therefore, a high clustering factor means that it costs more to use a range scan to fetch rows by rowid, because more blocks in the table need to be visited to return the data. 

#### Index Unique Scans

This scan returns, at most, a single rowid. Oracle Database performs a unique scan if a statement contains a  `UNIQUE`  or a  `PRIMARY KEY`  constraint that guarantees that only a single row is accessed. The database uses this access path when the user specifies all columns of a unique (B-tree) index or an index created as a result of a primary key constraint with equality conditions.

#### Index Range Scans

An index range scan is a common operation for accessing selective data. It can be bounded (bounded on both sides) or unbounded (on one or both sides). Data is returned in the ascending order of index columns. Multiple rows with identical values are sorted in ascending order by rowid.

If you require the data to be sorted by order, then use the  ORDER BY  clause, and do not rely on an index. If an index can satisfy an  ORDER BY  clause, then the optimizer uses this option and avoids a sort. The optimizer uses a range scan when it finds one or more leading columns of an index specified in conditions

#### Index Skip Scans

Index skip scans improve index scans by nonprefix columns. Often, scanning index blocks is faster than scanning table data blocks.

Skip scanning lets a composite index be split logically into smaller subindexes. In skip scanning, the initial column of the composite index is not specified in the query. In other words, it is skipped.

The database determines the number of logical subindexes by the number of distinct values in the initial column. Skip scanning is advantageous when there are few distinct values in the leading column of the composite index and many distinct values in the nonleading key of the index.

#### Full Scans

A full index scan eliminates a sort operation, because the data is ordered by the index key. It reads the blocks singly. Oracle Database may use a full scan in any of the following situations:

An  ORDER BY  clause that meets the following requirements is present in the query:

* All of the columns in the  ORDER BY  clause must be in the index.
* The order of the columns in the  ORDER BY  clause must match the order of the leading index columns.

The  ORDER BY  clause can contain all of the columns in the index or a subset of the 	columns in the index. 
	
The query requires a sort merge join. The database can perform a full index scan instead of doing a full table scan followed by a sort when the query meets the following requirements:

* All of the columns referenced in the query must be in the index.
* The order of the columns referenced in the query must match the order of the leading index columns.

The query can contain all of the columns in the index or a subset of the columns in the index.

* A  GROUP BY  clause is present in the query, and the columns in the  GROUP BY  clause are present in the index. The columns do not need to be in the same order in the index and the  GROUP BY  clause. The  GROUP BY  clause can contain all of the columns in the index or a subset of the columns in the index.

#### Index Joins

An index join is a hash join of several indexes that together contain all the table columns referenced in the query. If the database uses an index join, then table access is not needed because the database can retrieve all the relevant column values from the indexes. The database cannot use an index join cannot to eliminate a sort operation. 

#### Bitmap Indexes

A bitmap join uses a bitmap for key values and a mapping function that converts each bit position to a rowid. Bitmaps can efficiently merge indexes that correspond to several conditions in a  WHERE  clause, using Boolean operations to resolve  AND  and  OR conditions.

#### Cluster Access

The database uses a cluster scan to retrieve all rows that have the same cluster key value from a table stored in an indexed cluster. In an indexed cluster, the database stores all rows with the same cluster key value in the same data block. To perform a cluster scan, Oracle Database first obtains the rowid of one of the selected rows by scanning the cluster index. Oracle Database then locates the rows based on this rowid. 

#### Hash Access

The database uses a hash scan to locate rows in a hash cluster based on a hash value. In a hash cluster, all rows with the same hash value are stored in the same data block. To perform a hash scan, Oracle Database first obtains the hash value by applying a hash function to a cluster key value specified by the statement. Oracle Database then scans the data blocks containing rows with that hash value. 

#### Sample Table Scans

A sample table scan retrieves a random sample of data from a simple table or a complex  `SELECT  statement`, such as a statement involving joins and views. The database uses this access path when a statement's  `FROM  clause` includes the  `SAMPLE clause` or the  `SAMPLE BLOCK  clause`. To perform a sample table scan when sampling by rows with the  `SAMPLE  clause`, the database reads a specified percentage of rows in the table. To perform a sample table scan when sampling by blocks with the  `SAMPLE BLOCK clause`, the database reads a specified percentage of table blocks. 

## Reference

* Oracle Database Performance Tuning Guide