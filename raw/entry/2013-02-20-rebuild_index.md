---
layout: post
title: Rebuild Indexes
category : Oracle
tags : [Oracle, Database, DBA, Exception]
---

## 异常日志

警告日志

	Wed Feb 20 11:00:20 2013
	GATHER_STATS_JOB encountered errors.  Check the trace file.
	Errors in file /db/oracle/diag/rdbms/dbtest/DBTEST/trace/DBTEST_j000_21813.trc:
	ORA-20000: index "BARCODE"."BC_BOXES_I"  or partition of such index is in unusable state

在执行`GATHER_STATS_JOB`任务时，检查到索引 `"BARCODE"."BC_BOXES_I"`存在异常，状态为`unusable`。

跟踪日志：

	ORA-20000: index "BARCODE"."BC_BOXES_I"  or partition of such index is in unusable state
	
	*** 2013-02-20 11:00:20.158
	GATHER_STATS_JOB: GATHER_TABLE_STATS('"BARCODE"','"BC_BOXES"','""', ...)
	ORA-20000: index "BARCODE"."BC_BOXES_I"  or partition of such index is in unusable state

在跟踪日志文件中，可以看到同样的错误信息。

## 异常确认

检查索引状态：

	SELECT C.INDEX_NAME,
	       I.UNIQUENESS,
	       C.COLUMN_NAME,
	       C.COLUMN_POSITION,
	       I.STATUS
	  FROM DBA_IND_COLUMNS C, DBA_INDEXES I
	 WHERE I.INDEX_NAME = C.INDEX_NAME
	   AND I.OWNER = 'BARCODE'
	  9   ORDER BY C.INDEX_NAME, C.COLUMN_POSITION;
	
	INDEX_NAME	     UNIQUENESS  COLUMN_NAME	COLUMN_POSITION STATUS
	--------------- 	------------ -------------- --------------- ----------
	BC_BOXES_I	     NONUNIQUE	 BOX_NUMBER 				1 UNUSABLE
	ITEM_MODEL_I	 NONUNIQUE	 MODEL						1 VALID
	ITEM_NUMBER_I	 NONUNIQUE	 ITEM_NUMBER				1 VALID

执行统计信息收集程序，确认异常：

	SQL> conn /as sysdba
	Connected.
	SQL> begin
	  2  dbms_stats.gather_table_stats('"BARCODE"','"BC_BOXES"','""');
	  3  end;
	  4  /
	begin
	*
	ERROR at line 1:
	ORA-20000: index "BARCODE"."BC_BOXES_I"  or partition of such index is in
	unusable state
	ORA-06512: at "SYS.DBMS_STATS", line 20337
	ORA-06512: at "SYS.DBMS_STATS", line 20360
	ORA-06512: at line 2

## 解决异常

重建索引：

	SQL> alter index "BARCODE"."BC_BOXES_I" rebuild tablespace barcode_idx nologging;
	
	Index altered.


再次执行搜集程序：

	SQL> begin
	  2  dbms_stats.gather_table_stats('"BARCODE"','"BC_BOXES"','""');
	  3  end;
	  4  /
	
	PL/SQL procedure successfully completed.

## 关于重建索引
	
When you rebuild an index, you use an existing index as the data source. Creating an index in this manner enables you to change storage characteristics or move to a new tablespace. Rebuilding an index based on an existing data source removes intra-block fragmentation. Compared to dropping the index and using the `CREATE INDEX` statement, re-creating an existing index offers better performance.

即：重建(rebuild)索引使用已有的索引作为数据源，可以调整存储参数，移除数据块之间的碎片。另外，重要的一点是，相比先删除(drop)再创建索引(create index)，重建(rebuild)能够提供更好的性能。

## 参考

 * Oracle Database Administrator's Guide#Rebuilding an Existing Inde
