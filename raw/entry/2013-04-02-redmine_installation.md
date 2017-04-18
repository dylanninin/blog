---
layout: post
title: Redmine Installation on CentOS
category : Linux
tags : [Linux, Utilities]
---

## bitnami-redmine

[Redmine](http://www.redmine.org/)是一个开源的项目管理系统，基于[ROR](http://rubyonrails.org/)开发，在小型项目管理中比较实用。[BitNami](http://bitnami.com/)提供了打包好的[Redmine](http://bitnami.com/stack/redmine)程序，集成Apache, Mysql，简化了安装配置过程。

以下是安装示例。

更改权限

	[root@redmine]# chmod +x bitnami-redmine-2.3.0-0-linux-x64-installer.run 
	
开始安装
	
	[root@redmine]# ./bitnami-redmine-2.3.0-0-linux-x64-installer.run 
	Language Selection

安装语言	

	Please select the installation language
	[1] English - English
	[2] Spanish - Español
	[3] Japanese - 日本語
	[4] Korean - 한국어
	[5] Simplified Chinese - 简体中文
	[6] Hebrew - עברית
	[7] German - Deutsch
	[8] Romanian - Română
	[9] Russian - Русский
	Please choose an option [1] : 
	----------------------------------------------------------------------------
	Welcome to the BitNami Redmine Stack Setup Wizard.
	
选择组件

	----------------------------------------------------------------------------
	Select the components you want to install; clear the components you do not want 
	to install. Click Next when you are ready to continue.
	
	PhpMyAdmin [Y/n] :n
	
	Redmine : Y (Cannot be edited)
	
	Is the selection above correct? [Y/n]: Y
	
安装路径

	----------------------------------------------------------------------------
	Installation folder
	
	Please, choose a folder to install BitNami Redmine Stack
	
	Select a folder [/opt/redmine-2.3.0-0]: /apps/redmine 

管理员账户
	
	----------------------------------------------------------------------------
	Create Admin account
	
	BitNami Redmine Stack admin user creation
	
	Login [user]: admin
	
	Password :z9AZz7cz
	Please confirm your password :z9AZz7cz
	Your real name [User Name]: gonghaibing
	
	Email Address [mail@example.com]: gonghaibing@tp-link.net
	
配置语言

	----------------------------------------------------------------------------
	Language for default data configuration
	
	Select your language for default data configuration:
	
	[1] Bulgarian
	[2] Czech
	[3] German
	[4] English
	[5] Spanish
	[6] French
	[7] Hebrew
	[8] Italian
	[9] Japanese
	[10] Korean
	[11] Dutch
	[12] Polish
	[13] Portuguese
	[14] Portuguese/Brazilian
	[15] Romanian
	[16] Russian
	[17] Serbian
	[18] Swedish
	[19] Chinese
	[20] Chinese/Taiwan
	Please choose an option [4] : 
	
	Do you want to configure mail support? [y/N]: y
	
邮件支持	

	----------------------------------------------------------------------------
	Configure SMTP Settings
	
	This is required so your application can send notifications via email.
	
	Default email provider:
	
	[1] GMail
	[2] Custom
	Please choose an option [1] : 2
	
	----------------------------------------------------------------------------
	Configure SMTP Settings
	
	Default mail server configuration.
	
	Username []: dylanninin
	
	Password :
	Re-enter :
	SMTP Host []: smtp.egolife.com
	
	SMTP Port []: 25
	
	Secure connection
	
	[1] None
	[2] SSL
	[3] TLS
	Please choose an option [3] : 1
	
开始安装

	----------------------------------------------------------------------------
	Setup is now ready to begin installing BitNami Redmine Stack on your computer.
	
	Do you want to continue? [Y/n]: Y
	
	----------------------------------------------------------------------------
	Please wait while Setup installs BitNami Redmine Stack on your computer.
	
	 Installing
	 0% ______________ 50% ______________ 100%
	 #########################################
	
	----------------------------------------------------------------------------
	Setup has finished installing BitNami Redmine Stack on your computer.
	
	Launch Redmine application. [Y/n]: Y
	
	Info: To access the BitNami Redmine Stack, go to
	http://localhost:80 from your browser.
	Press [Enter] to continue :

## 导出数据

	[root@old]# /opt/rubystack-2.1-0/apps/redmine/config/database.yml

	production:
	  adapter: mysql
	  database: bitnami_redmine
	  host: localhost
	  username: bn_redmine
	  password: b3eae0f5e6 
	  socket: /opt/rubystack-2.1-0/mysql/tmp/mysql.sock

	[root@old rubystack-2.1-0]# mysql/bin/mysqldump -ubn_redmine -p --opt bitnami_redmine > ~/redmine_20130402.sql
	Enter password: 

## 导入数据

	[root@redmine]# less /apps/rubystack/apps/redmine/htdocs/config/database.yml
	
	production:
	  adapter: mysql
	  database: bitnami_redmine
	  host: localhost
	  username: bn_redmine
	  password: 7e37e93290 
	  socket: /apps/rubystack/mysql/tmp/mysql.sock

	[root@redmine ~]# /apps/redmine/mysql/bin/mysql -ubitnami -p bitnami_redmine < redmine_20130402.sql 
	Enter password: 7e37e93290

## 参考

* [Installing Redmine](http://www.redmine.org/projects/redmine/wiki/RedmineInstall)
* [bitnami Redmine]((http://bitnami.com/stack/redmine))
