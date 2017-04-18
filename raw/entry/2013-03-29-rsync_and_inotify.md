---
layout: post
title: Configure Rsync and Inotify on Linux
category : Linux
tags : [Linux, Utilities]
---

## 测试环境

* wxbak.egolife.com CentOS 5.5 	inotify-tools-3.14-1.el5
* nxbak.egolife.com CentOS 5.5  xinetd-2.3.14-10.el5

测试前，先安装好所需要的软件包。测试中，进行了wxbak、nxbak的双向同步测试。

这里仅列出单向测试记录。

* nxbak上安装xinetd服务，充当rsync服务端；
* wxbak上安装inotify-tools，可以实时监测wxbak机上指定文件夹的变化，并触发相应的事件，激活rsync以实时同步文件系统的变化到nxbak机上。
   
具体如下：

![rsync_arch](http://dylanninin.com/assets/images/2013/rsync_arch.png)

## 服务端

### 1.开启rsync服务

编辑	/etc/xinetd.d/rsync文件

	[root@nxbak]# cat /etc/xinetd.d/rsync 
	# default: off
	# description: The rsync server is a good addition to an ftp server, as it \
	#	allows crc checksumming etc.
	service rsync
	{
		disable	= no 
		socket_type     = stream
		wait            = no
		user            = root
		server          = /usr/bin/rsync
		server_args     = --daemon
		log_on_failure  += USERID
	}

将`disable = yes` 改为 `disable = no`

### 2.配置rsync服务

创建/etc/rsyncd.conf

	[root@nxbak]# vim /etc/rsyncd.conf 
	#2012-06-11	dylanninin@gmail.com	settings for rsync server
	#rsync backup side settings
	uid = root 
	gid = root
	use chroot = no
	max connections = 200
	timeout = 600
	strict modes = yes
	port = 873
	pid file = /var/run/rsyncd.pid
	lock file = /var/run/rsyncd.lock
	log file = /var/log/rsyncd.log
	
	#backup fs settings
	[nxbak]
	path = /data/nxbak
	ignore errors
	comment = rsync rman backup
	auth users=oracle
	uid = root
	gid = root
	secrets file = /etc/rsync_server.pwd 
	read only = no
	list = no
	hosts allow = 192.168.1.118
	hosts deny = 0.0.0.0/32	

### 3.密码文件

创建/etc/rsync_server.pwd

	[root@nxbak]# vim /etc/rsync_server.pwd 
	oracle:security

修改权限

	[root@nxbak]# chmod 600 /etc/rsync_server.pwd 
	[root@nxbak]# ll /etc/rsync_server.pwd 
	-rw------- 1 root root 17 Jun 12 11:43 /etc/rsync_server.pwd

## 客户端

### 1.密码文件

	[root@wxbak ]# vim /etc/rsync_client.pwd 
	security

修改权限

	[root@wxbak]# chmod 600 /etc/rsync_client.pwd
	[root@wxbak]# ll /etc/rsync_client.pwd 
	-rw------- 1 root root 10 Jun 12 11:42 /etc/rsync_client.pwd
	
### 2.rsync+inotify脚本

	[root@wxbak ]# cat /apps/scripts/rsync.sh 
	#!/bin/sh
	#abstract:
	#rsync auto sync script
	#2012-06-11	mis_ghb		first_release
	#variables
	current_date=$(date +%Y%m%d_%H%M%S)
	rman_path=/apps/rmanbak
	log_file=/var/log/rsync.log
	
	#rsync
	rsync_server=192.168.1.119
	rsync_user=oracle
	rsync_pwd=/etc/rsync_client.pwd
	rsync_module=nxbak
	#rsync_client password check
	if [ ! -e ${rsync_pwd} ]; then
	   echo -e "rsync client password file ${rsync_pwd} does not exist!"
	   exit 0
	fi
	
	#inotify function
	inotify_fun(){
	    /usr/bin/inotifywait -mrq --timefmt '%d/%m/%y-%H:%M' --format '%T%w%f' \
	-e modify,delete,create,move ${rman_path} | while read file
	   do
	        /usr/bin/rsync -vrtzopg --progress --delete --password-file=${rsync_pwd} ${rman_path} ${rsync_user}@${rsync_server}::${rsync_module}
	   done
	}

	#inotify
	inotify_fun >> ${log_file}  2>&1 &

## 测试

### 1.开启xinetd服务（服务端）

	 [root@nxbak]# service xinetd restart
	Stopping xinetd:                                           [  OK  ]
	Starting xinetd:                                           [  OK  ]
 
查看服务监听状态netstat

	 [root@nxbak]# netstat -nap | grep xinetd
	tcp     0     0 0.0.0.0:873    0.0.0.0:*      LISTEN      5310/xinetd   

或者lsof

	[root@nxbak]# lsof -i:873
	COMMAND  PID USER   FD   TYPE DEVICE SIZE NODE NAME
	xinetd  5310 root    5u  IPv4 597328       TCP *:rsync (LISTEN)

### 2.运行rsync脚本（客户端）

	[root@wxbak ]# /apps/scripts/rsync.sh

查看脚本运行状态

	[root@wxbak ]# ps -ef | grep rsync
	root     29896     1  0 09:42 pts/1    00:00:00 /bin/sh /apps/scripts/rsync.sh
	root     29898 29896  0 09:42 pts/1    00:00:00 /bin/sh /apps/scripts/rsync.sh
	root     29902 18433  0 09:42 pts/1    00:00:00 grep rsync

### 3.变更同步目录（客户端）

	[root@wxbak rmanbak]# pwd
	/apps/rmanbak
	[root@wxbak rmanbak]# touch rsync
	[root@wxbak rmanbak]# touch inotify
	[root@wxbak rmanbak]# ll
	total 1211696
	-rw-r--r-- 1 oracle oinstall       3414 Jun 12 13:46 20120612_134619-inc0.log
	-rw-r--r-- 1 oracle oinstall       3038 Jun 12 13:50 20120612_134935-inc2.log
	-rw-r--r-- 1 oracle oinstall       1664 Jun 12 23:00 20120612_230001-obsolete.log
	-rw-r--r-- 1 oracle oinstall       3240 Jun 12 23:45 20120612_234501-inc2.log
	-rw-r----- 1 oracle oinstall 1112170496 Jun 12 13:46 20120612_inc0_87ndbqle_1_1.bkp
	-rw-r----- 1 oracle oinstall       4096 Jun 12 13:46 20120612_inc0_89ndbqlv_1_1.bkp
	-rw-r----- 1 oracle oinstall      37888 Jun 12 13:49 20120612_inc2_8andbqrg_1_1.bkp
	-rw-r----- 1 oracle oinstall     319488 Jun 12 13:50 20120612_inc2_8bndbqri_1_1.bkp
	-rw-r----- 1 oracle oinstall   11927552 Jun 12 13:50 20120612_inc2_8cndbqsl_1_1.bkp
	-rw-r----- 1 oracle oinstall       7168 Jun 12 13:50 20120612_inc2_8dndbqsn_1_1.bkp
	-rw-r----- 1 oracle oinstall   55731200 Jun 12 23:45 20120612_inc2_8endctnv_1_1.bkp
	-rw-r----- 1 oracle oinstall   47374336 Jun 12 23:45 20120612_inc2_8fndcto0_1_1.bkp
	-rw-r----- 1 oracle oinstall   11927552 Jun 12 23:45 20120612_inc2_8gndctp3_1_1.bkp
	-rw-r----- 1 oracle oinstall       6656 Jun 12 23:45 20120612_inc2_8hndctp6_1_1.bkp
	-rw-r--r-- 1 root   root              0 Jun 13 09:48 inotify
	-rw-r--r-- 1 root   root              0 Jun 13 09:48 rsync

### 4.查看同步效果（服务端）

	[oracle@nxbak rmanbak]$ pwd
	/data/nxbak/rmanbak
	[oracle@nxbak rmanbak]$ ll
	total 1211696
	-rw-r--r-- 1 oracle oinstall       3414 Jun 12 13:46 20120612_134619-inc0.log
	-rw-r--r-- 1 oracle oinstall       3038 Jun 12 13:50 20120612_134935-inc2.log
	-rw-r--r-- 1 oracle oinstall       1664 Jun 12 23:00 20120612_230001-obsolete.log
	-rw-r--r-- 1 oracle oinstall       3240 Jun 12 23:45 20120612_234501-inc2.log
	-rw-r----- 1 oracle oinstall 1112170496 Jun 12 13:46 20120612_inc0_87ndbqle_1_1.bkp
	-rw-r----- 1 oracle oinstall       4096 Jun 12 13:46 20120612_inc0_89ndbqlv_1_1.bkp
	-rw-r----- 1 oracle oinstall      37888 Jun 12 13:49 20120612_inc2_8andbqrg_1_1.bkp
	-rw-r----- 1 oracle oinstall     319488 Jun 12 13:50 20120612_inc2_8bndbqri_1_1.bkp
	-rw-r----- 1 oracle oinstall   11927552 Jun 12 13:50 20120612_inc2_8cndbqsl_1_1.bkp
	-rw-r----- 1 oracle oinstall       7168 Jun 12 13:50 20120612_inc2_8dndbqsn_1_1.bkp
	-rw-r----- 1 oracle oinstall   55731200 Jun 12 23:45 20120612_inc2_8endctnv_1_1.bkp
	-rw-r----- 1 oracle oinstall   47374336 Jun 12 23:45 20120612_inc2_8fndcto0_1_1.bkp
	-rw-r----- 1 oracle oinstall   11927552 Jun 12 23:45 20120612_inc2_8gndctp3_1_1.bkp
	-rw-r----- 1 oracle oinstall       6656 Jun 12 23:45 20120612_inc2_8hndctp6_1_1.bkp
	-rw-r--r-- 1 root   root              0 Jun 13 09:48 inotify
	-rw-r--r-- 1 root   root              0 Jun 13 09:48 rsync

### 5.查看日志

服务端日志

	[root@nxbak]# tail -f /var/log/rsyncd.log 
	2012/06/12 23:46:07 [1633] params.c:Parameter() - Ignoring badly formed line in configuration file: ignore errors
	2012/06/12 23:46:07 [1633] name lookup failed for 192.168.1.118: Temporary failure in name resolution
	2012/06/12 23:46:07 [1633] connect from UNKNOWN (192.168.1.118)
	2012/06/12 23:46:07 [1633] rsync to nxbak from oracle@unknown (192.168.1.118)
	2012/06/12 23:46:07 [1633] sent 69 bytes  received 589 bytes  total size 1239517788
	2012/06/12 23:46:07 [1635] params.c:Parameter() - Ignoring badly formed line in configuration file: ignore errors
	2012/06/12 23:46:07 [1635] name lookup failed for 192.168.1.118: Temporary failure in name resolution
	2012/06/12 23:46:07 [1635] connect from UNKNOWN (192.168.1.118)
	2012/06/12 23:46:07 [1635] rsync to nxbak from oracle@unknown (192.168.1.118)
	2012/06/12 23:46:07 [1635] sent 69 bytes  received 589 bytes  total size 1239517788
	2012/06/13 09:49:06 [5342] params.c:Parameter() - Ignoring badly formed line in configuration file: ignore errors
	2012/06/13 09:49:06 [5342] name lookup failed for 192.168.1.118: Temporary failure in name resolution
	2012/06/13 09:49:06 [5342] connect from UNKNOWN (192.168.1.118)
	2012/06/13 09:49:06 [5342] rsync to nxbak from oracle@unknown (192.168.1.118)
	2012/06/13 09:49:06 [5342] rmanbak/
	2012/06/13 09:49:06 [5342] sent 69 bytes  received 675 bytes  total size 1239517788
	2012/06/13 09:49:12 [5344] params.c:Parameter() - Ignoring badly formed line in configuration file: ignore errors
	2012/06/13 09:49:12 [5344] name lookup failed for 192.168.1.118: Temporary failure in name resolution
	2012/06/13 09:49:12 [5344] connect from UNKNOWN (192.168.1.118)
	2012/06/13 09:49:12 [5344] rsync to nxbak from oracle@unknown (192.168.1.118)
	2012/06/13 09:49:12 [5344] rmanbak/
	2012/06/13 09:49:12 [5344] sent 69 bytes  received 729 bytes  total size 1239517788

客户端日志

	[root@wxbak]tail -f /var/log/rsync.log
	sent 505 bytes  received 16 bytes  1042.00 bytes/sec
	total size is 1239517788  speedup is 2379112.84
	building file list ... 
	16 files to consider
	rmanbak/
	rmanbak/rsync
	           0 100%    0.00kB/s    0:00:00 (xfer#1, to-check=0/16)
	
	sent 591 bytes  received 44 bytes  1270.00 bytes/sec
	total size is 1239517788  speedup is 1951996.52
	building file list ... 
	17 files to consider
	rmanbak/
	rmanbak/inotify
	           0 100%    0.00kB/s    0:00:00 (xfer#1, to-check=1/17)
	
	sent 645 bytes  received 44 bytes  1378.00 bytes/sec
	total size is 1239517788  speedup is 1799009.85

## 异常

昨天在配置rsync时，出现一个新问题，提示`mkdir failed: Permission denied (13)`和`mkstemp failed: Permission`，后来查看Stackoverflow，以及以前的[CentOS 5.5下rsync使用技巧与权限问题解读](http://os.51cto.com/art/201101/243374.htm)，发现可能是开启了SELinux导致的，因对SELinux的权限控制不熟悉，关闭SELinux，rsync即可以正常同步文件、文件夹。

rsync client log

	sending incremental file list
	scripts/checkalert.sh
	        1288 100%    0.00kB/s    0:00:00 (xfer#1, to-check=39/41)
	scripts/checkbak.sh
	        1275 100%    1.22MB/s    0:00:00 (xfer#2, to-check=38/41)
	scripts/cleaner.sh
	         257 100%  250.98kB/s    0:00:00 (xfer#3, to-check=37/41)
	scripts/dailyduty.sh
	        1773 100%    1.69MB/s    0:00:00 (xfer#4, to-check=36/41)
	scripts/full.rman
	         263 100%  256.84kB/s    0:00:00 (xfer#5, to-check=35/41)
	scripts/historycleaner.sh
	        1721 100%    1.64MB/s    0:00:00 (xfer#6, to-check=34/41)
	scripts/inc0.rman
	         287 100%  280.27kB/s    0:00:00 (xfer#7, to-check=33/41)
	scripts/inc1.rman
	         275 100%  268.55kB/s    0:00:00 (xfer#8, to-check=32/41)
	scripts/inc2.rman
	         274 100%  267.58kB/s    0:00:00 (xfer#9, to-check=31/41)
	scripts/inotify
	           0 100%    0.00kB/s    0:00:00 (xfer#10, to-check=30/41)
	scripts/obsolete.rman
	         192 100%  187.50kB/s    0:00:00 (xfer#11, to-check=29/41)
	scripts/rman.sh
	        1256 100%    1.20MB/s    0:00:00 (xfer#12, to-check=28/41)
	scripts/rsync.sh
	         844 100%  824.22kB/s    0:00:00 (xfer#13, to-check=27/41)
	scripts/sql/
	rsync: recv_generator: mkdir "scripts/sql" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.checkalert.sh.J5S0do" (in oa_fs) failed: Permission denied (13)
	*** Skipping any contents from this failed directory ***
	rsync: mkstemp "scripts/.checkbak.sh.evfA21" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.cleaner.sh.L6ccRF" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.dailyduty.sh.cShQFj" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.full.rman.tn4vuX" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.historycleaner.sh.O2mdjB" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.inc0.rman.xLgW7e" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.inc1.rman.kDyGWS" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.inc2.rman.BBHsLw" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.inotify.w68fAa" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.obsolete.rman.ZAO4oO" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.rman.sh.KkEVds" (in oa_fs) failed: Permission denied (13)
	rsync: mkstemp "scripts/.rsync.sh.hp2Q25" (in oa_fs) failed: Permission denied (13)
	
	sent 6010 bytes  received 260 bytes  12540.00 bytes/sec
	total size is 20476  speedup is 3.27
	rsync error: some files/attrs were not transferred (see previous errors) (code 23) at main.c(1039) [sender=3.0.6]
	
rsync server log

	2013/03/28 20:14:58 [12524] connect from oaprod.tp-link.net (172.31.1.90)
	2013/03/28 20:14:58 [12524] rsync to oa_fs/ from oa@oaprod.tp-link.net (172.31.1.90)
	2013/03/28 20:14:58 [12524] receiving file list
	2013/03/28 20:14:58 [12524] rsync: recv_generator: mkdir "scripts/sql" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] *** Skipping any contents from this failed directory ***
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.checkalert.sh.vOJStU" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.checkbak.sh.kpYRTQ" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.cleaner.sh.LwyTjN" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.dailyduty.sh.2ZJWJJ" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.full.rman.f3w29F" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.historycleaner.sh.K1tbAC" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.inc0.rman.lGzm0y" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.inc1.rman.2cSzqv" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.inc2.rman.VFAOQr" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.obsolete.rman.4WV6go" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.rman.sh.phPqHk" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] rsync: mkstemp "scripts/.rsync.sh.kslM7g" (in oa_fs) failed: Permission denied (13)
	2013/03/28 20:14:58 [12524] sent 1546 bytes  received 6003 bytes  total size 20476

Stackoverflow

Even though you got this working, I recently had a similar encounter and no SO or google searching was any help as they all dealt with basic permission issues wheres the solution below is somewhat of an off setting that you would even think to check in most situations.

One thing to check for with permission denied that I recently found having issues with rsync myself where permissions were exactly the same on both servers including the owner and group but rsync transfers worked one way on one server but not the other way.

It turned out the server with problems that I was getting permission denied from had SELinux enabled which in turn overrides POSIX permissions on files/folders. So even though the folder in question could of been 777 with root running the command SELinux was enabled and would in turn overwrite those permissions and was producing a permission denied error with rsync.

You can run the command getenforce to see if SELinux is enabled on the machine.

In my situation I ended up just disabling SELINUX completely because it wasn't needed and already disabled on the server that was working fine and just caused problems being enabled. To disable, open `/etc/selinux/config` and set `SELINUX=disabled`. To temporarily disable you can run the command `setenforce 0` which will set SELinux into a permissive state rather then enforcing state which causes it to print warnings instead of enforcing.

## 参考

* [Inotify](http://en.wikipedia.org/wiki/Inotify)
* [Inotify: Efficient, Real-Time Linux File System Event Monitoring](http://www.infoq.com/articles/inotify-linux-file-system-event-monitoring)
* [Security-Enhanced Linux](http://en.wikipedia.org/wiki/Security-Enhanced_Linux)
* [SELinux](http://wiki.centos.org/HowTos/SELinux)
* [rsync-mkstemp-failed-permission-denied-13](http://stackoverflow.com/questions/11039559/rsync-mkstemp-failed-permission-denied-13)
* [CentOS 5.5下rsync使用技巧与权限问题解读](http://os.51cto.com/art/201101/243374.htm)
* [rsync日常维护](http://dylanninin.com/blog/2012/10/26/rsync_exception.html)
