---
layout: post
title: Configure Postfix, Cyrus-SASL and MySQL
category : Linux
tags : [Linux, Utilities, Mail]
---

### OS Configuration

kernel

    [dev@dev ~]$ uname -a
    Linux oa.egolife.com 2.6.32-220.el6.x86_64 #1 SMP Tue Dec 6 19:48:22 GMT 2011 x86_64 x86_64 x86_64 GNU/Linux
    
account

    [root@dev ~]# useradd -s /sbin/nologin me
    [root@dev ~]# passwd me
    Changing password for user me.
    New password: 
    Retype new password: 
    passwd: all authentication tokens updated successfully.
    
## postfix sasl mysql

required packages

    [dev@dev ~]$ rpm -qa | egrep 'postfix|sasl|mysql'
    cyrus-sasl-sql-2.1.23-13.el6.x86_64
    cyrus-sasl-ldap-2.1.23-13.el6.x86_64
    cyrus-sasl-md5-2.1.23-13.el6.x86_64
    cyrus-sasl-gssapi-2.1.23-13.el6.x86_64
    mysql-5.1.52-1.el6_0.1.x86_64
    mysql-libs-5.1.52-1.el6_0.1.x86_64
    mysql-devel-5.1.52-1.el6_0.1.x86_64
    cyrus-sasl-lib-2.1.23-13.el6.x86_64
    cyrus-sasl-plain-2.1.23-13.el6.x86_64
    mysql-server-5.1.52-1.el6_0.1.x86_64
    cyrus-sasl-2.1.23-13.el6.x86_64
    cyrus-sasl-devel-2.1.23-13.el6.x86_64
    postfix-2.6.6-2.2.el6_1.x86_64

config postfix
    
    postconf -e 'home_mailbox = Maildir/'
    postconf -e 'smtpd_sasl_path = postfix'
    postconf -e 'smtpd_sasl_security_options = noanonymous'
    postconf -e 'broken_sasl_auth_clients = yes'
    postconf -e 'smtpd_sasl_auth_enable = yes'
    postconf -e 'smtpd_recipient_restrictions = permit_sasl_authenticated, permit_mynetworks,reject_unauth_destination'
    postconf -e 'inet_interfaces = all'
    postconf -e 'mynetworks = 172.31.0.0/16, 127.0.0.0/8'
    postconf -e 'myorigin = egolife.com'

    [dev@dev ~]$ grep '^\s*[^# \t].*$' /etc/postfix/main.cf 
    queue_directory = /var/spool/postfix
    command_directory = /usr/sbin
    daemon_directory = /usr/libexec/postfix
    data_directory = /var/lib/postfix
    mail_owner = postfix
    myhostname = oa.egolife.com
    myorigin = egolife.com
    inet_interfaces = all
    inet_protocols = all
    mydestination = $myhostname, localhost.$mydomain, localhost
    unknown_local_recipient_reject_code = 550
    mynetworks = 172.31.0.0/16, 127.0.0.0/8
    alias_maps = hash:/etc/aliases
    alias_database = hash:/etc/aliases
    home_mailbox = Maildir/
    debug_peer_level = 7
    debugger_command =
         PATH=/bin:/usr/bin:/usr/local/bin:/usr/X11R6/bin
         ddd $daemon_directory/$process_name $process_id & sleep 5
    sendmail_path = /usr/sbin/sendmail.postfix
    newaliases_path = /usr/bin/newaliases.postfix
    mailq_path = /usr/bin/mailq.postfix
    setgid_group = postdrop
    html_directory = no
    manpage_directory = /usr/share/man
    sample_directory = /usr/share/doc/postfix-2.6.6/samples
    readme_directory = /usr/share/doc/postfix-2.6.6/README_FILES
    smtpd_recipient_restrictions = permit_sasl_authenticated, permit_mynetworks,reject_unauth_destination
    smtpd_sasl_auth_enable      =  yes
    smtpd_sasl_security_options = noanonymous
    smtpd_sasl_path             = postfix
    broken_sasl_auth_clients    =  yes
    smtpd_sasl_authenticated_header =  yes

config sasl2

    [dev@dev ~]$ cat /etc/sasl2/postfix.conf
    log_level: 5
    pwcheck_method: auxprop
    auxprop_plugin: sql
    mech_list: CRAM-MD5 PLAIN LOGIN
    sql_engine: mysql
    sql_hostnames: localhost
    sql_user: email
    sql_passwd: email
    sql_database: email
    sql_verbose: yes
    sql_select: SELECT clear_password FROM users WHERE username='%u@%r'  AND active=1
    
