---
layout: post
title: The Invalid Object of Oracle Database
category : Oracle
tags : [Oracle, Database, DBA, Exception]
---

##异常症状

在Oracle EBS系统中可以正常打开物料编辑页面，输入料号、描述等，选择物料模板，点击 保存按钮保存；此时切换到组织属性或组织分配页，再切换回物料属性页或者按料号查找该 物料，均无法找到该物料的信息；直接在数据库中查找该物料为空。

##异常确认

登录到Oracle ERP系统，输入物料确实无法保存；最大化编辑页面，Oracle Forms左下角没 有保存数据的事务操作提示。

##环境

* Oracle RDBMS : 11.1.0.7.0
* Oracle Applications : 12.1.1

##异常解决

在ERP服务器上部署了一些定时任务，其中每天结束前（23:55）会定时检查数据库系统的警 告日志，若有错误，则会发送邮件通知。

2012-10-29 收到来自此ERP系统的警告日志邮件通知。

###警告日志

alert_PROD.log.2012-10-28

	Fri Oct 26 14:24:24 2012
	Errors in file /u1/PROD/prodora/db/tech_st/11.1.0/admin/PROD_poprod/diag/rdbms/prod/
	PROD/trace/PROD_ora_14573.trc  (incident=22169):
	ORA-00600: internal error code, arguments: [qcsgpvc3], [], [], [], [], [], [], [], [], [], [], []
	Incident details in: /u1/PROD/prodora/db/tech_st/11.1.0/admin/PROD_poprod/diag/rdbms/
	prod/PROD/incident/incdir_22169/PROD_ora_14573_i22169.trc
	Non critical error ORA-48913 caught while writing to trace file "/u1/PROD/prodora/db/tech_st/11.1.0/admin/PROD_poprod/diag/rdbms/
	prod/PROD/incident/incdir_22169/PROD_ora_14573_i22169.trc"
	Error message: ORA-48913: Writing into trace file failed, file size limit [10485760] reached
	Writing to the above trace file is disabled for now on...

###跟踪日志

`PROD_ora_14573_i22169.trc`

	... ...
	*** 2012-10-26 14:24:24.811
	*** SESSION ID:(307.48840) 2012-10-26 14:24:24.811
	*** CLIENT ID:() 2012-10-26 14:24:24.811
	*** SERVICE NAME:(PROD) 2012-10-26 14:24:24.811
	*** MODULE NAME:(PL/SQL Developer) 2012-10-26 14:24:24.811
	*** ACTION NAME:(Main session) 2012-10-26 14:24:24.811

	Dump continued from file: /u1/PROD/prodora/db/tech_st/11.1.0/admin/PROD_poprod/diag/rdbms/PROD_ora_14573.trc

