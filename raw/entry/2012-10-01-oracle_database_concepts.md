---
layout: post
title: Oracle Database Concepts
category : Oracle
tags : [Oracle, Database, DBA]
---

Oracle Database概念非常多，其中关于SID、NAMES以及监听参数的定义和关系经常让人混
淆。在[tianlesoftware](http://blog.csdn.net/tianlesoftware)的博客上，有一篇专门 讲解了这些概念，行文思路清晰，概念和实践分析相结合，易于理解；且文中大量引用官 方文档，来源可靠，可信度高。作者的博客很值得同行学习和借鉴。 

由于刚入行不久，秉承实用原则这里仅作粗略了解和记录，详情可以参见博客原文。

##基本概念

###db相关

* dbid, sid

###pfile参数

* `db_name`, `db_domain`, `instance_name`

* `db_unique_name`, `service_names`

* `global_name`, `global_names`

###listener.ora参数

* `sid_name`, `global_dbname`

###tnsnames.ora参数

* `service_name`, `sid`

###1. DB相关

####dbid

* `db_name`在数据库内部的表示，创建数据库时用`db_name`结合一种算法生成。

* `dbid`存在于数据文件、控制文件中，表示数据文件的归属，`dbid`唯一。不同数据库 `dbid`不同，但`db_name`有可能相同

####dbid 和 sid

查看dbid：

	select * from v$database;

####在controlfile中查看dbid和sid

转存控制文件到trace file：

	alter session set events 'immediate trace name CONTROLF level 8'; 

	select gettracefile() from dual; 

	Db ID=1873459096=0x6faab798, Db Name='EGOLIFE'

####修改`dbid`和`dbname`

主要步骤：

* a. `startup mount`;
* b. `nid TARGET=SYS/oracle@egolife DBNAME=one`
* c. `startup mount`;
* d. `alter database open resetlogs`;

更改`dbname`自后，之前的备份均无效。

####查看`sid`(system identifier)

	ORACLE_SID sid
	ORACLE_HOME oracle home

oracle用`sid`和`oracle_home`生成一个key，来创建共享内存。

###2. pfile参数

	SQL> show parameter name
	NAME TYPE VALUE
	-------------------------- ----------- --------------------
	db_file_name_convert       string
	db_name                    string       MANUAL
	db_unique_name             string       MANUAL
	global_names               boolean     	FALSE
	instance_name              string       MANUAL
	lock_name_space            string
	log_file_name_convert      string
	service_names              string       MANUAL.egolife.com
	
####db_name

* 不能超过8个字符
* 动态注册监听

###instance_name

* 在RAC环境中`DB_NAME`相同，但`INSTANCE_NAME`不同，用以区分唯一的实例
* 默认值为`SID`，一般与数据库名相同，也可以不同
* 与进程名相关 ,并且`initSID.ora/orapwSID`与`instance_name`保持一致

####db_domain

* 区分网络层次结构

####db_unique_name

* 在DataGuard环境中，DB_NAME相同，但`DB_UNIQUE_NAME`不同

####service_names

* 值：`db_unique_name.db_domain`

####global_name

* 由`db_name.db_domain`组成

####global_names

* 创建db link时是否强制使用远程数据库的`global_name`，多用于分布式系统

###3. listener.ora参数

####sid_name

* 数据库的运行的实例名，与`instance_name`一致

####global_dbname

* 配置静态监听需要使用
* `global_dbname`是listener对外的连接名称，我们可以写成任意值，客户端配置时， `service_name`需要与`global_dbname`一致
* 如果是动态监听，因`service_names`由多个，则会注册多个，每个对应着同一个 `instance_name`，这样配置任意一个即可访问

###4. tnsnames.ora参数

####service_name

* 静态监听：`service_name` = `global_dbname`
* 动态监听：`service_name` = `service_names`(在initSID.ora文件中)

####sid

* 直接指定`instance_name`

##参考

 * [SID、NAMES及监听参数说明](http://blog.csdn.net/tianlesoftware)
 * [Oracle小知识总结(一)](http://blog.csdn.net/tianlesoftware/article/details/5622268)
