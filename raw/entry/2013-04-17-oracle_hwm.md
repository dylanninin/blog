---
layout: post
title: HWM Introduction
category : Oracle
tags : [Oracle, Database, DBA]
---

在ORACLE Database中，执行对表的删除操作不会降低该表的高水位线。而全表扫描将始终读取一个段(extent)中所有低于高水位线标记的块。如果在执行删除操作后不降低高水位线标记，则将导致查询语句的性能低下。rebuild, truncate, shrink,move 等操作会降低高水位。

## 实验

### 创建表

	[oracle@dev ~]$ sqlplus /nolog
	
	SQL*Plus: Release 11.2.0.1.0 Production on Wed Apr 17 14:25:48 2013
	
	Copyright (c) 1982, 2009, Oracle.  All rights reserved.
	
	SQL> conn dev
	Enter password: 
	Connected.
	SQL> create table hwm (id number);
	
	Table created.
	
	SQL> select segment_name,segment_type,blocks from dba_segments where segment_name = 'HWM';
	
	no rows selected

	
	SQL> select table_name,num_rows, blocks, empty_blocks from user_tables where table_name = 'HWM';
	
	TABLE_NAME			 			NUM_ROWS     BLOCKS EMPTY_BLOCKS
	------------------------------ ---------- ---------- ------------
	HWM

疑问：在查询dba_segments时没有找到数据，延时？？？

	
### 插入数据

	SQL> declare
	  2      i number;
	  3  begin
	  4      for i in 1..10000 loop
	  5          insert into hwm values(i);
	  6      end loop;
	  7      commit;
	  8  end;
	  9  /
	
	PL/SQL procedure successfully completed.
	

	SQL> select segment_name,segment_type,blocks from dba_segments where segment_name = 'HWM';
	
	SEGMENT_NAME	   SEGMENT_TYPE	  	  	  BLOCKS
	------------------ ------------------ ----------
	HWM			       TABLE			  		  24
	

	SQL> select table_name,num_rows, blocks, empty_blocks from user_tables where table_name = 'HWM';
	
	TABLE_NAME		   NUM_ROWS       BLOCKS EMPTY_BLOCKS
	------------------ ---------- ---------- ------------
	HWM
	
此时表HWM已经占有了数据，24个数据块。其他统计信息为空。这些信息需要做统计分析之后才会有。

### 搜集统计信息

	SQL> exec dbms_stats.gather_table_stats('DEV','HWM');
	
	PL/SQL procedure successfully completed.
	
	SQL> select segment_name,segment_type,blocks from dba_segments where segment_name = 'HWM';
	
	SEGMENT_NAME	   SEGMENT_TYPE	  	  	  BLOCKS
	------------------ ------------------ ----------
	HWM			       	TABLE			  		  24
	
	SQL> select table_name,num_rows, blocks, empty_blocks from user_tables where table_name = 'HWM';
	
	TABLE_NAME		   	 NUM_ROWS     BLOCKS EMPTY_BLOCKS
	------------------ ---------- ---------- ------------
	HWM				    	10000	  	  20			0
	
使用`dbms_stats`收集统计信息后，显示表HWM有1000行，占用20个数据块。但`EMPTY_BLOCKS`为空，该列需要在`ANALYZE`之后才会有数据。


### 分析表
	
	
	SQL> analyze table hwm compute statistics;
	
	Table analyzed.


	SQL> select segment_name,segment_type,blocks from dba_segments where segment_name = 'HWM';
	
	SEGMENT_NAME	   SEGMENT_TYPE	  	  	  BLOCKS
	------------------ ------------------ ----------
	HWM			       TABLE			  		  24
	
	SQL> select table_name,num_rows, blocks, empty_blocks from user_tables where table_name = 'HWM';
	
	TABLE_NAME		   	 NUM_ROWS     BLOCKS EMPTY_BLOCKS
	------------------ ---------- ---------- ------------
	HWM				    	10000	  	  20			4
	

### 删除数据

	SQL> delete from hwm;
	
	10000 rows deleted.
	
	SQL> commit;
	
	Commit complete.
	
	SQL> select segment_name,segment_type,blocks from dba_segments where segment_name = 'HWM';
	
	SEGMENT_NAME	   SEGMENT_TYPE	  	  	  BLOCKS
	------------------ ------------------ ----------
	HWM			       TABLE			  		  24
	
	SQL> select table_name,num_rows, blocks, empty_blocks from user_tables where table_name = 'HWM';
	
	TABLE_NAME		   	 NUM_ROWS     BLOCKS EMPTY_BLOCKS
	------------------ ---------- ---------- ------------
	HWM				        10000	      20			4
	

删除数据后再分析表

	SQL> analyze table hwm compute statistics;
	
	Table analyzed.
	
	SQL> select segment_name,segment_type,blocks from dba_segments where segment_name = 'HWM';
	
	SEGMENT_NAME	   SEGMENT_TYPE	  	  	  BLOCKS
	------------------ ------------------ ----------
	HWM			       TABLE			  	      24
	
	SQL> select table_name,num_rows, blocks, empty_blocks from user_tables where table_name = 'HWM';
	
	TABLE_NAME		   	 NUM_ROWS     BLOCKS EMPTY_BLOCKS
	------------------ ---------- ---------- ------------
	HWM							0	  	  20			4
	

delete数据，不会降低高水位。


### truncate表

	SQL> truncate table hwm;
	
	Table truncated.

	SQL> select segment_name,segment_type,blocks from dba_segments where segment_name = 'HWM';
	
	SEGMENT_NAME	   SEGMENT_TYPE	  	  	  BLOCKS
	------------------ ------------------ ----------
	HWM			       TABLE			   		   8
	
	SQL> select table_name,num_rows, blocks, empty_blocks from user_tables where table_name = 'HWM';
	
	TABLE_NAME		   	 NUM_ROWS     BLOCKS EMPTY_BLOCKS
	------------------ ---------- ---------- ------------
	HWM						    0	  	  20			4
	

runcate后再次收集统计信息


	SQL> exec dbms_stats.gather_table_stats('DEV','HWM');
	
	PL/SQL procedure successfully completed.

	SQL> select segment_name,segment_type,blocks from dba_segments where segment_name = 'HWM';
	
	SEGMENT_NAME	   SEGMENT_TYPE	  	  	  BLOCKS
	------------------ ------------------ ----------
	HWM			       TABLE			   		   8
	
	
	SQL> select table_name,num_rows, blocks, empty_blocks from user_tables where table_name = 'HWM';
	
	TABLE_NAME		   	 NUM_ROWS     BLOCKS EMPTY_BLOCKS
	------------------ ---------- ---------- ------------
	HWM						    0	       0			4
	

再次分析表

	SQL> analyze table hwm compute statistics;
	
	Table analyzed.

	SQL> select segment_name,segment_type,blocks from dba_segments where segment_name = 'HWM';
	
	SEGMENT_NAME	   SEGMENT_TYPE	  	  	  BLOCKS
	------------------ ------------------ ----------
	HWM			       TABLE			   		   8
	
	SQL> select table_name,num_rows, blocks, empty_blocks from user_tables where table_name = 'HWM';
	
	TABLE_NAME		   	 NUM_ROWS     BLOCKS EMPTY_BLOCKS
	------------------ ---------- ---------- ------------
	HWM						    0	   	   0		    8

truncate后，高水位降低。