`PROD_ora_14573.trc`
	
	ORA-00600: internal error code, arguments: [qcsgpvc3], [], [], [], [], [], [], [], [], [], [], []
	========= Dump for incident 22169 (ORA 600 [qcsgpvc3]) ========
	----- Beginning of Customized Incident Dump(s) -----
	QCSGPVC3: icodefs yet to be processed = 1
	QCSGPVC3: ico = 0x7fa94803cad0
	QCSGPVC3: ico->icocop = 0x7fa9478e3ab8
	QCSGPVC3: ico->icocop->colkcc = (nil)
	QCDDMP: -------------------------------------------------------
	QCDDMP:  qcsgpvc3_CTX: [0x7fa94801ee10]
	QCDDMP:  {
	QCDDMP:    ->ctxqbc: [0x7fa94801d068]
	QCDDMP:    {
	QCDDMP:      ->qbcqtxt: N/A
	QCDDMP:      ->qbcfro: [0x7fa94801d3f0]
	QCDDMP:      {
	QCDDMP:        ->frooid: [(nil)]
	QCDDMP:        ->frotni: MTL_SYSTEM_ITEMS_INTERFACE
	QCDDMP:        ->froaid: MTL_SYSTEM_ITEMS_INTERFACE
	QCDDMP:        ->frotyp = 2
	QCDDMP:        ->froflg = 0x4b
	... ...

其中MTL_SYSTEM_ITEMS_INTERFACE表为物料接口表，用于临时保存物料信息。无法保存物 料，可能和此表异常相关。

在MOS上找到关于ORA-600[qcsgpvc3]的一篇文档，有可能是存储过程依赖的表结构发生了变 更，重新编译存储过程时会出现此错误。

根据此文档，在R12的测试环境上进行测试，过程如下：

	SQL> create table xx_qcsgpvc( c1 varchar2(60),c2 number);
	Table created.
	SQL> create or replace package xx_qcsgpvc_p is
	  2  procedure po(c1 varchar2, c2 number);
	  3  end xx_qcsgpvc_p;
	  4  /
	Package created.
	
	SQL> create or replace package body xx_qcsgpvc_p is
	  2  procedure po(c1 varchar2,c2 number)
	  3  is
	  4  begin
	  5  insert into xx_qcsgpvc(c1,c2) values (c1,c2);
	  6  end po;
	  7  end xx_qcsgpvc_p;
	  8  /
	Package body created.
	
	SQL> alter table xx_qcsgpvc rename column c2 to i_problem;
	Table altered.
	
	SQL> alter package xx_qcsgpvc_p compile body;
	Warning: Package Body altered with compilation errors.

###警告日志

alert_VIS.ora

	Mon Oct 29 09:15:01 2012
	Errors in file
	/u1/VIS/visora/db/tech_st/11.1.0/admin/VIS_demoerp/diag/rdbms/
	vis/VIS/trace/VIS_ora_925.trc  (incident=24961):
	ORA-00600: internal error code, arguments: [qcsgpvc3], [], [], [], [], [], [], [], [], [], [], []
	Incident details in:
	/u1/VIS/visora/db/tech_st/11.1.0/admin/VIS_demoerp/diag/rdbms/vis/
	VIS/incident/incdir_24961/VIS_ora_925_i24961.trc

###跟踪日志

`VIS_ora_925_i24961.trc`

	... ...
	*** 2012-10-29 09:15:01.536
	*** SESSION ID:(278.26930) 2012-10-29 09:15:01.536
	*** CLIENT ID:() 2012-10-29 09:15:01.536
	*** SERVICE NAME:(SYS$USERS) 2012-10-29 09:15:01.536
	*** MODULE NAME:(SQL*Plus) 2012-10-29 09:15:01.536
	*** ACTION NAME:() 2012-10-29 09:15:01.536
	
	Dump continued from file:
	/u1/VIS/visora/db/tech_st/11.1.0/admin/VIS_demoerp/diag/rdbms/
	vis/VIS/trace/VIS_ora_925.trc
	ORA-00600: internal error code, arguments: [qcsgpvc3], [], [], [], [], [], [], [], [], [], [], []
	========= Dump for incident 24961 (ORA 600 [qcsgpvc3]) ========
	----- Beginning of Customized Incident Dump(s) -----
	QCSGPVC3: icodefs yet to be processed = 1
	QCSGPVC3: ico = 0x7fc230514c90
	QCSGPVC3: ico->icocop = 0x7fc2305152b8
	QCSGPVC3: ico->icocop->colkcc = (nil)
	QCDDMP: -------------------------------------------------------
	QCDDMP:  qcsgpvc3_CTX: [0x7fc2305106b8]
	QCDDMP:  {
	QCDDMP:    ->ctxqbc: [0x7fc230514438]
	QCDDMP:    {
	QCDDMP:      ->qbcqtxt: N/A
	QCDDMP:      ->qbcfro: [0x7fc2305147c0]
	QCDDMP:      {
	QCDDMP:        ->frooid: [(nil)]
	QCDDMP:        ->frotni: XX_QCSGPVC
	QCDDMP:        ->froaid: XX_QCSGPVC
	QCDDMP:        ->frotyp = 2
	QCDDMP:        ->froflg = 0x43
	... ...

根据以上日志，可能是系统对象做过更改，导致依赖于这些对象的存储过程失效而无法正常 运行。

查看物料相关表创建编译时间

	SELECT owner,
	       object_name,
	       object_type,
	       created,
	       last_ddl_time,
	       TIMESTAMP,
	       status
	  FROM dba_objects do
	  WHERE do.object_name IN ('MTL_SYSTEM_ITEMS_INTERFACE', 'MTL_SYSTEM_ITEMS_B');

物料表和物料接口表近期均未更改和重编译。

###紧接着查找系统无效对象

无效对象

	SELECT owner,
	       object_name,
	       object_type,
	       status
	  FROM dba_objects
	 WHERE status = 'INVALID'
	 ORDER BY owner,
	          object_type,
	          object_name;
	output:
	APPS        OE_ITEMS_MV         MATERIALIZED VIEW       INVALID
	APPS        XX_IMPORT_MATERIEL_PCK   PACKAGE BODY        INVALID
	APPS        XX_ITEM_DEFAULT_SUBINVENTORY      TRIGGER INVALID

无效对象和依赖关系

	SELECT object_name,
	       object_type,
	       referenced_owner,
	       referenced_type,
	       referenced_name
	  FROM user_objects,
	       user_dependencies
	 WHERE object_name = NAME
	   AND status != 'VALID'
	 ORDER BY object_name,
	          object_type,
	          referenced_owner,
	          referenced_type,
	          referenced_name;

生成无效对象的编译脚本

	SELECT decode(object_type,
	              'PACKAGE BODY',
	              'alter package ' || owner || '.' || object_name ||
	              ' compile body;',
	              'alter ' || object_type || ' ' || owner || '.' || object_name ||
	              ' compile;')
	  FROM dba_objects
	 WHERE status = 'INVALID'
	   AND object_type IN ('PACKAGE BODY',
	                       'PACKAGE',
	                       'FUNCTION',
	                       'PROCEDURE',
	                       'TRIGGER',
	                       'VIEW')
	 ORDER BY object_type,
	          object_name;

编译后，还有无效触发器`APPS.XX_ITEM_DEFAULT_SUBINVENTORY`。

再次尝试新建物料时，依然无法保存。

通过与客制化开发人员沟通，了解到最近在尝试开发物料导入功能，以减轻物料录入的负 担。此触发器在11i中使用过，但在R12中不再使用，这里暂且drop掉该触发器或者禁用该触 发器：

	DROP TRIGGER apps.XX_ITEM_DEFAULT_SUBINVENTORY;

再次尝试新建物料时，可以正常保存。

根据ORA-600[qcsgpvc3]的错误提示以及近期有客制化功能开发可以总结，因对象结构发生 变更使得系统中存在一些无效对象从而导致物料无法保存。在本例中，引起物料无法保存的 应是依赖于物料基础表MTL_SYSTEMS_ITEM_B的触发器XX_ITEM_DEFAULT_SUBINVENTORY无效， 即当对物料基础表进行插入操作时该触发器无法运行，导致整个操作失败。在客制化开发过 程中，涉及到更改标准功能或者系统标准对象等，因Oracle系统的庞大和复杂性，无法确定 做出更改后所有功能都可以正常使用；但对数据库系统的日常维护来说，定期检查和编译无 效对象是必须的，否则某些功能将不能正常运行。

##脚本

检查数据库系统警告日志，结合crontab，若有ora error message，则发送邮件通知

checkalert.sh 

	#!/bin/sh
	#abstract:
	#oracle database daily alert check and send mail notifications if ora error messages occur
	#history:
	#2012-08-14     dylanninin@gmail.com         first release
	#variables
	script_basepath=/u1/PROD/prodora/itsection/adm/sql
	mail_date=$(date +%Y-%m-%d\ %H:%M:%S)
	receipt=dylanninin@gmail.com
	hostname=$(hostname)
	
	#path
	ORACLE_HOME=/u1/PROD/prodora/db/tech_st/11.1.0
	export ORACLE_HOME
	PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:
	$ORACLE_HOME/bin
	export PATH
	ORACLE_SID=PROD
	export ORACLE_SID
	
	#sql log file
	script_name=alert
	sqllog="${script_basepath}/${script_name}.log"
	
	#check alert log
	if [ "${script_name}" == "alert" ]; then
	   alert_basepath=/u1/PROD/prodora/db/tech_st/11.1.0/admin/PROD_poprod/diag/rdbms/prod/PROD/trace
	   alert_log=${alert_basepath}/alert_$ORACLE_SID.log
	   if [ -f ${alert_log} ]; then
	        current_date=$(date +%F)
	        current_log=${alert_log}.${current_date}
	        mv  ${alert_log} ${current_log}
	        touch ${alert_log}
	        grep -i ORA- ${current_log} > ${sqllog}
	   else
	        echo -e "Oracle Instance alert log file ${alert_log} does not exist!"
	        touch ${alert_log}
	   fi
	fi
	
	#mail
	if [ ! -e ${sqllog} ]; then
	   echo -e "sqllog file ${sqllog} does not exist!"
	   exit 0
	fi
	if [ `cat ${sqllog} | wc -l` -gt 0 ]; then
	   cat ${sqllog} | mail -s "${mail_date}:${hostname} dba daily check of ${script_name}" ${receipt}
	fi
	
##参考

* Bug 7172752 - OERI[qcsgpvc3] recompiling a package body [ID 7172752.8]
* Invalid Objects In Oracle Applications FAQ [ID 104457.1]
