---
layout: post
title: A Case of ATO Exception
category : Oracle
tags : [Oracle, Database, DBA, EBS]
---

##异常症状

2012-12-21下午Oracle ERP在销售模块做ATO产品订单进展时，没有弹出任何错误，也没有 弹出订单进展的"确认"提示，直接跳到订单头信息，行信息中也没有出现带`*`的标准成品料 号。且所有的ATO订单都无法完成订单进展。导致特制单不能及时录入系统，问题较为严重。

##解决思路

使用topas查看操作系统是否有异常进程；

登录系统查看并发请求状态；

查系统当前会话、进程数；

看数据库警告日志；

##详细过程

###1. OS进程检查

登录到erp，运行topas观察系统进程使用资源情况。

###2. 并发请求 

职责路径：system administrator >> Concurrent >> Manager >> Administer 此时再查看并发管理运行状态，等待处理的请求 因只有系统管理员有该权限，大家也可以通过SQL脚本进行查询，脚本如下(可以APPS运行)：

	WITH requests_count AS
	(SELECT COUNT(1) counts
   	FROM apps.fnd_concurrent_requests fcr
	WHERE fcr.request_date > trunc(SYSDATE - 1)
     AND fcr.requested_start_date < trunc(SYSDATE + 1)
     AND fcr.phase_code IN ('P', 'R'))
	SELECT 'Attention! Concurrent requests are up to ' || rc.counts "attention"
 	FROM requests_count rc
	WHERE rc.counts > 300;

###3. 系统当前进程、会话数

Oracle数据库当前数据库设置的最大进程数、会话数在数据初始参数中已经设置，可以查询如下：

1)使用PL/SQL Developer，打开Command Windows即可（以APPS运行）

	SQL> show parameter processes
	 
	NAME                                 TYPE        VALUE
	------------------------------------ ----------- ------------------------------
	aq_tm_processes                      integer     2
	db_writer_processes                  integer     1
	job_queue_processes                  integer     10
	log_archive_max_processes            integer     2
	processes                            integer     800
	 
	SQL> show parameter sessions
	 
	NAME                                 TYPE        VALUE
	------------------------------------ ----------- ------------------------------
	java_max_sessionspace_size           integer     0
	java_soft_sessionspace_limit         integer     0
	license_max_sessions                 integer     0
	license_sessions_warning             integer     0
	logmnr_max_persistent_sessions       integer     1
	mts_sessions                         integer     0
	sessions                             integer     1600
	shared_server_sessions               integer     0
	

2)使用SQL脚本查询，打开SQL Windows，或者SQLPlus(以APPS运行)

	select * from v$parameter p where p.NAME in ('processes','sessions');

再查看当前系统的进程数、会话数。

	SELECT COUNT(*) FROM v$process;	--当前进程数

	SELECT COUNT(*) FROM v$session; --当前会话数

当以上数目非常接近系统设定的最大值时，系统就可能出现类似以上的问题，主要是超出最 大会话数，无法进行新的会话、连接等响应。

此时一般会手动处理一些过期的会话，主要是以下方式

	--类似session/cookie的会话
	SELECT 'kill -9 ' || b.spid
	  FROM v$session a,
	       v$process b,
	       v$sqltext c
	 WHERE a.paddr = b.addr
	   AND a.username IS NOT NULL
	   AND c.hash_value = a.sql_hash_value
	   AND c.sql_text LIKE '%SESSION_COOKIE_DOMAIN%'
	   AND a.sid != (SELECT sid FROM v$mystat WHERE rownum = 1);

	--当前之前还没有正常回收的forms会话
	SELECT 'alter system kill session' || '''' || s.sid || ',' || s.serial# || ''';' oracle_level_kill
	  FROM v$session s,
	       v$process p
	 WHERE s.paddr = p.addr
	   AND s.sid IN (SELECT se.sid
	                   FROM v$session se
	                  WHERE sid IN (SELECT session_id FROM v$locked_object)
	                    AND se.logon_time < trunc(SYSDATE))
	   AND s.action LIKE 'FRM:%'
	   AND s.STATUS = 'INACTIVE';

