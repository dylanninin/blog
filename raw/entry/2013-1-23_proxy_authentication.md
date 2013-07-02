#写在前面的话
在学习[cx_Oracle](http://sourceforge.net/projects/cx-oracle/)访问Oracle数据库时，下载作者的源代码，发现作者在测试的数据库脚本中创建用户即使用了代理授权。当时没有太注意，最近正好总结作半年以来的工作，想起来就先测试下，以作备忘。

#代理认证测试

##cx_Oracle中创建用户脚本

	... ...
	create user cx_Oracle identified by "password"
	quota unlimited on dba_data
	default tablespace dba_data
	temporary tablespace dba_tmp;
	
	
	create user cx_Oracle_proxy identified by "password";
	alter user cx_Oracle_proxy grant connect through cx_Oracle;
	
	grant create session to cx_Oracle_proxy;
	
	grant
	  create session,
	  create table,
	  create procedure,
	  create type
	to cx_Oracle;
	... ...

##代理认证测试
###创建代理/被代理用户

查看DEV所有的系统权限

	SQL> conn /as sysdba
	Connected.
	
	SQL> SELECT * FROM dba_sys_privs dsp WHERE dsp.grantee = upper('&grantee');
	Enter value for grantee: dev
	old   1: SELECT * FROM dba_sys_privs dsp WHERE dsp.grantee = upper('&grantee')
	new   1: SELECT * FROM dba_sys_privs dsp WHERE dsp.grantee = upper('dev')
	
	GRANTEE 		    PRIVILEGE			    ADM
	------------------ ------------------------ ---
	DEV			       CREATE ANY VIEW			NO
	DEV			       DEBUG CONNECT SESSION	NO
	DEV			       CREATE ANY PROCEDURE		NO
	DEV			       UNLIMITED TABLESPACE		NO
	DEV			       DEBUG ANY PROCEDURE		NO
	

创建账户`DEV_APP`，并授权代理。`DEV_APP`通过`DEV`代理数据库连接

	SQL> create user dev_app default tablespace dba_data temporary tablespace dba_tmp identified by APP;
	User created.
	
	SQL> alter user dev_app grant connect through dev;
	User altered.


使用代理用户连接数据库
	
	SQL> conn dev[dev_app]  --conn proxy_user[real_user]/password_of_proxy_user
	Enter password: 
	ERROR:
	ORA-01045: user DEV_APP lacks CREATE SESSION privilege; logon denied
	Warning: You are no longer connected to ORACLE.
	SQL> alter create session to dev_app;
	SP2-0640: Not connected
	SQL> conn /as sysdba
	Connected.
	
DEV_APP需要`CREATE SESSION`权限

	SQL> grant create session to dev_app;
	Grant succeeded.
	
查看当前用户和代理用户

	SQL> conn dev[dev_app]		
	Enter password: 			
	Connected.
	SQL> select sys_context('userenv','current_user') from dual;
	SYS_CONTEXT('USERENV','CURRENT_USER')
	------------------------------------------------------------
	DEV_APP
	
	SQL> select sys_context('userenv','proxy_user') from dual;
	SYS_CONTEXT('USERENV','PROXY_USER')
	------------------------------------------------------------
	DEV

从这部分测试可用看出，被代理的用户(即`DEV_APP`)通过代理用户(即`DEV`)进行连接时，使用代理用户的用户名、密码进行认证，但被代理用户需要有连接数据库创建会话的权限才能连接。

###对象访问权限
因`DEV_APP`通过代理用户`DEV`进行连接，不知`DEV_APP`是否也会拥有DEV的权限。故测试下被代理用户的权限是如何处理的。

DEV拥有的表：

	SQL> conn dev
	Enter password: 
	Connected.
	SQL> select table_name from user_tables;	
	TABLE_NAME
	------------------------------
	DBA_TEST

查看`DEV_APP`拥有的表，并访问`DEV`的对象：

	SQL> conn dev[dev_app]/
	Enter password: 
	Connected.
	SQL> select table_name from user_tables;
	no rows selected

	SQL> select count(1) from dev.dba_test;
	select count(1) from dev.dba_test
	                         *
	ERROR at line 1:
	ORA-00942: table or view does not exist

	SQL> SELECT * FROM session_privs;
	PRIVILEGE
	----------------------------------------
	CREATE SESSION
	
	SQL> create table app_test(id number);
	create table app_test(id number)
	*
	ERROR at line 1:
	ORA-01031: insufficient privileges
	
给`DEV_APP`用户授权：

	SQL> conn /as sysdba
	Connected.
	SQL> grant create table to dev_app;
	Grant succeeded.
	
	SQL> conn dev[dev_app]
	Enter password: 
	Connected.
	SQL> create table app_test(id number);	
	Table created.
	
通过这部分测试可用看出，被代理用户`DEV_APP`不会继承代理用户`DEV`的权限。要权限需要额外授予。

#小结

One should understand that a database proxied user behaves just like the user itself. The connection is created by the proxy, but the session's privileges are limited to the privileges of the proxied user, who is after all a database user.

意即被代理用户(如`DEV_APP`)仅仅是通过代理用户(如`DEV`)身份认证并创建数据库会话连接，在该连接过程中所有的操作都受限于被代理用户的权限。

代理认证的作用：

* 多用户(被代理用户)可以使用单一用户(代理用户)进行认证连接，因统一使用代理用户的用户名/密码进行认证，简化了多用户的密码管理。
* 当忘记用户密码(如`DEV_APP`)，而又想以该身份登陆数据库时，可以使用代理用户（如`DEV`）。