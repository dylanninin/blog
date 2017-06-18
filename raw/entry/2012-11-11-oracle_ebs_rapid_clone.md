---
layout: post
title: Oracle EBS Rapid Clone
category : Oracle
tags : [Oracle, Database, DBA,  EBS]
---

## 克隆环境

* OS: IBM AIX 5.3 64bit
* EBS: 11.5.10.2 64bit
* DB: 9.2.0.6 64bit

ERPProd和ERPTest环境一样，在硬件方面ERPTest配置稍低

## 准备工作

关闭克隆目标系统的数据库、应用等。目前ERP环境采用定期克隆，这里还需要删除克隆目标系统上以前的数据

1)关闭测试环境应用、监听、数据库

	--testmgr
	adstpall.sh apps/xxxxxx

	--testora
	addlnctl.sh stop ERP
	addbctl.sh stop immediate

2)删除测试环境数据

	--testora
	rm -rf /u2/TEST/testora/testdata /u2/TEST/testora/testdb &
	--testora
	rm -f /erpdata/redodata/redo*.dbf

	--testmgr
	rm -rf /u2/TEST/testmgr/testappl /u2/TEST/testmgr/testora &

3)删除测试环境上一次克隆时做的备份

	--testmgr
	cd /u2/TEST/testmgr/testcomn
	rm -rf _pages_120422bk &
	rm -rf html_120422bk &
	rm -rf java_120422bk &
	rm -rf clone_120422bk & 
	rm -rf util_120422bk &

4)备份测试环境上一次克隆的数据

	--testmgr
	mv /u2/TEST/testmgr/testcomn/_pages /u2/TEST/testmgr/testcomn/_pages_120527bk
	mv /u2/TEST/testmgr/testcomn/html /u2/TEST/testmgr/testcomn/html_120527bk
	mv /u2/TEST/testmgr/testcomn/java /u2/TEST/testmgr/testcomn/java_120527bk
	mv /u2/TEST/testmgr/testcomn/clone /u2/TEST/testmgr/testcomn/clone_120527bk
	mv /u2/TEST/testmgr/testcomn/util /u2/TEST/testmgr/testcomn/util_120527bk

## 2.正式克隆

在执行rapid clone时，会从原系统创建克隆用的模板配置文件，当原系统文件复制到目标 系统时，rapid clone工具将使用目标心痛的配置来更新这些模板配置文件，达到克隆出另 外一套系统的目的。

1)关闭应用、监听、数据库
	
	--prodmgr
	adstpall.sh apps/xxxxxx
	--prodora
	addlnctl.sh stop PROD
	addbctl.sh stop immediate

2)数据库预克隆

	--prodora
	cd /u1/PROD/prodora/proddb/9.2.0/appsutil/scripts/PROD_erpprod
	perl adpreclone.pl dbTier

3)应用预克隆

	--prodmgr
	cd /u1/PROD/prodmgr/prodcomn/admin/scripts/PROD_erpprod
	perl adpreclone.pl appsTier

4)关闭原系统数据

因克隆后，数据库已经开启，再次关闭db

	--prodora
	addbctl.sh stop immediate

5)拷贝原系统数据到目标系统

目前ERP正式、测试环境使用AIX 5.3操作系统，共用磁阵，拷贝数据可以采用挂载文件系统 的方式进行

卸载正式环境上/u1文件系统

	--root@prod
	fuser -u /dev/fslv00
	umount /u1
	varyoffvg prodvg

挂载/u1到测试环境

	--root@test
	varyonvg prodvg
	mount /u1

复制原系统数据到目标系统

	--root@test
	cp -hrf /u1/PROD/prodora/proddb /u2/TEST/testora/testdb &
	cp -hrf /u1/PROD/prodora/proddata /u2/TEST/testora/testdata &
	cp -hrf /u1/PROD/prodmgr/prodappl /u2/TEST/testmgr/testappl &
	cp -hrf /u1/PROD/prodmgr/prodora /u2/TEST/testmgr/testora &
	
	cp -hrf /u1/PROD/prodmgr/prodcomn/_pages /u2/TEST/testmgr/testcomn/_pages &
	cp -hrf /u1/PROD/prodmgr/prodcomn/html /u2/TEST/testmgr/testcomn/html &
	cp -hrf /u1/PROD/prodmgr/prodcomn/java /u2/TEST/testmgr/testcomn/java &
	cp -hrf /u1/PROD/prodmgr/prodcomn/util /u2/TEST/testmgr/testcomn/util &
	cp -hrf /u1/PROD/prodmgr/prodcomn/clone /u2/TEST/testmgr/testcomn/clone &

检查复制数据任务是否完成
	
	--root@test
	jobs 或 ps -ef|grep cp