config mysql

    [root@dev ~]# mysql -uroot -p
    Enter password: 
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 240512
    Server version: 5.1.52-log Source distribution

    Copyright (c) 2000, 2010, Oracle and/or its affiliates. All rights reserved.
    This software comes with ABSOLUTELY NO WARRANTY. This is free software,
    and you are welcome to modify and redistribute it under the GPL v2 license

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | email              |
    | mysql              |
    | test               |
    +--------------------+
    4 rows in set (0.07 sec)

    mysql> use email;
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A

    Database changed
    mysql> show tables;
    +-----------------+
    | Tables_in_email |
    +-----------------+
    | users           |
    +-----------------+
    1 row in set (0.00 sec)

    mysql> desc users;
    +----------------+--------------+------+-----+-------------------+-------+
    | Field          | Type         | Null | Key | Default           | Extra |
    +----------------+--------------+------+-----+-------------------+-------+
    | username       | varchar(255) | NO   | PRI | NULL              |       |
    | password       | varchar(255) | NO   |     | $$$$$$            |       |
    | clear_password | varchar(255) | NO   |     | 888888            |       |
    | maildir        | varchar(255) | NO   |     |                   |       |
    | mailquota      | int(11)      | NO   |     | 20                |       |
    | created        | timestamp    | NO   |     | CURRENT_TIMESTAMP |       |
    | modified_by    | varchar(255) | NO   |     |                   |       |
    | active         | int(11)      | NO   |     | 1                 |       |
    +----------------+--------------+------+-----+-------------------+-------+
    8 rows in set (0.01 sec)
    
    mysql> select * from users;
    +-------------------------+----------+----------------+---------+-----------+---------------------+-------------+--------+
    | username                | password | clear_password | maildir | mailquota | created             | modified_by | active |
    +-------------------------+----------+----------------+---------+-----------+---------------------+-------------+--------+
    | Dev@dev.egolife.com    | $$$$$$   | dbVm116#       |         |        20 | 2012-12-19 11:32:41 |             |      1 |
    | Mailer@dev.egolife.com | $$$$$$   | 6$!Xxuw4       |         |        20 | 2012-12-19 10:44:12 |             |      1 |
    +-------------------------+----------+----------------+---------+-----------+---------------------+-------------+--------+
    2 rows in set (0.00 sec)
    
    mysql> grant all on email.* to email@'%' identified by 'password';
  
## chkconfig and start service
  
chkconfig 
    
    [root@db ~]# chkconfig postfix on
    [root@db ~]# chkconfig saslauthd on
    [root@db ~]# chkconfig mysqld on

start service

    [root@db ~]# service postfix restart
    Shutting down postfix:                                     [  OK  ]
    Starting postfix:                                          [  OK  ]
    [root@db ~]# service saslauthd restart
    Stopping saslauthd Imap:                                     [  OK  ]
    Starting saslauthd Imap:                                     [  OK  ]
    
## mail test

script 

    F:\Workspace\python\pydev\mail\eml\mail.py

client 

    cd /d  F:\Workspace\python\pydev\mail\eml\
    python mail.py
    send mail successfully!
    
server

    [root@db ~]# tail -f /var/log/maillog
    Dec 19 17:57:34 oa postfix/smtpd[4397]: connect from unknown[192.168.1.1]
    Dec 19 17:57:34 oa postfix/smtpd[4397]: C683287A03: client=unknown[192.168.1.1], sasl_method=CRAM-MD5, sasl_username=me
    Dec 19 17:57:34 oa postfix/cleanup[4404]: C683287A03: message-id=<>
    Dec 19 17:57:34 oa postfix/qmgr[2159]: C683287A03: from=<me@egolife.com>, size=4331, nrcpt=1 (queue active)
    Dec 19 17:57:34 oa postfix/smtpd[4397]: disconnect from unknown[192.168.1.1]
    Dec 19 17:57:35 oa postfix/smtp[4405]: C683287A03: to=<me@egolife.com>, relay=smtp.egolife.com[192.168.1.10]:25, delay=0.28, delays=0.04/0/0.02/0.22, dsn=2.0.0, status=sent (250 Message queued)
    Dec 19 17:57:35 oa postfix/qmgr[2159]: C683287A03: removed
	
##Reference

* [postfix](http://www.postfix.org/)
* [SASL](http://asg.web.cmu.edu/sasl/)