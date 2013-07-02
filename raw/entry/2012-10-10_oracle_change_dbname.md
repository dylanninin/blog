#写在前面的话
因新项目开发需要，现需建立新的测试数据库。但目前测试服务器没有到位，故暂且使用以前的测试机代替，其中安装的Oracle数据库仅作学习测试使用，数据库名、实例名均为dbtest。现在将此数据库的数据库名、实例名从dbtest改为CRMTEST。

以下是更改记录，以作备忘。

#测试环境

* 操作系统：CentOS 5.5 
* 数据库: Oracle Database 10.2.0.1.0

#主要步骤
##1. 先更改dbname
修改oracle数据库的dbid和dbname，主要步骤如下：

* 1)将数据库启动到mount状态：`startup mount`;
* 2)使用nid命令修改：`nid target=/ DBNAME=CRMTEST`
* 3)更改初始化参数文件中的`db_name`：`db_name="CRMTEST"`
* 4)启动到mount：`startup mount`
* 5)以resetlogs打开数据库：`alter database open resetlogs`;

###1)重启数据库到mount
查看当前数据库names设置：

	SQL> show parameter name
	NAME                       TYPE      VALUE
	-------------------------- --------- ------------------------------
	db_file_name_convert       string
	db_name                    string    dbtest
	db_unique_name             string    dbtest
	global_names               boolean   FALSE
	instance_name              string    dbtest
	lock_name_space            string
	log_file_name_convert      string
	service_names              string    dbtest

查看当前数据库启动参数类型：

	SQL> show parameter spfile
	NAME                       TYPE      VALUE
	-------------------------- --------- ------------------------------
	spfile                     string     /db/oracle/product/10.2.0/db_1/
	                                      dbs/spfiledbtest.ora
	
从spfile创建pfile，便于直接编辑参数文件：

	SQL> create pfile from spfile;
	File created.
	
关闭数据库：

	SQL> shutdown immediate
	Database closed.
	Database dismounted.
	ORACLE instance shut down.

启动数据库到mount状态：

	SQL> startup mount;
	ORACLE instance started.
	Total System Global Area 603979776 bytes
	Fixed Size 1220796 bytes
	Variable Size 163581764 bytes
	Database Buffers 432013312 bytes
	Redo Buffers 7163904 bytes
	Database mounted.

###2)运行nid,更改dbname和dbid
nid即new database id，根据dbname生成新的dbid：

	[oracle@shoptest dbs]$ nid target=/ dbname=CRMTEST
	DBNEWID: Release 10.2.0.1.0 - Production on Tue Oct 9 20:02:52 2012
	Copyright (c) 1982, 2005, Oracle. All rights reserved.
	Connected to database DBTEST (DBID=1176995883)
	Connected to server version 10.2.0
	Control Files in database:
	/db/oracle/oradata/dbtest/control01.ctl
	/db/oracle/oradata/dbtest/control02.ctl
	/db/oracle/oradata/dbtest/control03.ctl
	Change database ID and database name DBTEST to CRMTEST? (Y/[N]) => y
	Proceeding with operation
	Changing database ID from 1176995883 to 889633516
	Changing database name from DBTEST to CRMTEST
	Control File /db/oracle/oradata/dbtest/control01.ctl - modified
	Control File /db/oracle/oradata/dbtest/control02.ctl - modified
	Control File /db/oracle/oradata/dbtest/control03.ctl - modified
	Datafile /db/oracle/oradata/dbtest/system01.dbf - dbid changed, wrote new name
	Datafile /db/oracle/oradata/dbtest/undotbs01.dbf - dbid changed, wrote new name
	Datafile /db/oracle/oradata/dbtest/sysaux01.dbf - dbid changed, wrote new name
	Datafile /db/oracle/oradata/dbtest/users01.dbf - dbid changed, wrote new name
	Datafile /db/oracle/oradata/dbtest/crm_data01.dbf - dbid changed, wrote new name
	Datafile /db/oracle/oradata/dbtest/crm_index01.dbf - dbid changed, wrote new name
	Datafile /db/oracle/oradata/dbtest/temp01.dbf - dbid changed, wrote new name
	Datafile /db/oracle/oradata/dbtest/crm_temp01.dbf - dbid changed, wrote new name
	Control File /db/oracle/oradata/dbtest/control01.ctl - dbid changed, wrote new name
	Control File /db/oracle/oradata/dbtest/control02.ctl - dbid changed, wrote new name
	Control File /db/oracle/oradata/dbtest/control03.ctl - dbid changed, wrote new name
	Instance shut down
	Database name changed to CRMTEST.
	Modify parameter file and generate a new password file before restarting.
	Database ID for database CRMTEST changed to 889633516.
	All previous backups and archived redo logs for this database are unusable.
	Database is not aware of previous backups and archived logs in Recovery Area.
	Database has been shutdown, open database with RESETLOGS option.
	Succesfully changed database name and ID.
	DBNEWID - Completed succesfully.