复制完成后，测试环境上卸载/u1，并将/u1挂载至原系统

	--root@test
	unmount /u1
	varyoffvg prodvg
	
	--root@prod
	varyonvg prodvg
	mount /u1

开启原系统数据库、应用等，使应用正常提供服务

开启DB、监听

	--prodora
	adautocfg.sh

备份jserv.properties文件

	--prodmgr
	cp /u1/PROD/prodmgr/prodora/iAS/Apache/Jserv/etc/jserv.properties /u1/PROD/prodmgr/prodora/iAS/Apache/Jserv/etc/jserv.properties.dist
	adautocfg.sh
	
正式环境加上第三方jar包
开启应用

	--prodmgr
	adstrtal.sh apps/xxxxxx

## 3.配置目标系统

配置目标系统，主要是运行一些配置命令，设置目标系统的sid，路径，端口等

1)更改文件所属用户组

	--root@test
	chown -R testora:dba /u2/TEST/testora/testdb /u2/TEST/testora/testdata &
	chown -R testmgr:dba /u2/TEST/testmgr/testora /u2/TEST/testmgr/testcomn /u2/TEST/testmgr/testappl &

2)配置重做日志

原系统中新增了重做日志组，路径/erpdata/redodata

复制重做日志

	su - testora

切换时会提示找不到环境文件，属于正常现象(.profile[11]: /u2/TEST/testora/testdb/9.2.0/ERP_erp.env)
复制redolog到/erpdata/redodata下

	cp /u2/TEST/testora/testdata/redo01.dbf /erpdata/redodata
	cp /u2/TEST/testora/testdata/redo02.dbf /erpdata/redodata
	cd /erpdata/redodata
	
更改重做日志组设置

系统中重做日志组更改了路径，此时需要手动更改adcrdb.zip中的配置

	--testora
	cd /u2/TEST/testora/testdb/9.2.0/appsutil/clone/data/stage
	cp adcrdb.zip adcrdb.zip.120527bk
	unzip adcrdb.zip
	Archive: adcrdb.zip
	inflating: adcrdbclone.sql
	inflating: adcrdb.sh 
	inflating: dbfinfo.lst
	
修改redolog路径，共四处

	vi adcrdbclone.sql
	GROUP 1 ('%s_dbhome2%/redo01.dbf', '/erpdata/redodata/redo01.dbf') SIZE 314572800

重新打包adcrdb文件

	zip -o adcrdb.zip adcrdbclone.sql adcrdb.sh dbfinfo.lst

运行orainstRoot.sh脚本
	
	--root@test
	/tmp/orainstRoot.sh

配置和开启数据库层

从原系统克隆复制过来的配置需要根据目标系统进行一些调整，需谨慎

	--testora
	cd /u2/TEST/testora/testdb/9.2.0/appsutil/clone/bin
	perl adcfgclone.pl dbTier
	
	Do you want to use a virtual hostname for the target node (y/n) [n] ?:
	Target instance is a Real Application Cluster (RAC) instance (y/n) [n]:
	Target System database name [PROD]:ERP
	Target system RDBMS ORACLE_HOME directory [/u1/PROD/prodora/proddb/9.2.0]:/u2/TEST/testora/testdb/9.2.0
	Target system utl_file accessible directories list [/usr/tmp, /usr/tmp, /u1/PROD/prodora/proddb/9.2.0/appsutil/outbound/PROD_erpprod]:
	/usr/tmp,/usr/tmp,/u2/TEST/testora/testdb/9.2.0/appsutil/outbound/ERP_erp
	Number of DATA_TOP's on the target system [2]:1
	Target system DATA_TOP 1:/u2/TEST/testora/testdata
	Do you want to preserve the Display set to erpprod:1.0 (y/n) [y] ?:n
	Target system Display [erptest:0.0]::0.0
	Do you want to preserve the port values from the source system on the target system (y/n) [y] ?:n
	Enter the port pool number [0-99]:
	3
	... ...

再次运行orainstRoot.sh脚本

	--root@test
	/tmp/orainstRoot.sh