###4.查看数据库警告日志

数据库警告日志中记录了数据库在运行过程中的状态信息，包括发生的错误。 登录到服务器主机，如prodora，警告日志文件路径：

	注：
	以上路径也是在数据库的初始化参数设定，查询如下：
	--PL/SQL Developer的Command Windows
	SQL> show parameter background_dump_dest;
	 
	NAME                                 TYPE        VALUE
	------------------------------------ ----------- ------------------------------
	background_dump_dest                 string      /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/bdump

	--sql脚本
	select * from v$parameter p where p.NAME in ('background_dump_dest');

	如今天的警告日志截取如下：
	Errors in file /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_5173482.trc:
	ORA-00600: 内部错误代码，参数: [15419], [severe error during PL/SQL execution], [], [], [], [], [], []
	ORA-06544: PL/SQL: 内部错误，参数: [77406], [], [], [], [], [], [], []
	ORA-06553: PLS-801: 内部错误 [77406]
	ORA-00018: 超出最大会话数
	ORA-06512: 在"APPS.FND_SIGNON", line 239
	Fri Dec 21 15:32:03 2012
	Timed out trying to start process J002.
	Fri Dec 21 15:32:43 2012
	Errors in file /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_3883030.trc:
	ORA-00600: 内部错误代码，参数: [4414], [0], [0], [5454], [2], [], [], []
	ORA-00018: 超出最大会话数
	ORA-00018: 超出最大会话数
	Fri Dec 21 15:33:55 2012
	Errors in file /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_688340.trc:
	ORA-00600: 内部错误代码，参数: [15419], [severe error during PL/SQL execution], [], [], [], [], [], []
	ORA-06544: PL/SQL: 内部错误，参数: [77406], [], [], [], [], [], [], []
	ORA-06553: PLS-801: 内部错误 [77406]
	ORA-00018: 超出最大会话数
	ORA-06512: 在"APPS.FND_SIGNON", line 239
	Fri Dec 21 15:33:55 2012
	Errors in file /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_6520900.trc:
	ORA-00600: 内部错误代码，参数: [15419], [severe error during PL/SQL execution], [], [], [], [], [], []
	ORA-06544: PL/SQL: 内部错误，参数: [77406], [], [], [], [], [], [], []
	ORA-06553: PLS-801: 内部错误 [77406]
	ORA-20001: Oracle 错误 -18：FND_SIGNON.AUDIT_END 中检测到 ORA-00018: 超出最大会话数。
	ORA-06512: 在"APPS.APP_EXCEPTION", line 72
	ORA-06512: 在"APPS.FND_SIGNON", line 18
	ORA-06512: 在"APPS.FND_SIGNON", line 317
	Fri Dec 21 15:34:43 2012
	Completed checkpoint up to RBA [0x514c6.2.10], SCN: 0x0771.4352af6c
	Fri Dec 21 15:40:51 2012
	Restarting dead background process QMN0
	QMN0 started with pid=600
	Fri Dec 21 15:41:06 2012
	Errors in file /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_6520900.trc:
	ORA-00600: 内部错误代码，参数: [17285], [0x1103D2D58], [4294967295], [0x70000008B9DF418], [], [], [], []
	Fri Dec 21 15:41:07 2012
	Errors in file /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_6520900.trc:
	ORA-00600: 内部错误代码，参数: [17285], [0x1103D2D58], [4294967295], [0x70000008B9DF418], [], [], [], []
	ORA-00600: 内部错误代码，参数: [17285], [0x1103D2D58], [4294967295], [0x70000008B9DF418], [], [], [], []
	Fri Dec 21 15:42:37 2012
	Errors in file /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_4214832.trc:
	ORA-00604: 递归 SQL 层 1 出现错误
	ORA-00018: 超出最大会话数
	ORA-06512: 在line 1
	Fri Dec 21 15:42:40 2012
	Errors in file /u1/PROD/prodora/proddb/9.2.0/admin/PROD_erpprod/udump/prod_ora_3190972.trc:
	ORA-00604: 递归 SQL 层 1 出现错误
	ORA-00018: 超出最大会话数
	ORA-06512: 在line 1
	
