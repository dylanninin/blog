---
layout: post
title: Configure cx_Oracle on CentOS
category : Python
tags : [Python, Database, Libs]
---

uname

    [root@oradb]~# uname -a
    Linux oradb.egolife.com 2.6.32-220.el6.x86_64 #1 SMP Tue Dec 6 19:48:22 GMT 2011 x86_64 x86_64 x86_64 GNU/Linux

python version
	
    [root@oradb]~# python     
    Python 2.6.6 (r266:84292, Dec  7 2011, 20:48:22) 
    [GCC 4.4.6 20110731 (Red Hat 4.4.6-3)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> exit()

cx_Oracle package
	
    [root@oradb]~# ll software 
    total 276
    -rw-r--r--. 1 root   root     275117 Jul 25 10:16 cx_Oracle-5.1.2-11g-py26-1.x86_64.rpm
    drwxr-xr-x. 8 oracle oinstall   4096 Aug 21  2009 database

install cx_Oracle
	
    [root@oradb]~# rpm -ihv software/cx_Oracle-5.1.2-11g-py26-1.x86_64.rpm 
    Preparing...                ########################################### [100%]
       1:cx_Oracle              ########################################### [100%]

cx_Oracle test
	   
    [root@oradb]~# su - oracle
    [oracle@oradb]~# python
    Python 2.6.6 (r266:84292, Dec  7 2011, 20:48:22) 
    [GCC 4.4.6 20110731 (Red Hat 4.4.6-3)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import cx_Oracle
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ImportError: libclntsh.so.11.1: cannot open shared object file: No such file or directory
    >>> exit()

    [oracle@oradb]~# locate libclntsh.so.11.1
    /db/oracle/product/11.2.0/db_1/inventory/Scripts/ext/lib/libclntsh.so.11.1
    /db/oracle/product/11.2.0/db_1/inventory/backup/2012-11-30_04-38-40AM/Scripts/ext/lib/libclntsh.so.11.1
    /db/oracle/product/11.2.0/db_1/lib/libclntsh.so.11.1
    /root/software/database/stage/ext/lib/libclntsh.so.11.1

    [oracle@oradb ~]$ cat ~/.bash_profile 
    # .bash_profile

    # Get the aliases and functions
    if [ -f ~/.bashrc ]; then
        . ~/.bashrc
    fi

    # User specific environment and startup programs

    PATH=$PATH:$HOME/bin

    export PATH

    #2013-1-22	oracle 11gR2 settings
    export TMP=/tmp
    export TMPDIR=$TMP
    export ORACLE_BASE=/db/oracle
    export ORACLE_HOME=/db/oracle/product/11.2.0/db_1
    export ORACLE_SID=DBTEST
    export LD_LIBRARY_PATH=/db/oracle/product/11.2.0/db_1/lib
    export PATH=$PATH:$ORACLE_HOME/bin

    alias sqlplus='rlwrap sqlplus'
	
    [oracle@oradb ~]$ python
    Python 2.6.6 (r266:84292, Dec  7 2011, 20:48:22) 
    [GCC 4.4.6 20110731 (Red Hat 4.4.6-3)] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import cx_Oracle
    >>> connection = cx_Oracle.connect('dev/dev@dbtest')
    >>> connection = cx_Oracle.connect('dev/dev@172.29.88.164:1521:/dbtest')
    >>> connection.version
    '11.2.0.1.0'
	
##Reference

* [Python cx_Oracle 5.0 New Features Overview](http://www.oracle.com/technetwork/articles/tuininga-cx-oracle-084866.html)
* [cx_Oracle Tutorial](http://dbaportal.eu/sidekicks/sidekick-cx_oracle-code-paterns/)

