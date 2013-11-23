---
layout: post
title: A Case of NTP Exception
category : Linux
tags : [NTP, Linux, Exception]
---

最近虚拟化服务器出现时钟同步异常：定时同步，但发现时间比个人电脑时间相差10几个小 时。看了下鸟哥的私房菜，觉得没太大问题，于是决定测试NTP服务以排查问题。因网络限 制，无法连接到互联网，就采用其中的一台虚拟机作为NTP服务器，并以本机时间为准。测 试后才知道原来是系统安装时没有选择时区（默认为美国纽约），而使用的NTP服务器时区 为中国，所以导致虚拟化服务器时间相差13个小时。

从这次经历，再次得到一些经验教训：

* 安装Linux时注意选择合适的时区;
* 仔细阅读官方文档，这些才是最权威的文档;
* 结合理论进行测试，绝知此事要躬行;
* 要掌握一个理论，不是一朝一夕之事;

##搭建NTP服务器

###主要配置

启用本机时钟作为NTP基准时间，主要需取消注释`server	127.127.1.0	# local clock`和`fudge	127.127.1.0 stratum 10`。

完整配置如下：

	[root@server ~]# cat /etc/ntp.conf
	# For more information about this file, see the man pages
	# ntp.conf(5), ntp_acc(5), ntp_auth(5), ntp_clock(5), ntp_misc(5), ntp_mon(5).
	
	driftfile /var/lib/ntp/drift
	
	# Permit time synchronization with our time source, but do not
	# permit the source to query or modify the service on this system.
	#restrict default kod nomodify notrap nopeer noquery
	#restrict -6 default kod nomodify notrap nopeer noquery
	
	# Permit all access over the loopback interface.  This could
	# be tightened as well, but to do so would effect some of
	# the administrative functions.
	
	# Hosts on local network are less restricted.
	restrict 192.168.1.0 mask 255.255.255.0 nomodify notrap
	
	# Use public servers from the pool.ntp.org project.
	# Please consider joining the pool (http://www.pool.ntp.org/join.html).
	#server 0.centos.pool.ntp.org
	#server 1.centos.pool.ntp.org
	#server 2.centos.pool.ntp.org
	
	#broadcast 192.168.1.255 autokey	# broadcast server
	#broadcastclient			# broadcast client
	#broadcast 224.0.1.1 autokey		# multicast server
	#multicastclient 224.0.1.1		# multicast client
	#manycastserver 239.255.254.254		# manycast server
	#manycastclient 239.255.254.254 autokey # manycast client
	
	# Undisciplined Local Clock. This is a fake driver intended for backup
	# and when no outside source of synchronized time is available. 
	server	127.127.1.0	# local clock
	fudge	127.127.1.0 stratum 10	
	
	# Enable public key cryptography.
	#crypto
	
	includefile /etc/ntp/crypto/pw
	
	# Key file containing the keys and key identifiers used when operating
	# with symmetric key cryptography. 
	keys /etc/ntp/keys
	
	# Specify the key identifiers which are trusted.
	#trustedkey 4 8 42
	
	# Specify the key identifier to use with the ntpdc utility.
	#requestkey 8
	
	# Specify the key identifier to use with the ntpq utility.
	#controlkey 8
	
	# Enable writing of statistics records.
	#statistics clockstats cryptostats loopstats peerstats

###开启服务

开启ntp服务

	[root@server ~]# service ntpd restart
	Shutting down ntpd:                                        [  OK  ]
	Starting ntpd:                                             [  OK  ]

注意：
	
每次重启NTP服务之后大约要5分钟客户端才能建立正常的NTP通讯连接，否则在执行ntpdate时候将返回：

	[root@oradb ~]# ntpdate -d 192.168.1.162
	... ...
	192.168.1.162: Server dropped: strata too high
	server 192.168.1.162, port 123
	stratum 16, precision -23, leap 11, trust 000
	... ...
	8 Jan 19:28:07 ntpdate[17795]: no server suitable for synchronization found

在ntp客户端用`ntpdate –d`查看，发现有“Server dropped: strata too high”的错误，并且显示“stratum 16”。而正常情况下stratum这个值得范围是“0~15”。