###3)更改initdbtest.ora，将db_name设置为CRMTEST
进入到$ORACLE_HOME/dbs目录：

	[oracle@shoptest dbs]$ pwd
	/db/oracle/product/10.2.0/db_1/dbs

更改db_name参数，改为CRMTEST：

	[oracle@shoptest dbs]$ vim initdbtest.ora
	... ...
	*.db_name='CRMTEST'
	... ...

###4)以initdbtest.ora启动数据库到mount状态

	SQL> startup mount pfile='/db/oracle/product/10.2.0/db_1/dbs/initdbtest.ora';
	ORACLE instance started.
	Total System Global Area 603979776 bytes
	Fixed Size 1220796 bytes
	Variable Size 163581764 bytes
	Database Buffers 432013312 bytes
	Redo Buffers 7163904 bytes
	Database mounted.

###5)以resetlogs开启数据库

	SQL> alter database open resetlogs;
	Database altered.

查看当前数据库的names：

	SQL> show parameter name
	NAME                       TYPE      VALUE
	-------------------------- --------- --------------------
	db_file_name_convert       string
	db_name                    string    CRMTEST
	db_unique_name             string    dbtest
	global_names               boolean 	 FALSE
	instance_name              string    dbtest
	lock_name_space            string
	log_file_name_convert      string
	service_names              string    dbtest

到这里，已经将`dbname`从dbtest更改为CRMTEST，但`instance_name`还是dbtest，接下来将`intance_name`更改为CRMTEST。
其他的如`db_unique_name`，`service_names`同样更改为CRMTEST。

##2. 再更改`instance_name`
更改数据库的`instance_name`，主要步骤如下：

* 1)创建新的密码文件：`orapwd`
* 2)创建新的初始化参数文件:`cp init<SID>.ora to init<NEW_SID>.ora`，并作修改
* 3)以新的初始化参数文件启动数据库：`startup pfile='?/dbs/init<NEW_SID>.ora`
* 4)更改数据库以spfile启动:`create spfile from pfile`
* 5)修改监听：`vim $ORACLE_HOME/network/admin/listener.ora`

###1)创建新的密码文件orapwCRMTEST

	[oracle@shoptest dbs]$ pwd
	/db/oracle/product/10.2.0/db_1/dbs
	[oracle@shoptest dbs]$ orapwd file=orapwCRMTEST password=oracle entries=5
	[oracle@shoptest dbs]$ ll
	total 7252
	-rw-r----- 1 oracle oinstall 1544 Oct 9 20:20 hc_dbtest.dat
	-rw-r--r-- 1 oracle oinstall 1436 Oct 9 20:04 initdbtest.ora
	-r--r--r-- 1 oracle oinstall 982 May 24 15:20 initdbtest.ora.dist
	-rw-r----- 1 oracle oinstall 12920 May 3 2001 initdw.ora
	-rw-r----- 1 oracle oinstall 8385 Sep 11 1998 init.ora
	-rw-r----- 1 oracle oinstall 24 May 24 14:43 lkDBTEST
	-rw-r----- 1 oracle oinstall 2048 Oct 9 20:23 orapwCRMTEST
	-rw-r----- 1 oracle oinstall 1536 Sep 21 19:31 orapwdbtest
	-rw-r----- 1 oracle oinstall 7356416 Oct 9 20:06 snapcf_dbtest.f
	-rw-r----- 1 oracle oinstall 3584 Oct 9 20:17 spfiledbtest.ora

###2)创建initCRMTEST.ora文件，设置相关参数
拷贝initdbtest.ora到initCRMTEST.ora：
	
	[oracle@shoptest dbs]$ cp initdbtest.ora initCRMTEST.ora

更改initCRMTEST.ora文件，主要是instance_name，db_unique_name，dispatcher等：

	[oracle@shoptest dbs]$ vim initCRMTEST.ora 
	CRMTEST.__db_cache_size=432013312
	CRMTEST.__java_pool_size=4194304
	CRMTEST.__large_pool_size=4194304
	CRMTEST.__shared_pool_size=155189248
	CRMTEST.__streams_pool_size=0
	... ...
	*.db_name='CRMTEST'
	*.db_unique_name='CRMTEST'
	*.dispatchers='(PROTOCOL=TCP) (SERVICE=CRMTESTXDB)'
	... ...

