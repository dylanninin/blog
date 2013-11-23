---
layout: post
title: MT Installation II
category : Blog
tags : [Blog, MovableType]
---

##MovableType 安装记录（二）

接着[上一篇](http://dylanninin.com/blog/2012/09/29/mt_installation.html)继续配置Movable Type。

##Apache配置

###配置站点首页

打开`http://dev.egolife.com`时，默认显示为Apache的测试页面。当访问 `http://dev.egolife.com/blog`才会显示博客首页。

取消显示Apache测试页面,更改配置`/etc/httpd/conf.d/welcome.conf`,注释掉 LocationMatch配置：
	
	[root@dev html]# vim /etc/httpd/conf.d/welcome.conf
	1 #.
	2 # This configuration file enables the default "Welcome"
	3 # page if there is no default index page present for
	4 # the root URL. To disable the Welcome page, comment
	5 # out all the lines below.
	6 #
	7 #<LocationMatch "^/+$">
	8 # Options -Indexes
	9 # ErrorDocument 403 /error/noindex.html
	10 #</LocationMatch>

运行`service http reload`命令，重新加载配置后，直接访问主机，则出现的是 `/var/www/html`的页面列表信息。

###禁止列表文件

禁止列表信息，需要更改配置`/etc/httpd/conf/httpd.conf`：

	[root@dev html]# vim /etc/httpd/conf/httpd.conf
	317 <Directory "/var/www/html">
	318 
	319 #
	320 # Possible values for the Options directive are "None", "All",
	321 # or any combination of:
	322 # Indexes Includes FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews
	323 #
	324 # Note that "MultiViews" must be named *explicitly* --- "Options All"
	325 # doesn't give it to you.
	326 #
	327 # The Options directive is both complicated and important. Please see
	328 # http://httpd.apache.org/docs/2.2/mod/core.html#options
	329 # for more information.
	330 #
	331 # Options Indexes FollowSymLinks
	332 Options FollowSymLinks
	333 
	334 #
	335 # AllowOverride controls what directives may be placed in .htaccess files.
	336 # It can be "All", "None", or any combination of the keywords:
	337 # Options FileInfo AuthConfig Limit
	338 #
	339 AllowOverride None
	340 
	341 #
	342 # Controls who can get stuff from this server.
	343 #
	344 Order allow,deny
	345 Allow from all
	346 
	347 </Directory>

更改配置后，重新加载配置文件，则显示禁止访问，此时可以自定义显示的页面，这里采用 软链接的方式。

###设置软连接

	[root@dev html]# ln -s /var/www/html/blog/index.html /var/www/html/index.html
	[root@dev html]# ll
	total 12
	drwxr-xr-x 7 apache apache 4096 Sep 23 16:05 blog
	-rw-r--r-- 1 apache apache 1406 Sep 23 15:47 favicon.ico
	lrwxrwxrwx 1 root root 29 Sep 23 16:29 index.html -> /var/www/html/blog/index.html
	lrwxrwxrwx 1 root root 40 Sep 22 23:58 mt-static -> /var/www/cgi-bin/MTOS-4.38-en/mt-static/
	drwxr-xr-x 2 apache apache 4096 Sep 23 00:31 server-status

这样访问`http://dev.egolife.com`时，会直接显示博客首页。当然，可以使用URL重写或 重定向来实现.

###错误提示页

主要是403,404,500页面的配置，更改`/etc/httpd/conf/httpd.conf`：

	[root@dev html]# vim /etc/httpd/conf/httpd.conf
	833 # Some examples:
	834 #ErrorDocument 500 "The server made a boo boo."
	835 #ErrorDocument 404 /missing.html
	836 #ErrorDocument 404 "/cgi-bin/missing_handler.pl"
	837 #ErrorDocument 402 http://www.example.com/subscription_info.html
	838 #
	839 #2012-09-22|dylanninin@gmail.com| ErrorDocument
	840 ErrorDocument 500 http://dev.egolife.com/errors/500.html
	841 ErrorDocument 404 http://dev.egolife.com/errors/404.html
	842 ErrorDocument 403 http://dev.egolife.com/errors/403.html

###添加错误页面

	[root@dev errors]# pwd
	/var/www/html/errors
	[root@dev errors]# ll
	total 0
	-rw-r--r-- 1 apache apache 0 Sep 23 16:58 403.html
	-rw-r--r-- 1 apache apache 0 Sep 23 16:58 404.html
	-rw-r--r-- 1 apache apache 0 Sep 23 17:00 500.html

以上页面内容待完善!

##参考

* Movable Type：[MTOS文件系统描述](http://www.movabletype.org/documentation/installation/file-system.html)