配置和开启应用层

	--testmgr
	cd /u2/TEST/testmgr/testcomn/clone/bin
	perl adcfgclone.pl appsTier
	
	Do you want to use a virtual hostname for the target node (y/n) [n] ?:
	Target system database SID [PROD]:ERP
	Target system database server node [erpprod]:erp
	Target system database domain name [egolife.com]:
	Does the target system have more than one application tier server node (y/n) [n] ?:
	Is the target system APPL_TOP divided into multiple mount points (y/n) [n] ?:
	Target system APPL_TOP mount point [/u1/PROD/prodmgr/prodappl]:/u2/TEST/testmgr/testappl
	Target system COMMON_TOP directory [/u1/PROD/prodmgr/prodcomn]:/u2/TEST/testmgr/testcomn
	Target system 8.0.6 ORACLE_HOME directory [/u1/PROD/prodmgr/prodora/8.0.6]:/u2/TEST/testmgr/testora/8.0.6
	Target system iAS ORACLE_HOME directory [/u1/PROD/prodmgr/prodora/iAS]:/u2/TEST/testmgr/testora/iAS
	Do you want to preserve the Display set to erpprod:1.0 (y/n) [y] ?:n
	Target system Display [erptest:0.0]::0.0
	Location of the JDK on the target system [/usr/java14]:
	Do you want to preserve the port values from the source system on the target system (y/n) [y] ?:n
	Enter the port pool number [0-99]:
	3
	UTL_FILE_DIR on database tier consists of the following directories.
	
	1. /usr/tmp
	2. /usr/tmp
	3. /usr/tmp
	4. /u2/TEST/testora/testdb/9.2.0/appsutil/outbound/TEST_erptest
	5. /u2/TEST/testora/testdb/9.2.0/appsutil/outbound/TEST_erptest
	6. /usr/tmp
	Choose a value which will be set as APPLPTMP value on the target node [1]:1
	
	
	addisctl.sh version 115.15
	
	/u2/TEST/testmgr/testora/8.0.6/vbroker/bin/osagent
	Started osagent.
	Osagent logs messages to the file /u2/TEST/testmgr/testora/8.0.6/discwb4/util/osagent.log.
	Waiting for OAD to start...
	Started OAD.
	OAD logs messages to the file /u2/TEST/testmgr/testora/8.0.6/discwb4/util/oad.log.
	Discoverer Locator Started.
	Locator logs messages to the file /u2/TEST/testmgr/testora/8.0.6/discwb4/util/locator.log.
	Registering Discoverer Session
	Completed registration of repository_id = IDL:DCISessionManager:1.0
	object_name = erptest.egolife.com_8003OracleDiscovererSession4
	reference data =
	path_name = /u2/TEST/testmgr/testora/8.0.6/discwb4/util/runses.sh
	activation_policy = UNSHARED_SERVER
	args = (length=4)[-session; erptestegolife.com_8003OracleDiscovererSession4; -prefere
	nce; erptest.egolife.com_8003OracleDiscovererPreferences4; ]
	env = NONE
	for OAD on host 10.20.1.14
	Registering the Collector
	Completed registration of repository_id = IDL:DCICollector:1.0
	object_name = erptest.egolife.com_8003OracleDiscovererCollector4
	reference data =
	path_name = /u2/TEST/testmgr/testora/8.0.6/discwb4/util/runcol.sh
	activation_policy = SHARED_SERVER
	args = (length=2)[-collector; erptest.egolife.com_8003OracleDiscovererCollector4; ]
	env = NONE
	for OAD on host 10.20.1.14
	Applying preferences from file : /u2/TEST/testmgr/testora/8.0.6/discwb4/util/pref.txt
	Finished applying preferences
	
	Closing down registry..
	Registry File sync...
	Registering Discoverer Preference Repository
	Completed registration of repository_id = IDL:DCICORBAInterface:1.0
	object_name = erptest.egolife.com_8003OracleDiscovererPreferences4
	reference data =
	path_name = /u2/TEST/testmgr/testora/8.0.6/discwb4/util/runpref.sh
	activation_policy = SHARED_SERVER
	args = (length=2)[-preference; erptest.egolife.com_8003OracleDiscovererPreferences4; ]
	env = NONE
	for OAD on host 10.20.1.14
	
	addisctl.sh: exiting with status 0
	
	
	.end std out.
	
	.end err out.

## 4.完成目标系统最终设置

1)Profile参数设置

更改颜色和Site name

	System profile -> Java Color Scheme : blue
	Site Name : ERP

2)重新配置应用

关闭应用

	--testmgr
	adstpall.sh apps/xxxxxx

运行自动配置脚本

	--testmgr
	adautocfg.sh

删除原系统节点

	-apps
	select * from fnd_nodes ;
	DELETE FROM FND_NODES WHERE NODE_NAME='ERPPROD';

3)更改工作流设置

	--sysadmin
	Administrator -> workflow -> Notification Mailers -> Edit

将PROD改为ERP，用户名密码为testmgr的用户名密码
修改并发管理器的节点名为ERP Standard Manager

4)取消请求

取消所有定期跑的请求，如AIS、报表、定期请求等

5)更改密码

生产环境克隆到测试环境后，为安全起见，必须更改测试环境密码
更改数据库和应用用户密码，在更改密码前，先关闭应用

	--testmgr
	adstpall.sh apps/xxxxxx

运行fndcpass命令，更改密码

	FNDCPASS apps/oldpassword 0 Y system/manager SYSTEM APPLSYS newpassword