###3)以initCRMTEST.ora启动数据库
因实例名已经从dbtest改为CRMTEST，需重新设置`ORACLE_SID`：

	[oracle@shoptest dbs]$ export ORACLE_SID=CRMTEST

以initCRMTEST.ora重启数据库：

	SQL> conn /as sysdba
	Connected.
	SQL> shutdown immediate;
	Database closed.
	Database dismounted.
	ORACLE instance shut down.
	SQL> startup pfile='/db/oracle/product/10.2.0/db_1/dbs/initCRMTEST.ora';
	ORACLE instance started.
	Total System Global Area 603979776 bytes
	Fixed Size 1220796 bytes
	Variable Size 163581764 bytes
	Database Buffers 432013312 bytes
	Redo Buffers 7163904 bytes
	Database mounted.
	Database opened.

查看当前数据库的names
	
	SQL> show parameter name
	NAME                        TYPE      VALUE
	--------------------------- --------- ------------------
	db_file_name_convert        string
	db_name                     string    CRMTEST
	db_unique_name              string    CRMTEST
	global_names                boolean   FALSE
	instance_name               string    CRMTEST
	lock_name_space             string
	log_file_name_convert       string
	service_names               string    dbtest

###4)创建spfile，并以spfile重启数据库
从pfile创建spfile：

	SQL> create spfile from pfile;
	File created.

关闭数据库：

	SQL> shutdown immediate;
	Database closed.
	Database dismounted.
	ORACLE instance shut down.

启动数据库：

	SQL> startup;
	ORACLE instance started.
	Total System Global Area 603979776 bytes
	Fixed Size 1220796 bytes
	Variable Size 163581764 bytes
	Database Buffers 432013312 bytes
	Redo Buffers 7163904 bytes
	Database mounted.
	Database opened.

确认当前数据库使用的参数文件类型：


	SQL> show parameter spfile;
	NAME                       TYPE     VALUE
	-------------------------- -------- ------------------------------
	spfile                     string   /db/oracle/product/10.2.0/db_1/
										dbs/spfileCRMTEST.ora

更改service_names：

	SQL> alter system set service_names=CRMTEST;
	
	System altered.

再次查看当前数据库的names：
	
	SQL> show parameter name
	NAME                        TYPE      VALUE
	--------------------------- --------- ------------------
	db_file_name_convert        string
	db_name                     string    CRMTEST
	db_unique_name              string    CRMTEST
	global_names                boolean   FALSE
	instance_name               string    CRMTEST
	lock_name_space             string
	log_file_name_convert       string
	service_names               string    CRMTEST

查看当前数据库的归档模式：

	SQL> archive log list;
	Database log mode Archive Mode
	Automatic archival Enabled
	Archive destination USE_DB_RECOVERY_FILE_DEST
	Oldest online log sequence 1
	Next log sequence to archive 1
	Current log sequence 1
	
###5)修改并重启监听
修改监听中的`SID_NAME`和`GLOBAL_DBNAME`：
	
	[oracle@shoptest admin]$ vim listener.ora
	# listener.ora Network Configuration File: /db/oracle/product/10.2.0/db_1/network/admin/listener.ora
	# Generated by Oracle configuration tools.
	
	SID_LIST_LISTENER =
	    (SID_LIST =
	        (SID_DESC =
	            (SID_NAME = PLSExtProc)
	            (ORACLE_HOME = /db/oracle/product/10.2.0/db_1)
	            (PROGRAM = extproc)
	        )
	        (SID_DESC =
	            (GLOBAL_DBNAME= CRMTEST)
	            (ORACLE_HOME = /db/oracle/product/10.2.0/db_1)
	            (SID_NAME = CRMTEST)
	        )
	    )
	
	LISTENER =
	    (DESCRIPTION_LIST =
	        (DESCRIPTION =
	            (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1))
	            (ADDRESS = (PROTOCOL = TCP)(HOST = shoptest.egolife.com)(PORT = 1521))
	        )
	)

