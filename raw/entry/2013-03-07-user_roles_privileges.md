---
layout: post
title:  Users, Roles, Privileges in Oracle Database
category : Oracle
tags : [Oracle, Database, DBA]
---

##权限

权限(Privilege)：即执行特定语句的能力。权限允许用户访问数据库中其他用户的对象，执行存储过程，或者执行一些系统级的操作。在Oracle数据库系统中，一般分为系统权限，和对象权限。

###1.系统权限

与具体的对象无关，是在任何对象上执行操作的权利，以及运行批处理、改变系统参数、创建角色等方面的权限。
	
	--查询所有系统权限
	SELECT * FROM SYSTEM_PRIVILEGE_MAP;
	
	--查询某个用户/角色的所有系统权限
	SELECT * FROM DBA_SYS_PRIVS DSP WHERE DSP.GRANTEE = UPPER('&grantee');	
	
###2.对象权限

在特定对象上执行特定操作的权限，如SELECT,INSERT,UPDATE等。对象：表、视图、过程等。
	
	--所有对象权限
	SELECT * FROM DBA_TAB_PRIVS;
	
	--某角色被授予的相关表的权限
	SELECT * FROM ROLE_TAB_PRIVS RTP WHERE RTP.ROLE = UPPER('&role');
	
	--使用密码文件的用户
	SELECT * FROM V$PWFILE_USERS;
	
###3.角色相关

一组权限的集合，简化权限的管理。被授予给角色的用户，将继承该角色所授予的所有权限以及角色。角色可以使用密码认证加强安全性。
	
	--所有角色
	SELECT * FROM DBA_ROLES;
	
	--某一角色被授予的系统权限
	SELECT * FROM ROLE_SYS_PRIVS RSP WHERE RSP.ROLE = UPPER('&role');
	
	--用户角色分配关系
	SELECT * FROM DBA_ROLE_PRIVS DRP WHERE DRP.GRANTEE = UPPER('&user');
	
###4.当前用户

与当前登录用户相关的系统权限、对象权限、角色等相关的视图。

	--查看当前用户
	SELECT USER FROM DUAL;
	
	--当前用户授予的系统权限
	SELECT * FROM USER_SYS_PRIVS;
	
	--当前用户所拥有的全部权限
	SELECT * FROM SESSION_PRIVS;
	
	--当前用户所授予的直接角色
	SELECT * FROM USER_ROLE_PRIVS;
	
	--当前用户被授予的所有角色
	SELECT * FROM SESSION_ROLES;
	
	--当前用户所有角色被授予的角色
	SELECT * FROM ROLE_ROLE_PRIVS;
	
	--当前用户的对象权限
	SELECT * FROM TABLE_PRIVILEGES;
	
##权限、角色配置与管理

###1.授权

	SQL> ? grant
	
	 GRANT (Object Privileges)
	 -------------------------
	
	 Use this command to grant privileges for a particular object to
	 users and roles. To grant system privileges and roles, use the GRANT
	 command (System Privileges and Roles).
	
	 GRANT
	   { object_priv | ALL [PRIVILEGES] }
	   [ ( column [, column] ...) ]
	   [, { object_priv | ALL [PRIVILEGES] }
	      [ ( column [, column] ...) ] ] ...
	 ON [ schema.| DIRECTORY] object
	 TO { user | role | PUBLIC} ...
	    [ WITH GRANT OPTION]
	
	 For detailed information on this command, see the Oracle8 Server SQL
	 Reference.
	
	
	 GRANT (System Privileges and Roles)
	 -----------------------------------
	
	 Use this command to grant system privileges and roles to users and
	 roles. To grant object privileges, use the GRANT command (Object
	 Privileges).
	
	 GRANT
	   { system_priv | role}
	   [, { system_priv | role} ] ...
	 TO
	   { user | role | PUBLIC}
	   [, { user | role | PUBLIC} ] ...
	   [ WITH ADMIN OPTION]
	
	 For detailed information on this command, see the Oracle8 Server SQL
	 Reference.

注：

*  WITH ADMIN OPTION：带有该选项，则被授权用户也可以管理该权限，即授权、取消授权给其他用户。
* GRANT ANY PRIVILEGE：带有该选项，则被授权用户可以对任何权限进行授权或取消授权。

###2.取消授权

	SQL> ? revoke
	
	 REVOKE (Schema Object Privileges)
	 ---------------------------------
	
	 Use this command to revoke object privileges for a particular object
	 from users and roles. To revoke system privileges or roles, use the
	 REVOKE command (System Privileges and Roles).
	
	 REVOKE
	   { object_priv | ALL [PRIVILEGES] }
	   [, {object_priv | ALL [PRIVILEGES] } ] ...
	 ON
	   [ schema.| DIRECTORY] object
	 FROM
	   { user | role | PUBLIC}
	   [, {user | role | PUBLIC} ] ...
	   [ CASCADE CONSTRAINTS]
	
	 For detailed information on this command, see the Oracle8 Server SQL
	 Reference.
	
	
	 REVOKE (System Privileges and Roles)
	 ------------------------------------
	
	 Use this command to revoke system privileges and roles from users
	 and roles. To revoke object privileges from users and roles, use the
	 REVOKE command (Object Privileges).
	
	 REVOKE
	   { system_priv | role}
	   [, { system_priv | role} ] ...
	 FROM
	   { user | role | PUBLIC}
	   [, {user | role | PUBLIC} ] ...
	
	 For detailed information on this command, see the Oracle8 Server SQL
	 Reference.

###3.角色

####创建角色

	SQL> ? create role
	
	 CREATE ROLE
	 -----------
	
	 Use this command to create a role. A role is a set of privileges
	 that can be granted to users or to other roles.
	
	 CREATE ROLE role [NOT IDENTIFIED | IDENTIFIED {BY password |
	   EXTERNALLY | GLOBALLY} ]
	
	 For detailed information on this command, see the Oracle8 Server SQL
	 Reference.

####角色选择

创建角色后，可以使用GRANT/REVOKE给角色授予、取消授予适当权限，并最终分配给用户。一个用户可以拥有多个角色，在一个用户会话过程中，用户可以选择性的使某些角色生效或禁用，以控制对系统、对象的访问。

设置当前角色

	SQL> set role connect;
	
	Role set.
	
	SQL> create table role_t(id number);
	create table role_t(id number)
	*
	ERROR at line 1:
	ORA-01031: insufficient privileges
	

使用户所有角色生效

	SQL> set role all;
	
	Role set.

	SQL> create table role_t(id number);
	
	Table created.
	
排除某些角色

	SQL> select count(1) from v$session;
	
	  COUNT(1)
	----------
		88
	
	SQL> set role all except dba;
	
	Role set.
	
	SQL> select count(1) from v$session;
	select count(1) from v$session
	                     *
	ERROR at line 1:
	ORA-00942: table or view does not exist

####默认角色

当设置用户默认角色时，这些角色会在用户初始化会话时自动生效。

	alter user username defautl role role_list;

##延伸阅读

* [Oracle用户及角色介绍](http://blog.csdn.net/tianlesoftware/article/details/4786956)