这是因为NTP server还没有和其自身或者它的server同步上。详见[NTP常见错误](http://www.blogjava.net/spray/archive/2008/07/10/213964.html)。

##同步测试

###1. NTP服务器(192.168.1.162)
当前时间：

	[root@server ~]# date
	Tue Jan  8 19:32:42 EST 2013
 
###2. NTP客户端时间(192.168.1.163)：
当前时间：

	[root@oradb ~]# date
	Tue Jan  8 19:33:37 EST 2013

与192.168.1.162同步：

	[root@oradb ~]# ntpdate 192.168.1.162
	 8 Jan 19:33:51 ntpdate[24174]: adjust time server 192.168.1.162 offset -0.000002 sec

与172.31.1.1同步，时间滞后，大概是13个小时：

	[root@oradb ~]# ntpdate 172.31.1.1
	 8 Jan 06:34:10 ntpdate[24270]: step time server 172.31.1.1 offset -46801.549132 sec

在与172.31.1.1同步时，出现时钟同步异常，因与192.168.1.162同步的时钟相差太大。导致这种情况大致推测有两个原因：1）172.31.1.1上时间不对；2）192.168.1.162、163时间不对。不过这两点很快都被排除了，经过同事提点，查看[鸟哥的私房菜](http://linux.vbird.org/linux_server/0440ntp.php)，对比[世界时差表](http://www.timedate.cn/time/time_diff.asp)，才知道是192.168.1.162、163系统的时区不正确。由于系统安装时没有选择时区（默认为美国纽约），与中国上海大概相差13个小时。
 
###3.调整时区

系统当前时区

	[root@server ~]# cat /etc/sysconfig/clock.20130109 
	# The time zone of the system is defined by the contents of /etc/localtime.
	# This file is only for evaluation by system-config-date, do not rely on its
	# contents elsewhere.
	ZONE="America/New York"

调整后系统时区

	[root@server ~]# cat /etc/sysconfig/clock
	# The time zone of the system is defined by the contents of /etc/localtime.
	# This file is only for evaluation by system-config-date, do not rely on its
	# contents elsewhere.
	ZONE="Asia/Shanghai"
 
调整后时，再次与172.31.1.1同步：

	[root@oradb ~]# date
	Wed Jan  9 21:59:23 CST 2013
	[root@oradb ~]# cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime 
	cp: overwrite `/etc/localtime'? y
	[root@oradb ~]# clock -w
	[root@oradb ~]# date
	Wed Jan  9 21:59:53 CST 2013
	[root@oradb ~]# ntpdate 172.31.1.1
	 9 Jan 09:04:46 ntpdate[5898]: step time server 172.31.1.1 offset -46801.989143 sec
 
设置定时同步

	[root@server ~]# crontab -l
	00 07 * * *  /usr/sbin/ntpdate 172.31.1.1 && /sbin/hwclock -w

##鸟哥的讲解

例題： 

假設你的筆記型電腦安裝 CentOS 這套系統，而且選擇的時區為台灣。現在，你將有一個月的時間要出差到美國的紐約去， 你會帶著這個筆電，那麼到了美國之後，時間會不一致啊！你該如何手動的調整時間參數呢？

答： 

因為時區資料檔在 `/usr/share/zoneinfo` 內，在該目錄內會找到 `/usr/share/zoneinfo/America/New_York` 這個時區檔。 而時區設定檔在 `/etc/sysconfig/clock` ，且目前的時間格式在 `/etc/localtime` ，所以你應該這樣做： 

	[root@www ~]# date
	Thu Jul 28 15:08:39 CST 2011  <==重點是 CST 這個時區喔！
	
	[root@www ~]# vim /etc/sysconfig/clock
	ZONE="America/New_York"       <==改的是這裡啦！
	
	[root@www ~]# cp /usr/share/zoneinfo/America/New_York /etc/localtime
	[root@www ~]# date
	Thu Jul 28 03:09:21 EDT 2011  <==時區與時間都改變了！

 
這個範例做完之後，記得將這兩個檔案改回來！不然以後你的時間都是美國時間啦！ 

##参考
* [鸟哥的私房菜：时间服务器](http://linux.vbird.org/linux_server/0440ntp.php)
* [NTP Project](http://www.eecis.udel.edu/~mills/ntp.html)
* [NTP常见错误](http://www.blogjava.net/spray/archive/2008/07/10/213964.html)