重启监听：

	[oracle@shoptest admin]$ lsnrctl start
	LSNRCTL for Linux: Version 10.2.0.1.0 - Production on 10-OCT-2012 19:52:12
	Copyright (c) 1991, 2005, Oracle. All rights reserved.
	Starting /db/oracle/product/10.2.0/db_1/bin/tnslsnr: please wait...
	
	TNSLSNR for Linux: Version 10.2.0.1.0 - Production
	System parameter file is /db/oracle/product/10.2.0/db_1/network/admin/listener.ora
	Log messages written to /db/oracle/product/10.2.0/db_1/network/log/listener.log
	Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1)))
	Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=shoptest.egolife.com)(PORT=1521)))
	
	Connecting to (DESCRIPTION=(ADDRESS=(PROTOCOL=IPC)(KEY=EXTPROC1)))
	STATUS of the LISTENER
	------------------------
	Alias LISTENER
	Version TNSLSNR for Linux: Version 10.2.0.1.0 - Production
	Start Date 10-OCT-2012 19:52:13
	Uptime 0 days 0 hr. 0 min. 0 sec
	Trace Level off
	Security ON: Local OS Authentication
	SNMP OFF
	Listener Parameter File /db/oracle/product/10.2.0/db_1/network/admin/listener.ora
	Listener Log File /db/oracle/product/10.2.0/db_1/network/log/listener.log
	Listening Endpoints Summary...
	(DESCRIPTION=(ADDRESS=(PROTOCOL=ipc)(KEY=EXTPROC1)))
	(DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=shoptest.egolife.com)(PORT=1521)))
	Services Summary...
	Service "CRMTEST" has 1 instance(s).
	Instance "CRMTEST", status UNKNOWN, has 1 handler(s) for this service...
	Service "PLSExtProc" has 1 instance(s).
	Instance "PLSExtProc", status UNKNOWN, has 1 handler(s) for this service...
	The command completed successfully

最后，注意更改bash环境变量，设置`ORACLE_SID=CRMTEST`，之前使用`export ORACLE_SID=CRMTEST`仅对当前的用户有效

	[oracle@shoptest admin]$ vim ~/.bash_profile
	... ...
	export ORACLE_SID=CRMTEST
	... ...



#测试和确认
这样数据库的`instance_name`就更改完成，下面进行一些简单的测试，确认更改成功，主要测试一下几个方面：
* 监听正常，可以接收连接请求：tnsping crmtest
* 密码文件生效：conn sys@crmtest /as sysdba

##1. 监听测试
###服务器端连接测试
配置tnsnames.ora：

	[oracle@shoptest admin]$ vim tnsnames.ora
	CRMTEST =
	    (DESCRIPTION =
	        (ADDRESS = (PROTOCOL = TCP)(HOST = shoptest.egolife.com)(PORT = 1521))
	        (CONNECT_DATA =
	            (SERVER = DEDICATED)
	            (SERVICE_NAME = CRMTEST)
	        )
	    )
	
	EXTPROC_CONNECTION_DATA =
	    (DESCRIPTION =
	        (ADDRESS_LIST =
	            (ADDRESS = (PROTOCOL = IPC)(KEY = EXTPROC1))
	        )
	        (CONNECT_DATA =
	            (SID = PLSExtProc)
	           (PRESENTATION = RO)
	        )
	    )

使用tnsping，测试crmtest连接是否正常：
	
	[oracle@shoptest admin]$ tnsping crmtest
	TNS Ping Utility for Linux: Version 10.2.0.1.0 - Production on 10-OCT-2012 19:54:31
	Copyright (c) 1997, 2005, Oracle. All rights reserved.
	
	Used parameter files:
	/db/oracle/product/10.2.0/db_1/network/admin/sqlnet.ora
	
	Used TNSNAMES adapter to resolve the alias
	Attempting to contact (DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = shoptest.egolife.com)(PORT = 1521)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = CRMTEST)))
	OK (0 msec)

###Windows客户端连接测试
同样，先配置tnsnames.ora，然后运行tnsping crmtest，确认是否可以连接：

	C:\> tnsping crmtest
	TNS Ping Utility for 32-bit Windows: Version 11.2.0.1.0 - Production on 10-10月-2012 20:09:57
	Copyright (c) 1997, 2010, Oracle. All rights reserved.
	
	已使用的参数文件:
	D:\Oracle\11g\product\11.2.0\db_1\network\admin\sqlnet.ora
	
	已使用 TNSNAMES 适配器来解析别名
	尝试连接 (DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = shoptest.egolife.com)(PORT = 1521)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = CRMTEST)))
	OK (0 毫秒)

##2. orapwCRMTEST密码文件生效测试
再使用sqlplus以sysdba身份登录，检查密码文件是否生效：

	C:\>sqlplus /nolog
	SQL*Plus: Release 11.2.0.1.0 Production on 星期三 10月 10 20:11:38 2012
	Copyright (c) 1982, 2010, Oracle. All rights reserved.
	SQL> conn sys@crmtest/as sysdba
	输入口令:
	已连接。
	SQL>

#参考

* [Oracle 修改DB_NAME 和 DBID](http://blog.csdn.net/tianlesoftware/article/details/6087641)
* [如何修改数据库实例名](http://oonicedream.itpub.net/post/36905/457005)