通过发生的ORA-错误，以及应用的异常时间，基本可以确定是由于会话引起的以上异常，清 理一些过期的会话就可以解决。

##特别说明

在操作系统中已经做了一些cron任务，定期预警或者执行会话清理。主要如下：

* 定期清理过期会话(session)
* 定期检查死锁(deadlock)
* 定期检查请求(requests)
* 定期检查无效对象、表空间等(invalidobject, tablespace, tablespaces)
* 定期检查数据库警告日志(checkalert.sh)

以上脚本均会发送邮件通知。

查看prodora定义的cron job

	$ crontab -l
	45 07,13,16 * * *   /u1/PROD/prodora/dailyduty.sh session  > /dev/null 2>&1
	00 08 * * *   /u1/PROD/prodora/dailyduty.sh database > /dev/null 2>&1
	05 08 * * *   /u1/PROD/prodora/dailyduty.sh instance > /dev/null 2>&1
	10 08 * * *   /u1/PROD/prodora/dailyduty.sh datafiles > /dev/null 2>&1
	15 08 * * *   /u1/PROD/prodora/dailyduty.sh tablespaces > /dev/null 2>&1
	20 08 * * 5   /u1/PROD/prodora/dailyduty.sh tablespace > /dev/null 2>&1
	00 10,16 * * *   /u1/PROD/prodora/dailyduty.sh deadlock > /dev/null 2>&1
	00 15,16,17 * * *   /u1/PROD/prodora/dailyduty.sh requests > /dev/null 2>&1
	00 08 * * 5   /u1/PROD/prodora/dailyduty.sh invalidobject > /dev/null 2>&1
	55 23 * * 0-4   /u1/PROD/prodora/checkalert.sh > /dev/null 2>&1
	
主要脚本dailyduty.sh

	#!/bin/ksh
	#abstract:
	#oracle database alert jobs
	#history:
	#2012-06-11     dylanninin@gmail.com         first release
	#variables
	script_basepath=/u1/PROD/prodora/sql
	mail_date=$(date +%Y-%m-%d\ %H:%M:%S)
	receipt=dylanninin@gmail.com
	hostname=$(hostname)
	
	#path
	ORACLE_HOME=/u1/PROD/prodora/proddb/9.2.0
	export ORACLE_HOME
	PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:$ORACLE_HOME/bin
	export PATH
	ORACLE_SID=PROD
	export ORACLE_SID
	
	
	#variabls
	script_name=$1
	if [ "${script_name}" == "" ]; then
	   echo "script file name was empty!"
	   exit 0
	fi
	script="${script_basepath}/${script_name}.sql"
	if [ ! -e ${script} ]; then
	   echo "sql script file ${script} does not exist!"
	   exit 0
	fi
	
	#sql spool log file
	sqllog="${script_basepath}/${script_name}.log"
	
	#sqlplus logon
	sqlplus -s '/as sysdba' << EOF
	set feed off
	set linesize 200
	set pagesize 200
	spool ${sqllog}
	@${script}
	spool off
	exit
	EOF
	
	#grep spool file and kill processes
	if [ "${script_name}" == "session" ]; then
	   grep "kill -9" ${sqllog} | awk 'NR >1 {print $0}' | ksh
	fi
	
	#mail
	if [ "${script_name}" != "session" ]; then
	   if [ `cat ${sqllog} | wc -l` -gt 0 ]; then
	       cat ${sqllog} | mail -s "${mail_date}:${hostname} dba daily check of ${script_name}" ${receipt} 
	   fi
	fi

##参考

* Oracle Database Administrator Guide
* Oracle Application Administrator Guide
