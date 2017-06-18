---
layout: post
title: Statspack Introduction
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

Oracle  Statspack 从 Oracle8.1.6 开始被引入 Oracle,并马上成为 DBA 和 Oracle 专家用来诊断数据库性能的强有力的工具。通过 Statspack 我们可以很容易的确定 Oracle 数据库的瓶颈所在，记录数据库性能状态，也可以使远程技术支持人员迅速了解你的数据库运行状况。因此了解和使用 Statspack 对于 DBA 来说至关重要。

Oracle 10g之前对数据库做性能检测使用statspack工具，自10g 提供了一个新的工具：(AWR:Automatic Workload Repository)。Oracle 建议用户用这个取代 Statspack。AWR 实质上是一个 Oracle 的内置工具，它采集与性能相关的统计数据，并从那些统计数据中导出性能量度，以跟踪潜在的问题。

在数据库中 Statspack 的脚本位于`$ORACLE_HOME/RDBMS/ADMIN` 目录下。

## 基本使用

### 1.安装statspack.

在$ORACLE_HOME/rdbms/admin/目录下运行：

	SQL> @spcreate.sql

若创建失败则在同一目录下运行： 
	
	SQL> @spdrop.sql
 
### 2.测试

	SQL>execute statspack.snap
	  PL/SQL procedure successfully completed.
	SQL>execute statspack.snap
	  PL/SQL procedure successfully completed.
	SQL>@spreport.sql
 
	SQL>exec statspack.snap; 

进行信息收集统计，每次运行都将产生一个快照号，获得快照号，必须要有两个以上的快照，才能生成报表
 
### 3.查选快照信息

	SQL>select SNAP_ID, SNAP_TIME from STATS$SNAPSHOT;
 
### 4.获取statspack 报告

	SQL>@spreport.sql          
                                                         
按照提示，输入需要查看的开始快照号与结束快照号即可。
 
### 5.其他相关脚本

* spauto.sql： 利用dbms_job提交一个作业，自动的进行STATPACK的信息收集统计
* sppurge.sql ：清除一段范围内的统计信息，需要提供开始快照与结束快照号
* sptrunc.sql ： 清除(truncate)所有统计信息
 
### 6.查看Statspack 生成源代码

在oracle 9i里面，我们可以通过查看statspack 生成脚本来帮助我们理解report，但是10g的AWR是通过`dbms_workload_repository`包来实现AWR的。包把代码都封装了起来，我们无法查看。
 	
statspack的生成脚本位置：`$ORACLE_HOME/rdbms/admin/sprepins.sql`
代码很长，不过看懂了，能帮助我们理解statspack中各个数据的意义。


## 检查系统参数

为了能够顺利安装和运行 Statspack 你可能需要设置以下系统参数：

### 1.`job_queue_processes` 

为了能够建立自动任务，执行数据收集，该参数需要大于 0。你可以在初试化参数文件中修改该参数(使该参数在重起后以然有效)。 

该参数可以在系统级动态修改。

	SQL> show parameter job_queue_processes;
	
	NAME                                 TYPE        VALUE
	------------------------------------ ----------- ------------------------------
	job_queue_processes                  integer     2
	SQL> alter system set job_queue_processes=6;
	
	System altered.
	
	SQL> show parameter job_queue_processes;
	
	NAME                                 TYPE        VALUE
	------------------------------------ ----------- ------------------------------
	job_queue_processes                  integer     6

在 Oracle9i 当中，可以指定范围，如 both,这样该修改在当前及之后保持有效(仅当你使用 spfile时，如果在 9i 中仍然使用 pfile，那么更改方法同 8i 相同): 

	SQL> alter system set job_queue_processes = 6 scope=both;   
	System altered.

### 2.`timed_statistics` 

收集操作系统的计时信息，这些信息可被用来显示时间等统计信息、优化数据库和 SQL 语句。要防止因从操作系统请求时间而引起的开销，请将该值设置为 False。 

使用 statspack 收集统计信息时建议将该值设置为 True，否则收集的统计信息大约只能起到10%的作用，将 timed_statistics 设置为 True 所带来的性能影响与好处相比是微不足道的。 

