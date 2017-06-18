---
layout: post
title: Rsync Exception
category : Linux
tags : [Linux, Oracle, Exception]
---

[rsync](http://en.wikipedia.org/wiki/Rsync)是Unix/Linux下同步文件的一个高效算法， 它能同步更新两处计算机的文件与目录，并适当利用查找文件中的不同块以减少数据传输。 rsync中一项与其他大部分类似程序或协定中所未见的重要特性是镜像是只对有变更的部分 进行传送。rsync可拷贝/显示目录属性，以及拷贝文件，并可选择性的压缩以及递归拷贝， 同步速度快。

本文主要是记录在工作中使用rsync进行远程同步时遇到的问题及其解决方案，同时向大家 推荐关于rsync的两篇博客，一篇是酷壳陈皓的[rsync的核心算法](http://coolshell.cn/articles/7425.html)； 另一篇是51CTO上[抚琴煮酒的CentOS 5.5 下 rsync使用技巧与权限问题解读](http://os.51cto.com/art/201101/243374.htm)。

## 环境

主机

	192.168.0.30 any.egolife.com  
	提供数据库服务，并部署rman增量备份
	使用inotify和rsync实时同步rman备份到备机，为rsync客户端

备机

	192.168.0.29 anybak.egolife.com
	部署数据库，配置与主机相同，但不提供数据库服务，仅在主机宕机时进行rman异机恢复
	部署rsync服务，为rsync服务端

以下是一次使用rsync出现异常的维护记录。

## 第一次同步异常

查看某一系统主机和备机，发现2012-8-7的备份未进行同步，查看日志rsync连接异常，并手动进行测试。

rsync服务端输出日志如下

	[root@anybak rmanbak]# tail -f /var/log/rsyncd.log
	2012/08/08 09:18:05 [9301] params.c:Parameter() - Ignoring badly formed line in configuration file: ignore errors
	2012/08/08 09:18:05 [9301] name lookup failed for 192.168.0.30: Temporary failure in name resolution
	2012/08/08 09:18:05 [9301] connect from UNKNOWN (192.168.0.30)
	2012/08/08 09:18:05 [9301] rsync to anbak from oracle@unknown (192.168.0.30)
	2012/08/08 09:18:05 [9301] rmanbak/
	2012/08/08 09:18:28 [9301] inflate (token) returned -5
	2012/08/08 09:18:28 [9301] rsync error: error in rsync protocol data stream (code 12) at token.c(478) [receiver=2.6.8]
	2012/08/08 09:18:28 [9301] rsync: connection unexpectedly closed (2097 bytes received so far) [generator]
	2012/08/08 09:18:28 [9301] rsync error: error in rsync protocol data stream (code 12) at io.c(463) [generator=2.6.8]

### 1.ignore errors 

查看`/etc/rsyncd.conf`，配置了ignore errors，注释掉即可；ignore errors 可以忽略掉一些无关的IO错误。

### 2.name lookup failed for 192.168.0.30: Temporary failure in name resolution

rsync 启用了DNS反向解析，查询不到时，可能需要花很长时间。 在`/etc/hosts`文件中，添加`192.168.0.30 any.egolife.com` 配置重新启动rynsc服务和客户端脚本，即可正常同步。

## 第二次同步异常

查看某一系统主机和备机，发现2012-9-25的备份未进行同步。

rsync客户端日志

	inflate (token) returned -5
	rsync: connection unexpectedly closed (229751 bytes received so far) [sender]
	rsync error: error in rsync protocol data stream (code 12) at io.c(463) [sender=2.6.8]

rsync服务端日志

	[root@anybak ~]# tail -f /var/log/rsyncd.log 
	2012/09/25 16:57:27 [8694] connect from any.egolife.com (192.168.0.30)
	2012/09/25 16:57:27 [8694] rsync to anybak from oracle@any.egolife.com (192.168.0.30)
	2012/09/25 16:57:27 [8694] rmanbak/
	2012/09/25 16:57:50 [8694] inflate (token) returned -5
	2012/09/25 16:57:50 [8694] rsync error: error in rsync protocol data stream (code 12) at token.c(478) [receiver=2.6.8]
	2012/09/25 16:57:50 [8694] rsync: connection unexpectedly closed (2096 bytes received so far) [generator]
	2012/09/25 16:57:50 [8694] rsync error: error in rsync protocol data stream (code 12) at io.c(463) [generator=2.6.8]

还是出现了上次出现过的异常。在网上搜索后，发现可能是rsync 2.6.8的bug，因传输的文件太多太大，此时需要升级rsync版本。

查看当前rsync版本

	[root@any rmanbak]# rpm -qa | grep rsync
	rsync-2.6.8-3.1
	
	[root@any rmanbak]# mount 192.168.1.100:/media/centos/5.7_64/1 /media/
	[root@any rmanbak]# rpm -ihv /media/CentOS/rsync-3.0.6-4.el5.x86_64.rpm
	warning: /media/CentOS/rsync-3.0.6-4.el5.x86_64.rpm: Header V3 DSA signature: NOKEY, key ID e8562897
	Preparing... ########################################### [100%]
	1:rsync ########################################### [100%]

### 升级版本之后，仍有错误信息。

rsync客户端日志

	rsync: writefd_unbuffered failed to write 4 bytes to socket [sender]: Connection reset by peer (104)
	inflate (token) returned -5
	rsync error: error in rsync protocol data stream (code 12) at token.c(604) [receiver=3.0.6]
	rsync: connection unexpectedly closed (229747 bytes received so far) [sender]
	rsync error: error in rsync protocol data stream (code 12) at io.c(600) [sender=3.0.6]

rsync服务端日志

	2012/09/25 17:29:21 [9026] connect from any.egolife.com (192.168.0.30)
	2012/09/25 17:29:21 [9026] rsync to anybak from oracle@any.egolife.com (192.168.0.30)
	2012/09/25 17:29:21 [9026] receiving file list
	2012/09/25 17:29:21 [9026] rmanbak/
	2012/09/25 17:29:44 [9026] inflate (token) returned -5
	2012/09/25 17:29:44 [9026] rsync error: error in rsync protocol data stream (code 12) at token.c(604) [receiver=3.0.6]
	2012/09/25 17:29:44 [9026] rsync: connection unexpectedly closed (2017 bytes received so far) [generator]
	2012/09/25 17:29:44 [9026] rsync error: error in rsync protocol data stream (code 12) at io.c(600) [generator=3.0.6]

升级之后，可能还是传输的文件太大所导致的。

根据网上搜索到的文档，在rsync命令中加入参数 --no-iconv，重启后，客户端日志信息如下：

	sending incremental file list
	rmanbak/
	rmanbak/20120917_inc0_tfnlf4ok_1_1.bkp
	1052737280 22% 47.78MB/s 0:01:13
	rsync: writefd_unbuffered failed to write 4 bytes to socket [sender]: Connection reset by peer (104)
	inflate (token) returned -5
	rsync error: error in rsync protocol data stream (code 12) at token.c(604) [receiver=3.0.6]
	rsync: connection unexpectedly closed (229747 bytes received so far) [sender]
	rsync error: error in rsync protocol data stream (code 12) at io.c(600) [sender=3.0.6]

根据以上提示，文件`20120917_inc0_tfnlf4ok_1_1.bkp`太大，导致传输异常。

查看该文件大小

	[root@any rmanbak]# ll -h 20120917_inc0_tfnlf4ok_1_1.bkp
	-rw-r----- 1 oracle oinstall 4.4G Sep 17 22:21 20120917_inc0_tfnlf4ok_1_1.bkp

这里需要调整rman备份片的大小，限制在500M，实际最大能够正常传输多大的文件尚未明确。 在rman中设置备份集中备份片的大小

	[root@any rmanbak]# su - oracle
	[root@any rmanbak]# rman target/
	RMAN> CONFIGURE CHANNEL DEVICE TYPE DISK MAXPIECESIZE 500M;
	
	new RMAN configuration parameters:
	CONFIGURE CHANNEL DEVICE TYPE DISK MAXPIECESIZE 500 M;
	new RMAN configuration parameters are successfully stored

不过以上设置对手动分配过channel的备份脚本无效，此时可以在分配通道的脚本中手动指定每个备份片的大小

	run{
		sql 'alter system archive log current';
		allocate channel cha_inc0 type disk maxpiecesize=500M;
		backup incremental level 0 format '/apps/rmanbak/data/%T_inc0_%U.bkp' tag 'weekly inc0 backup' database plus archivelog delete input;
		release channel cha_inc0;
	}

将未同步的文件使用scp命令手动同步到备机，再进行小文件(大不予500M)的同步测试。

另外，因主机和备机停机过(2012-09-24 17:08)，而rsync的实时同步备份只有监测的路径下文件结构发生变更时才会触发远程同步，这样累计起来需要同步的文件太多(2012-9-24 正好周一，rman每周一晚十点都会进行数据库全备，因此产生的备份文件很多)，也可能导致rsync同步失败。

主机日志

	[root@any ~]# uptime
	20:37:04 up 1 day, 3:31, 1 user, load average: 0.07, 0.02, 0.11
	
	[root@any ~]# last | more
	root pts/1 dev.egolife.com Tue Sep 25 20:36 still logged in 
	root pts/1 dev.egolife.com Tue Sep 25 12:46 - 20:28 (07:42) 
	root pts/2 dev.egolife.com Tue Sep 25 09:06 - 20:28 (11:22) 
	root pts/1 dev.egolife.com Tue Sep 25 08:55 - 10:04 (01:09) 
	oracle pts/1 :0.0 Tue Sep 25 08:32 - 08:33 (00:00) 
	oracle :0 Tue Sep 25 08:31 - 08:33 (00:01) 
	oracle :0 Tue Sep 25 08:31 - 08:31 (00:00) 
	reboot system boot 2.6.18-194.el5 Mon Sep 24 17:08 (1+03:28)

备机日志

	[root@anybak ~]# date
	Tue Sep 25 20:30:25 CST 2012
	[root@anybak ~]# uptime
	20:30:27 up 1 day, 3:32, 1 user, load average: 0.00, 0.00, 0.00
	[root@anybak ~]# last | more
	root pts/1 dev.egolife.com Tue Sep 25 20:30 still logged in 
	root pts/2 192.128.1.100 Tue Sep 25 16:58 - 19:58 (03:00) 
	root pts/1 192.138.1.100 Tue Sep 25 12:37 - 20:21 (07:43) 
	reboot system boot 2.6.18-194.el5 Mon Sep 24 16:59 (1+03:31)

## 脚本

rsync.sh

	#!/bin/sh
	#abstract:
	#rsync auto sync script
	#2012-06-11 dylanninin@gmail.com first_release
	#variables
	current_date=$(date +%Y%m%d_%H%M%S)
	rman_path=/apps/rmanbak
	log_file=/var/log/rsync.log

	#rsync
	rsync_server=192.168.0.29
	rsync_user=oracle
	rsync_pwd=/etc/rsync_client.pwd
	rsync_module=anybak
	#rsync_client password check
	if [ ! -e ${rsync_pwd} ]; then
		echo "rsync client password file does not exist!"
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
	inotify_fun >> ${log_file} 2<&1 &

## 延伸阅读

* [抚琴煮酒：CentIOS 5.5 下rsync使用技巧和权限问题解读](http://os.51cto.com/art/201101/243374.htm)
* [陈皓：rsync的核心算法](http://coolshell.cn/articles/7425.html)

## 参考文档

* [suchalin：在redhat5.4/5.5/5.6中默认的rsync出现的bug](http://suchalin.blog.163.com/blog/static/553046772011917112312684/)
