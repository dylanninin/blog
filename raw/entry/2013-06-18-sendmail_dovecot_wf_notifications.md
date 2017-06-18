---
layout: post
title: Configure Sendmail, Dovecot  for EBS
category : Oracle
tags : [Oracle, DBA, EBS, Mail, Utilities]
---

## Workflow Notification Mailer

Operation: System Administrator -> Oracle Application Manager: Workflow -> Notification Mailers -> Edit

Basic Configuration:

Details:
	Name: Workflow Notification Mailer
	
Outbount EMail Account(SMTP):
	Server Name: smtp.egolife.com
	Username:itsection
	Password:secret
	
Inbount Email Account(IMAP):
	check Inbound Processing
	Server Name:dev.egolife.com
	Username:me
	Password:secret
	Reply-To Address: me@dev.egolife.com

## Sendmail Configuration

check sendmail service 

	[root@dev ~]# yum install -y sendmail
	Loaded plugins: refresh-packagekit, security
	Setting up Install Process
	Package sendmail-8.14.4-8.el6.x86_64 already installed and latest version
	Nothing to do

	[root@dev ~]# service sendmail status
	sendmail dead but subsys locked
	sm-client (pid  32048) is running...

	[root@dev ~]# service sendmail stop
	Shutting down sm-client:                                   [  OK  ]
	Shutting down sendmail:                                    [FAILED]

	[root@dev ~]# service sendmail status
	sendmail is stopped
	sm-client is stopped

	[root@dev ~]# service sendmail start
	Starting sendmail:                                         [  OK  ]
	Starting sm-client:                                        [  OK  ]

	[root@dev ~]# chkconfig sendmail on

	[root@dev ~]# less /var/log/maillog
	Jun 18 14:33:45 dev sendmail[32366]: NOQUEUE: SYSERR(root): opendaemonsocket: daemon MTA: cannot bind: Address already in use
	Jun 18 14:33:45 dev sendmail[32366]: daemon MTA: problem creating SMTP socket
	Jun 18 14:33:50 dev sendmail[32366]: NOQUEUE: SYSERR(root): opendaemonsocket: daemon MTA: cannot bind: Address already in use
	Jun 18 14:33:50 dev sendmail[32366]: daemon MTA: problem creating SMTP socket
	Jun 18 14:33:55 dev sendmail[32366]: NOQUEUE: SYSERR(root): opendaemonsocket: daemon MTA: cannot bind: Address already in use
	Jun 18 14:33:55 dev sendmail[32366]: daemon MTA: problem creating SMTP socket
	Jun 18 14:34:00 dev sendmail[32366]: NOQUEUE: SYSERR(root): opendaemonsocket: daemon MTA: cannot bind: Address already in use
	Jun 18 14:34:00 dev sendmail[32366]: daemon MTA: problem creating SMTP socket
	Jun 18 14:34:00 dev sendmail[32366]: NOQUEUE: SYSERR(root): opendaemonsocket: daemon MTA: server SMTP socket wedged: exiting

stop postfix and restart sendmail

	[root@dev ~]# lsof -i:25
	COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
	master  31226 root   12u  IPv4 734327      0t0  TCP *:smtp (LISTEN)
	master  31226 root   13u  IPv6 734329      0t0  TCP *:smtp (LISTEN)

	[root@dev ~]# service postfix status
	master (pid  31226) is running...

	[root@dev ~]# service postfix stop
	Shutting down postfix:                                     [  OK  ]

	[root@dev ~]# lsof -i:25

	[root@dev ~]# service sendmail restart
	Shutting down sm-client:                                   [  OK  ]
	Shutting down sendmail:                                    [FAILED]
	Starting sendmail:                                         [  OK  ]
	Starting sm-client:                                        [  OK  ]

	[root@dev ~]# lsof -i:25

reinstall sendmail packages

	[root@dev ~]# rpm -qa | grep sendmail
	sendmail-cf-8.14.4-8.el6.noarch
	sendmail-8.14.4-8.el6.x86_64

	[root@dev ~]# rpm -e --nodeps sendmail
	[root@dev ~]# rpm -e --nodeps sendmail-cf


	[root@dev ~]# yum install -y sendmail
	[root@dev ~]# yum install -y sendmail-cf

