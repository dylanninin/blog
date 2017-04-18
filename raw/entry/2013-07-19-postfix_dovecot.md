---
layout: post
title: Configure Posfix  with Dovecot
category : Linux
tags : [Linux, Utilities, Mail]
---

### OS Configuration

kernel

    [root@db ~]# uname -a
    Linux db.egolife.com 2.6.32-220.el6.x86_64 #1 SMP Tue Dec 6 19:48:22 GMT 2011 x86_64 x86_64 x86_64 GNU/Linux

account

    [root@db ~]# useradd -s /sbin/nologin me
    [root@db ~]# passwd me
    Changing password for user me.
    New password: 
    Retype new password: 
    passwd: all authentication tokens updated successfully.
    

### postfix and dovecot 

required packages

    [root@db ~]# rpm -qa | egrep 'sendmail|postfix|dovecot'
    dovecot-2.0.9-2.el6_1.1.x86_64
    postfix-2.6.6-2.2.el6_1.x86_64

config postfix
    
    postconf -e 'home_mailbox = Maildir/'
    postconf -e 'smtpd_sasl_type = dovecot'
    postconf -e 'smtpd_sasl_path = private/auth'
    postconf -e 'smtpd_sasl_security_options = noanonymous'
    postconf -e 'broken_sasl_auth_clients = yes'
    postconf -e 'smtpd_sasl_auth_enable = yes'
    postconf -e 'smtpd_recipient_restrictions = permit_sasl_authenticated, permit_mynetworks,reject_unauth_destination'
    postconf -e 'inet_interfaces = all'
    postconf -e 'mynetworks = 127.0.0.0/8, 172.17.1.100/32, 172.29.73.0/24'
    postconf -e 'myorigin = egolife.com'

    [root@db ~]#  grep '^\s*[^# \t].*$' /etc/postfix/main.cf 
    queue_directory = /var/spool/postfix
    command_directory = /usr/sbin
    daemon_directory = /usr/libexec/postfix
    data_directory = /var/lib/postfix
    mail_owner = postfix
    myorigin = egolife.com
    inet_interfaces = all
    inet_protocols = all
    mydestination = $myhostname, localhost.$mydomain, localhost
    unknown_local_recipient_reject_code = 550
    mynetworks = 127.0.0.0/8, 172.17.1.100/32, 172.29.73.0/24
    alias_maps = hash:/etc/aliases
    alias_database = hash:/etc/aliases
    debug_peer_level = 2
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
    home_mailbox = Maildir/
    smtpd_sasl_type = dovecot
    smtpd_sasl_path = private/auth
    smtpd_sasl_security_options = noanonymous
    broken_sasl_auth_clients = yes
    smtpd_sasl_auth_enable = yes
    smtpd_recipient_restrictions = permit_sasl_authenticated, permit_mynetworks,reject_unauth_destination

config dovecot
    
dovecot.conf
    
    [root@db ~]# vim /etc/dovecot/dovecot.conf 
    ... ...
    listen = 127.0.0.1, 172.17.1.100
    mail_location = maildir:~/mail
    ... ...

    [root@db ~]#  grep '^\s*[^# \t].*$' /etc/dovecot/dovecot.conf 
    listen = 127.0.0.1, 172.17.1.100
    mail_location = maildir:~/mail
    dict {
    }
    !include conf.d/*.conf

10-master.conf
    
    [root@db ~]# vim /etc/dovecot/conf.d/10-master.conf 
    ... ...
    service auth {
      # auth_socket_path points to this userdb socket by default. It's typically
      # used by dovecot-lda, doveadm, possibly imap process, etc. Its default
      # permissions make it readable only by root, but you may need to relax these
      # permissions. Users that have access to this socket are able to get a list
      # of all usernames and get results of everyone's userdb lookups.
      unix_listener auth-userdb {
        #mode = 0600
        #user = 
        #group = 
      }

      # Postfix smtp-auth
      unix_listener /var/spool/postfix/private/auth {
        mode = 0666
      }

      # Auth process is run as this user.
      #user = $default_internal_user
    }

    [root@db ~]#  grep '^\s*[^# \t].*$' /etc/dovecot/conf.d/10-master.conf 
    service imap-login {
      inet_listener imap {
      }
      inet_listener imaps {
      }
    }
    service pop3-login {
      inet_listener pop3 {
      }
      inet_listener pop3s {
      }
    }
    service lmtp {
      unix_listener lmtp {
      }
    }
    service imap {
    }
    service pop3 {
    }
    service auth {
      unix_listener auth-userdb {
      }
      unix_listener /var/spool/postfix/private/auth {
        mode = 0666
      }
    }
    service auth-worker {
    }
    service dict {
      unix_listener dict {
      }
    }

10-auth.conf
    
    [root@db ~]# vim /etc/dovecot/conf.d/10-auth.conf 
    ... ...
    disable_plaintext_auth = no
    ... ...
    auth_mechanisms = plain login
    ... ...
    passdb {
        driver = shadow
    }
    ... ...

    [root@db ~]#  grep '^\s*[^# \t].*$' /etc/dovecot/conf.d/10-auth.conf 
    disable_plaintext_auth = no
    auth_mechanisms = plain login
    passdb {
        driver = shadow
    }
    !include auth-system.conf.ext

### chkconfig and start service
    
chkconfig 
    
    [root@db ~]# chkconfig postfix on
    [root@db ~]# chkconfig dovecot on

start service

    [root@db ~]# service postfix restart
    Shutting down postfix:                                     [  OK  ]
    Starting postfix:                                          [  OK  ]
    [root@db ~]# service dovecot restart
    Stopping Dovecot Imap:                                     [  OK  ]
    Starting Dovecot Imap:                                     [  OK  ]
    
### mail test

script 

    F:\Workspace\python\pydev\mail\eml\mail.py

client 

    cd /d  F:\Workspace\python\pydev\mail\eml\
    python mail.py
    send mail successfully!
    
server log

    [root@db ~]# tail -f /var/log/maillog
    Jul 19 17:35:09 db postfix/smtpd[16361]: connect from unknown[192.168.1.1]
    Jul 19 17:35:09 db postfix/smtpd[16361]: 160E68047E: client=unknown[192.168.1.1], sasl_method=PLAIN, sasl_username=me
    Jul 19 17:35:09 db postfix/cleanup[16370]: 160E68047E: message-id=<>
    Jul 19 17:35:09 db postfix/qmgr[16304]: 160E68047E: from=<me@egolife.com>, size=4298, nrcpt=1 (queue active)
    Jul 19 17:35:09 db postfix/smtpd[16361]: disconnect from unknown[192.168.1.1]
    Jul 19 17:35:09 db postfix/smtp[16371]: connect to gmail-smtp-in.l.google.com[2607:f8b0:400e:c03::1a]:25: Network is unreachable
    Jul 19 17:35:13 db postfix/smtp[16371]: 160E68047E: to=<dylanninin@gmail.com>, relay=gmail-smtp-in.l.google.com[74.125.25.26]:25, delay=4.2, delays=0.04/0/0.93/3.2, dsn=2.0.0, status=sent (250 2.0.0 OK 1374226522 pf2si10055347pac.244 - gsmtp)
    Jul 19 17:35:13 db postfix/qmgr[16304]: 160E68047E: removed

## Reference

* [postfix](http://www.postfix.org/)
* [dovecot](http://www.dovecot.org/)