该参数使收集的时间信息存储在在 V$SESSTATS 和 V$SYSSTATS 等动态性能视图中。

timed_statistics 参数可以在实例级进行更改

	SQL> alter system set timed_statistics = true; 
	System altered 
	SQL> show parameter timed_statistics;
	
	NAME                                 TYPE        VALUE
	------------------------------------ ----------- ------------------------------
	timed_statistics                     boolean     TRUE

如果你担心一致启用 timed_statistics  对于性能的影响，你可以在使用 statspack 之前在 system 更改，采样过后把该参数动态修改成 false。


## 检查Statspack
因测试环境中之前做过statspack监控，并未删除statspack对象，因此这里仅确认下是否安装正确。要看安装、卸载等，请查阅参考文档。

### 1.statspack检查

statspack脚本均在$ORACLE_HOME/rdbms/admin下。首先切换到该目录，下面执行脚本时会比较方便。

切换到该路径

	$ pwd
	/u2/TEST/testora/testdb/9.2.0/rdbms/admin

sp脚本

	$ ls sp*
	sp__.lst          spcpkg.sql        spctab.sql        spdoc.txt         spdusr.sql        spreport.sql      sprepsql.sql      spup816.sql
	spauto.sql        spcreate.sql      spcusr.lis        spdrop.sql        sppurge.sql       spreport0902.txt  sptrunc.sql       spup817.sql
	spcpkg.lis        spctab.lis        spcusr.sql        spdtab.sql        sprepins.sql      spreport0907.txt  spuexp.par        spup90.sql

### 2.测试sp脚本

	SQL> execute statspack.snap
	
	PL/SQL procedure successfully completed.
	
	SQL> execute statspack.snap
	
	PL/SQL procedure successfully completed.
	SQL> @spreport.sql
	……	

### 3.检查statspach表空间

	SQL> SELECT tablespace_name,file_name, round(dbf.BYTES / (1024 * 1024),0) "Total_space(M)" FROM dba_data_files dbf where dbf.TABLESPACE_NAME = 'STATSPACK';  
			TABLESPACE_NAME   FILE_NAME                     Total_space(M)
	-------------------- ------------------------------------------------------------ --------------
	STATSPACK  /u2/TEST/testora/testdata/statspack_01.dbf               500.00

## 规划自动任务

Statspack 正确安装以后，我们就可以设置定时任务，开始收集数据了。可以使用 spatuo.sql 来定义自动任务。

先来看看 spauto.sql 的关键内容：

	variable jobno number;
	variable instno number;
	begin
	  select instance_number into :instno from v$instance;
	  dbms_job.submit(:jobno, 'statspack.snap;',
	  trunc(sysdate+1/24,'HH'), 'trunc(SYSDATE+1/24,'HH')', 
	TRUE, :instno);
	  commit;
	end;

这个 job 任务定义了收集数据的时间间隔：

	一天有 24 个小时，1440 分钟，那么：
		1/24   HH           每小时一次
		1/48   MI           每半小时一次
		1/144  MI           每十分钟一次
		1/288  MI           每五分钟一次

	SQL> @spauto
	
	PL/SQL procedure successfully completed.
	
	
	Job number for automated statistics collection for this instance
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Note that this job number is needed when modifying or removing
	the job:
	
	     JOBNO
	----------
	     87890
	
	
	Job queue process
	~~~~~~~~~~~~~~~~~
	Below is the current setting of the job_queue_processes init.ora
	parameter - the value for this parameter must be greater
	than 0 to use automatic statistics gathering:
	
	NAME_COL_PLUS_SHOW_PARAM                                         TYPE
	---------------------------------------------------------------- -----------
	VALUE_COL_PLUS_SHOW_PARAM
	------------------------------------------------------------------------------
	job_queue_processes                                              integer
	6
	
	
	Next scheduled run
	~~~~~~~~~~~~~~~~~~
	The next scheduled run for this job is:
	
	       JOB NEXT_DATE       NEXT_SEC
	---------- --------------- ------------------------
	     87890 28-JUN-12       10:00:00

