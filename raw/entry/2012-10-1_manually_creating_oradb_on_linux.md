## 写在前面的话

今年上半年，由于工作调整，开始接手DBA的工作，负责ERP、数据库、服务器等的管理和维护工作。在粗略看完Oracle Database 2 Day DBA的官方文档后，结合一些中文书目以及工作中遇到的问题，对Oracle数据库有了初步的了解。但发现单看中文数目以及解决一个个突发问题，还远远不够，于是开始阅读2 Day DBA的升级版文档Administrator's Guide，并进行一些尝试和实践，希望能够有进一步的理解。

在Adminstartor's Guide的第二章，讲到了如何使用`CREATE DATABASE`语句手工创建数据库。这个语句比MySQL的复杂多了，涵盖了Oracle数据库最核心的概念，需要有一定的基础知识。按照参考文档的提示进行操作时，还是出现过一些错误，最后参考CSDN上的一篇[博客](http://blog.csdn.net/tianlesoftware/article/details/4680213)进行调整，成功创建了数据库，这里记录如下。

## 测试环境

* 操作系统 CentOS 6.0 x86 64bit
* 数据库	  Oracle 10.2

## 创建步骤

### 1. 规划sid,oracle home

	export ORACLE_SID=MANUAL
	export ORACLE_BASE=/db/oracle
	export ORACLE_HOME=/db/oracle/product/10.2.0/db_1

### 2. 系统规划

	ORACLE_SID=manual
	DB_NAME=MANUAL
	DB_DOMAIN=egolife.com

### 3. 手工创建必须的目录

dump目录
	
	mkdir /db/oracle/admin/MANUAL/adump
	mkdir /db/oracle/admin/MANUAL/bdump
	mkdir /db/oracle/admin/MANUAL/cdump
	mkdir /db/oracle/admin/MANUAL/udump
	mkdir /db/oracle/admin/MANUAL/pfile

数据文件目录

	mkdir /db/oracle/oradata/MANUAL

恢复目录
	
	mkdir /db/oracle/flash_recovery_area/MANUAL

### 4. 建立密码文件

	orapwd file=/db/oracle/product/10.2.0/db_1/dbs/orapwMANUAL password=oracle

### 5. 修改参数文件

编辑init.ora文件，更改主要配置：

	MANUAL.__db_cache_size=331350016
	MANUAL.__java_pool_size=4194304
	MANUAL.__large_pool_size=8388608
	MANUAL.__shared_pool_size=138412032
	MANUAL.__streams_pool_size=0
	*._kgl_large_heap_warning_threshold=8388608
	*.audit_file_dest='/db/oracle/admin/MANUAL/adump'
	*.background_dump_dest='/db/oracle/admin/MANUAL/bdump'
	*.compatible='10.2.0.1.0'
	*.control_files='/db/oracle/oradata/MANUAL/control01.ctl',
	'/db/oracle/oradata/MANUAL/control02.ctl',
	'/db/oracle/oradata/MANUAL/control03.ctl'
	*.core_dump_dest='/db/oracle/admin/MANUAL/cdump'
	*.db_2k_cache_size=33554432
	*.db_block_size=8192
	*.db_domain='egolife.com'
	*.db_file_multiblock_read_count=128
	*.db_files=4000
	*.db_name='MANUAL'
	*.db_recovery_file_dest_size=4294967296
	*.db_recovery_file_dest='/db/oracle/flash_recovery_area'
	*.log_checkpoints_to_alert=FALSE
	*.open_cursors=300
	*.parallel_execution_message_size=65535
	*.parallel_max_servers=128
	*.pga_aggregate_target=209715200
	*.processes=150
	*.recyclebin='OFF'
	*.remote_login_passwordfile='EXCLUSIVE'
	*.replication_dependency_tracking=FALSE
	*.session_cached_cursors=100
	*.sga_target=500m
	*.shared_pool_size=100m
	*.undo_management='AUTO'
	*.undo_retention=0
	*.undo_tablespace='UNDOTS'
	*.user_dump_dest='/db/oracle/admin/MANUAL/udump'
	*.workarea_size_policy='AUTO'
	_allow_resetlogs_corruption=true

### 6. 启动数据库

	SQL> conn /as sysdba
	Connected to an idle instance.
	SQL> startup nomount pfile=/db/oracle/product/10.2.0/db_1/dbs/initMANUAL.ora;
	
	ORACLE instance started.
	
	Total System Global Area  524288000 bytes
	Fixed Size     1220336 bytes
	Variable Size   150995216 bytes
	Database Buffers   364904448 bytes
	Redo Buffers     7168000 bytes

### 7. 运行创建数据库脚本

	CREATE DATABASE MANUAL
	LOGFILE
	GROUP 1 ('/db/oracle/oradata/MANUAL/redo01.log',
	'/db/oracle/oradata/MANUAL/redo01_1.log') size 100m reuse,
	GROUP 2 ('/db/oracle/oradata/MANUAL/redo02.log',
	'/db/oracle/oradata/MANUAL/redo02_1.log') size 100m reuse,
	GROUP 3 ('/db/oracle/oradata/MANUAL/redo03.log',
	'/db/oracle/oradata/MANUAL/redo03_1.log') size 100m reuse
	MAXLOGFILES 50
	MAXLOGMEMBERS 5
	MAXLOGHISTORY 200
	MAXDATAFILES 500
	MAXINSTANCES 5
	ARCHIVELOG
	CHARACTER SET UTF8
	NATIONAL CHARACTER SET UTF8
	DATAFILE '/db/oracle/oradata/MANUAL/system01.dbf' SIZE 1000M EXTENT MANAGEMENT LOCAL
	SYSAUX DATAFILE '/db/oracle/oradata/MANUAL/sysaux01.dbf' SIZE 1000M
	UNDO TABLESPACE UNDOTS DATAFILE '/db/oracle/oradata/MANUAL/undo.dbf' SIZE 500M
	DEFAULT TEMPORARY TABLESPACE TEMP TEMPFILE '/db/oracle/oradata/MANUAL/temp.dbf' SIZE 500M;

### 8. 运行必要的sql脚本(注意按以下顺序)

	/db/oracle/product/10.2.0/db_1/rdbms/admin/catalog.sql
	/db/oracle/product/10.2.0/db_1/rdbms/admin/catproc.sql

### 9. 创建相关表空间和用户
	
	create tablespace users datafile '/db/oracle/oradata/MANUAL/users01.dbf' size 500M;
	create tablespace indexes datafile '/db/oracle/oradata/MANUAL/index01.dbf' size 500M;

建立测试用户

	create user dylan identified by 000000 default tablespace users;
	grant connect,resource to dylan;

### 10. 改为spfile启动

	create spfile from pfile;

重启数据库，并运行show parameter spfile，确认启动的参数文件类型。

### 11. Windows客户端测试

tnsnames.ora配置：

	MANUAL =
	  (DESCRIPTION =
	    (ADDRESS = (PROTOCOL = TCP)(HOST = dev.egolife.com)(PORT = 1521))
	    (CONNECT_DATA =
	      (SERVER = DEDICATED)
	      (SERVICE_NAME = MANUAL.egolife.com )
	    )
	  )

运行tnsping MANUAL命令，并使用sqlplus进行连接测试。

## 参考

* [Manually Creating an Oracle Database](http://docs.oracle.com/cd/B19306_01/server.102/b14231/create.htm#sthref220)
* [Linux下手工新建数据库](http://blog.csdn.net/tianlesoftware/article/details/4680213
