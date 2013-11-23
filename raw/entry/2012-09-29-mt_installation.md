---
layout: post
title: MT Installation I
category : Blog
tags : [Blog, MovableType]
---

##MovableType 安装记录

安装环境

* 博客：MTOS-4.38-en
* 服务器：Linux dev.egolife.com 2.6.32-71.el6.i686 GNU/Linux
* 数据库： MySQL 5.1.47
* Web服务器: Apache/2.2.15 (CentOS) Server at localhost Port 80

##安装步骤

解压

	[root@dev]# unzip MTOS-4.38-en.zip /var/www/cgi-bin

创建cgi-bin软连接

	[root@dev]# ln -s /var/www/cgi-bin/MTOS-4.38-en /var/www/cgi-bin/mt
	[root@dev]# ll /var/www/cgi-bin/
	total 4
	lrwxrwxrwx 1 root root 13 Sep 22 23:57 mt -> MTOS-4.38-en/
	drwxr-xr-x 13 root root 4096 Sep 23 00:03 MTOS-4.38-en

创建静态文件软连接

	[root@dev]# ln -s /var/www/cgi-bin/MTOS-4.38-en/mt-static /var/www/html/mt-static
	[root@dev]# ll /var/www/html/
	total 0
	lrwxrwxrwx 1 root root 40 Sep 22 23:58 mt-static -> /var/www/cgi-bin/MTOS-4.38-en/mt-static/

权限更改

	[root@dev]# chmod 777 /var/www/cgi-bin/MTOS-4.38-en/mt-static/support
	[root@dev]# chmod 777 /var/www/cgi-bin/MTOS-4.38-en/themes

##配置文件

主要配置Movable Type的cgi-bin、静态文件的路径，数据库连接认证信息。

查看当前主机名

	[root@dev mt]# hostname
	dev.egolife.com

重命名配置文件

	[root@dev]# cd /var/www/cgi-bin/MTOS-4.38-en
	[root@dev mt]# cp mt-config.cgi-original mt-config.cgi

编辑配置文件，配置数据库

	[root@dev mt]# vim mt-config.cgi
	CGIPath http://dev.egolife.com/cgi-bin/mt/
	StaticWebPath http://dev.egolife.com/mt-static/
	ObjectDriver DBI::mysql
	Database xxxxxxxxx
	DBUser xxxxxxxxx
	DBPassword xxxxxxxxx
	DBHost localhost
	EmailAddressMain dylanninin@gmail.com
	
	#####################################################################

##创建MT数据库、用户并授权

	[root@dev]# mysql -uroot -p
	mysql> create database mt character utf8;
	mysql> create user mt;
	mysql> grant all on mt.* to xxxxxxxxx@'localhost' identified by 'xxxxxxxxx';

##启动web服务器

	[root@dev mt]# apachectl start

##第一次访问

使用浏览器打开以下url:

	http://dev.egolife.com/cgi-bin/mt/mt.cgi

此时出现异常，信息如下：

	Forbidden
	
	You don't have permission to access /cgi-bin/mt/mt.cgi on this server.
	Apache/2.2.15 (CentOS) Server at dev.egolife.com Port 80

查看httpd日志信息

	[root@dev]# less /var/log/httpd/error_log
	[Sun Sep 23 00:11:31 2012] [error] [client 192.168.136.1] Directory index forbidden by Options directive: /var/www/html/
	[Sun Sep 23 00:11:39 2012] [error] [client 192.168.136.1] Symbolic link not allowed or link target not accessible: /var/www/cgi-bin/mt
	[Sun Sep 23 00:13:44 2012] [error] [client 127.0.0.1] File does not exist: /var/www/html/server-status

##主要错误信息

###不允许mt符号连接

更改`httpd.conf`中`/var/www/cgi-bin`的配置，启用符号链接，如下:
	
	581 #
	582 <Directory "/var/www/cgi-bin">
	583 AllowOverride None
	584 # Options None
	585 Options FollowSymLinks 
	586 Order allow,deny
	587 Allow from all
	588 </Directory>

重启apache

	[root@dev httpd]# apachectl restart

再次访问，则可以正常浏览。

###文件server-status不存在
	
	[root@dev httpd]# ll /var/www/html/
	total 0
	lrwxrwxrwx 1 root root 40 Sep 22 23:58 mt-static -> /var/www/cgi-bin/MTOS-4.38-en/mt-static/
	[root@dev]# mkdir /var/www/html/server-status
	[root@dev]# chown apache:apache /var/www/html/server-status/
	[root@dev]# ll /var/www/html/
	total 4
	lrwxrwxrwx 1 root root 40 Sep 22 23:58 mt-static -> /var/www/cgi-bin/MTOS-4.38-en/mt-static/
	drwxr-xr-x 2 apache apache 4096 Sep 23 00:31 server-status

访问时，已经显示Movable Type配置页面，但出现新的错误提示:
	
	An error occurred
	Can't connect to data source '' because I can't work out what driver to use (it doesn't seem to contain a 'dbi:driver:' prefix and the DBI_DRIVER env var is not set)

可能是因为没有安装DBI扩展库，但查看rpm包时已经安装:

	[root@dev httpd]# rpm -qa | grep DBI
	perl-DBI-1.609-4.el6.i686
	perl-DBIx-Simple-1.32-3.el6.noarch

有可能是前面的`mt-config.cgi`配置出现问题:

	27 ##### MYSQL #####
	28 ObjectDriver DBI::mysql
	29 Database mt
	30 DBUser mt
	31 DBPassword 000000
	32 DBHost localhost
	33 EmailAddressMain dylanninin@gmail.com
	34 
	35 ##### POSTGRESQL #####
	36 #ObjectDriver DBI::postgres
	37 #Database DATABASE_NAME
	38 #DBUser DATABASE_USERNAME
	39 #DBPassword DATABASE_PASSWORD
	40 #DBHost localhost
	41 
	42 ##### SQLITE #####
	43 #ObjectDriver DBI::sqlite
	44 #Database /path/to/sqlite/database/file

发现更改DB配置时，没有将PostgreSQL和SQLite的配置注释掉，注释掉后重启Apache，则可以正常配置。

##创建博客

创建博客时，出现异常。主要信息如下:

	Blog Name:
	My First Blog
	Blog URL
	http://dev.egolife.com/blog/
	Publishing Path
	/var/www/html/blog

错误信息：

	In order to properly publish your blog, you must provide Movable Type with your blog's URL and the path on the filesystem where its files should be published.
	--The path provided below is not writable.
	Blog Name
	Blog URL
	Publishing Path
	Your 'Publishing Path' is the path on your web server's file system where Movable Type will publish all the files for your blog. Your web server must have write access to this directory.

创建目录

	[root@dev html]# cd /var/www/html
	[root@dev html]# mkdir blog
	[root@dev html]# chown apache:apache blog/
	[root@dev html]# ll
	total 8
	drwxr-xr-x 2 apache apache 4096 Sep 23 00:46 blog

到此，初步安装MovableType成功。