更改wdbsvr.app中记录的密码

	vi $IAS_ORACLE_HOME/Apache/modplsql/cfg/wdbsvr.app
	password = newpassword

运行自动配置脚本

	--testmgr
	adautocfg.sh

6)初始化参数设置

关闭数据库

	--testora
	addbctl.sh stop immediate

设置归档参数

	cd /u2/TEST/testora/testdb/9.2.0/dbs
	vi initERP.ora
	
	log_archive_start = true # if you want automatic archiving
	log_archive_dest_1 ='location=/u2/TEST/testora/arclog/'
	log_archive_format ='arch_%t_%s.arc'

开启数据库

	$ sqlplus /nolog
	SQL> conn /as sysdba
	SQL> startup mount pfile='/u2/TEST/testora/testdb/9.2.0/dbs/initERP.ora';
	SQL> alter database archivelog;
	SQL> archive log start;
	SQL> archive log list;
	SQL> alter database open;
	SQL> alter system switch logfile;
	SQL> create spfile from pfile;
	SQL> shutdown immediate
	SQL> startup
	SQL> alter system set sga_max_size = 3000M scope=spfile;
	SQL> shutdown
	SQL> startup

## 5.错误记录

### 1)2012-04-22 出错记录

将testvg挂载到正式环境后复制出现IO错误，重新挂载时出错

	# mount /u2
	Replaying log for /dev/fslv00.
	mount: 0506-324 Cannot mount /dev/fslv00 on /u2: The media is not formatted or the format is not correct.
	0506-342 The superblock on /dev/fslv00 is dirty. Run a full fsck to fix.

解决方法

在测试环境将testvg重新激活，使用fsck修复。复制时将prodvg挂载到测试环境进行复制。
testvg无法挂载到正式环境的原因待查。

	# fsck /u2
	The current volume is: /dev/fslv00
	Primary superblock is valid.
	J2_LOGREDO:log redo processing for /dev/fslv00 
	Primary superblock is valid.
	*** Phase 1 - Initial inode scan
	*** Phase 2 - Process remaining directories
	*** Phase 3 - Process remaining files
	*** Phase 4 - Check and repair inode allocation map
	File system inode map is corrupt; FIX? y
	Superblock marked dirty because repairs are about to be written.
	*** Phase 5 - Check and repair block allocation map
	File system is clean.
	Superblock is marked dirty; FIX? y
	All observed inconsistencies have been repaired.

### 2)2010-11-21 出错记录

	Completed Apply...
	Sun Nov 21 15:30:38 2010
	
	Beginning APPSIAS_ERP registration to central inventory...
	
	ORACLE_HOME NAME : APPSIAS_ERP
	ORACLE_HOME PATH : /u2/TEST/testmgr/testora/iAS
	Using Inventory location in /etc/oraInst.loc
	Log file located at /etc/oraInventory/logs/OracleHomeCloner_11210330.log
	
	ERROR: Registration Failed... Please check log file.
	
	You can rerun this registration with the following script:
	/u2/TEST/testmgr/testappl/admin/out/ERP_erp/regOUI_APPSIAS_ERP.sh
	
	Skipping the starting of services
	INFO : Rapid Clone completed successfully , but the AutoConfig run recorded some errors. 
	Please review the AutoConfig section in the logfile. If required, you can re-run AutoConfig from command line after fixing the problem
	Once Autoconfig issue is fixed , you can start services$ 
	$ /u2/TEST/testmgr/testappl/admin/out/ERP_erp/regOUI_APPSIAS_ERP.sh
	Using Inventory location in /etc/oraInst.loc
	Log file located at /etc/oraInventory/logs/OracleHomeCloner_11210334.log
	Registration failed
	ERRORCODE = 1 ERRORCODE_END

	# cat /etc/oraInventory/logs/OracleHomeCloner_11210340.log|more
	Registering local Oracle Home located at /u2/TEST/testmgr/testora/iAS to central
	oracle inventory
	RC-00126: Update inventory failed. 
	Unable to create a new Oracle Home at /u2/TEST/testmgr/testora/iAS. Oracle Home 
	already exists at this location. Select another location.
	Raised by oracle.apps.ad.clone.util.OracleHomeCloner
	Registering local Oracle Home located at /u2/TEST/testmgr/testora/iAS to central
	oracle inventory
	RC-00126: Update inventory failed. 
	Unable to create a new Oracle Home at /u2/TEST/testmgr/testora/iAS. Oracle Home 
	already exists at this location. Select another location.
	Raised by oracle.apps.ad.clone.util.OracleHomeCloner

解决方法

	mv /tmp/oraInventory /tmp/oraInventory.bk
	/tmp/orainstRoot.sh

## 参考

* Cloning Oracle Applications Release 11i with Rapid Clone
* EBS 11i Creating a Clone using Oracle Application Manager (OAM Clone)