关于采样间隔，我们通常建议以 1 小时为时间间隔，对于有特殊需要的环境，可以设置更短的，如半小时作为采样间隔，但是不推荐更短。因为 statspack 的执行本身需要消耗资源，对于繁忙的生产系统，太短的采样对系统的性能会产生较大的影响（甚至会使 statspack 的执行出现在采样数据中）。

## 生成分析报告

运行spreport脚本，输入起始和结束的快照ID，生成分析报告。

	SQL> @spreport
	Current Instance
	~~~~~~~~~~~~~~~~
	   DB Id    DB Name      Inst Num Instance
	---------- ------------ -------- ------------
	   33115540 ERP                 1 ERP 
	Instances in this Statspack schema
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	   DB Id    Inst Num DB Name      Instance     Host
	----------- -------- ------------ ------------ ------------
	   33115540        1 ERP          ERP          erp
	   56114082        1 PROD         PROD         erpprod
	
	Using   33115540 for database Id
	Using          1 for instance number
	Completed Snapshots
	                               Snap                    Snap
	Instance     DB Name             Id   Snap Started    Level Comment
	------------ ------------ --------- ----------------- ----- --------------------
	ERP          ERP                753 28 Jun 2012 10:30     5
	                                754 28 Jun 2012 11:30     5
	                                755 28 Jun 2012 12:30     5
	                                756 28 Jun 2012 13:30     5
	                                757 28 Jun 2012 14:30     5
	                                758 28 Jun 2012 15:30     5 
	Specify the Begin and End Snapshot Ids
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	Enter value for begin_snap: 753
	Begin Snapshot Id specified: 753
	Enter value for end_snap: 758
	End   Snapshot Id specified: 758
	Specify the Report Name
	~~~~~~~~~~~~~~~~~~~~~~~
	The default report file name is sp_753_758.  To use this name,
	press <return> to continue, otherwise enter an alternative.
	Enter value for report_name: sp_753_758.txt
	Using the report name sp_753_758.txt SNATSPACK report for DB Name         DB Id    Instance     Inst Num Release     Cluster Host
	----------- ----------- ------------ -------- ----------- ------- ------------
	ERP             33115540 ERP                 1 9.2.0.6.0   NO      erp
	              Snap Id     Snap Time      Sessions Curs/Sess Comment
	            --------- ------------------ -------- --------- -------------------
	Begin Snap:       753 28-Jun-12 10:30:16      153      91.9
	  End Snap:       758 28-Jun-12 15:30:17      160      90.5
	   Elapsed:              300.02 (mins) ……

一个 statspack 的报告不能跨越一次停机，但是之前或之后的连续区间，收集的信息依然有效。你可以选择之前或之后的采样声称 report。

## 移除定时任务

运行dbms_job.remove(‘job_id’)，移除定时任务。

	SQL> select job,log_user,priv_user,last_date,next_date,interval from user_jobs;
	    JOB LOG_USER  PRIV_USER LAST_DATE NEXT_DATE INTERVAL
	------------ --------------- -------------- ----------------  -------------- --------------------------
	87890 	SYS   SYS 	    28-JUN-12 28-JUN-12  trunc(SYSDATE+1/24,'HH') 

	SQL> execute dbms_job.remove('87890');
	PL/SQL procedure successfully completed.


## 删除历史数据

删除stats$snapshot数据表中的数据，其他表中的数据会相应的级联删除

	SQL> select max(snap_id) from stats$snapshot;
	MAX(SNAP_ID)
	------------
	        758
	SQL> delete from stats$snapshot where snap_id < = 758;

如果采样了大量的数据，直接delete是非常会慢的，可以考虑使用sptrunc脚本，清空stats历史数据。

	SQL> @sptrunc.sql 
	Warning
	~~~~~~~
	Running sptrunc.sql removes ALL data from Statspack tables.  You may
	wish to export the data before continuing. 
	About to Truncate Statspack Tables ……

## 延伸阅读

* [statspack安装使用和report分析](http://blog.csdn.net/tianlesoftware/article/details/4682329)
* [Oracle AWR说明](http://blog.csdn.net/tianlesoftware/article/details/4682300)

## 参考

* [statspack使用指南](http://www.eygle.com/pdf/Statspack-v3.0.pdf