add listen ip

	[root@dev ~]# vim /etc/mail/sendmail.mc
	DAEMON_OPTIONS(`Port=smtp,Addr=127.0.0.1, Name=MTA')dnl
	DAEMON_OPTIONS(`Port=smtp,Addr=192.168.1.6, Name=MTA')dnl

	[root@dev ~]# service sendmail restart
	Shutting down sm-client:                                   [  OK  ]
	Shutting down sendmail:                                    [FAILED]
	Starting sendmail:                                         [  OK  ]
	Starting sm-client:                                        [  OK  ]

	[root@dev ~]# lsof -i:25
	COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
	sendmail 3948 root    4u  IPv4 763157      0t0  TCP localhost:smtp (LISTEN)
	sendmail 3948 root    5u  IPv4 763158      0t0  TCP dev.egolife.com:smtp (LISTEN)
	
sendmail test

	[root@dev ~]# cat /etc/mail/sendmail.mc | mail -s "no-reply:sendmail test from `hostname`" me@egolife.com

	[root@dev ~]# tail /var/log/maillog
	Jun 18 17:34:38 dev sendmail[4201]: r5I9YcUV004201: from=root, size=7516, class=0, nrcpts=1, msgid=<201306180934.r5I9YcUV004201@dev.egolife.com>, relay=root@localhost
	Jun 18 17:34:38 dev sendmail[4202]: r5I9YcOE004202: from=<root@dev.egolife.com>, size=7772, class=0, nrcpts=1, msgid=<201306180934.r5I9YcUV004201@dev.egolife.com>, proto=ESMTP, daemon=MTA, relay=localhost [127.0.0.1]
	Jun 18 17:34:39 dev sendmail[4201]: r5I9YcUV004201: to=me@egolife.com, ctladdr=root (0/0), delay=00:00:01, xdelay=00:00:01, mailer=relay, pri=37516, relay=[127.0.0.1] [127.0.0.1], dsn=2.0.0, stat=Sent (r5I9YcOE004202 Message accepted for delivery)
	Jun 18 17:34:39 dev sendmail[4204]: r5I9YcOE004202: to=<me@egolife.com>, ctladdr=<root@dev.egolife.com> (0/0), delay=00:00:01, xdelay=00:00:00, mailer=esmtp, pri=127772, relay=smtp.egolife.com. [172.29.88.10], dsn=2.0.0, stat=Sent (Message queued)

## Dovecot Configuration

add listen ip and set mail location

	[root@dev ~]# vim /etc/dovecot/dovecot.conf 
	... ...
	listen = 127.0.0.1, 192.168.1.6
	mail_location = maildir:~/mail
	... ...

set auth mechanisms

	[root@dev ~]# vim /etc/dovecot/conf.d/10-auth.conf 
	... ...
	disable_plaintext_auth = no
	... ...
	# NOTE: See also disable_plaintext_auth setting.
	auth_mechanisms = plain login
	... ...
	##
	## Password and user databases
	##
	passdb {
	    driver = shadow
	}
	... ...

restart dovecot

	[root@dev ~]# service dovecot restart
	Stopping Dovecot Imap:                                     [  OK  ]
	Starting Dovecot Imap:                                     [  OK  ]
	[root@dev ~]# chkconfig dovecot on

	[root@dev ~]# lsof -i:143
	COMMAND  PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
	dovecot 5661 root   20u  IPv4 771014      0t0  TCP localhost:imap (LISTEN)
	dovecot 5661 root   21u  IPv4 771015      0t0  TCP dev.egolife.com:imap (LISTEN)
	
view maillog

	[root@dev ~]# tail /var/log/maillog
	Jun 18 18:16:21 dev dovecot: imap-login: Disconnected (no auth attempts): rip=192.168.1.6, lip=192.168.1.6, secured
	Jun 18 18:16:22 dev dovecot: imap-login: Login: user=<me>, method=PLAIN, rip=192.168.1.6, lip=192.168.1.6, mpid=5768, secured
	Jun 18 18:16:24 dev dovecot: imap-login: Disconnected (no auth attempts): rip=192.168.1.6, lip=192.168.1.6, secured
	Jun 18 18:16:26 dev dovecot: imap(me): Disconnected: Logged out bytes=76/773

## Test Mailer in EBS App Node

Operation: System Administrator -> Oracle Application Manager: Workflow -> Notification Mailers -> Edit -> Test Mailer

WF Mailer NOTIFICATIONS

Workflow Mailer Perference Settings

	SQL> SELECT NAME, DISPLAY_NAME, NOTIFICATION_PREFERENCE, EMAIL_ADDRESS, STATUS FROM WF_LOCAL_ROLES WHERE NAME = UPPER('&fnd_user_name');
	Enter value for fnd_user_name: me
	old   1: SELECT NAME, DISPLAY_NAME, NOTIFICATION_PREFERENCE, EMAIL_ADDRESS, STATUS FROM WF_LOCAL_ROLES WHERE NAME = UPPER('&fnd_user_name')
	new   1: SELECT NAME, DISPLAY_NAME, NOTIFICATION_PREFERENCE, EMAIL_ADDRESS, STATUS FROM WF_LOCAL_ROLES WHERE NAME = UPPER('me')

	NAME	   DISPLAY_NA NOTIFICATION_PREFERE EMAIL_ADDRESS		  STATUS
	---------- ---------- -------------------- ------------------------------ --------------------
	me    		我自己,    MAILHTML             me@egolife.com        ACTIVE

	SQL> SELECT NAME, DISPLAY_NAME, NOTIFICATION_PREFERENCE, EMAIL_ADDRESS, STATUS FROM WF_LOCAL_ROLES WHERE NAME = UPPER('&fnd_user_name');
	Enter value for fnd_user_name: sysadmin
	old   1: SELECT NAME, DISPLAY_NAME, NOTIFICATION_PREFERENCE, EMAIL_ADDRESS, STATUS FROM WF_LOCAL_ROLES WHERE NAME = UPPER('&fnd_user_name')
	new   1: SELECT NAME, DISPLAY_NAME, NOTIFICATION_PREFERENCE, EMAIL_ADDRESS, STATUS FROM WF_LOCAL_ROLES WHERE NAME = UPPER('sysadmin')

	NAME	   DISPLAY_NA NOTIFICATION_PREFERE EMAIL_ADDRESS		  STATUS
	---------- ---------- -------------------- ------------------------------ --------------------
	SYSADMIN   SYSADMIN   MAILHTML						  ACTIVE

WF Mailer Notification Status

	SQL> SELECT NOTIFICATION_ID, MESSAGE_NAME, RECIPIENT_ROLE, MAIL_STATUS FROM WF_NOTIFICATIONS WFN WHERE WFN.SENT_DATE > SYSDATE - 1;
	
	... ...
	
## Reference

* [sendmail](http://www.sendmail.com/)
* [dovecot](http://www.dovecot.org/)
