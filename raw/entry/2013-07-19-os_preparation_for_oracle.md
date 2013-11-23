---
layout: post
title: OS Preparation for Oracle Database
category : Oracle
tags : [Oracle, Database, DBA, Linux]
---

##OS Configuration

### kernel

    [root@db ~]# uname -a
    Linux db.egolife.com 2.6.32-220.el6.x86_64 #1 SMP Tue Dec 6 19:48:22 GMT 2011 x86_64 x86_64 x86_64 GNU/Linux

### hosts

	[root@db ~]# cat /etc/hosts
	127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
	::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
	172.17.1.100  db.egolife.com db
	172.29.88.135 wxbak.egolife.com wxbak

##Database 11gR2

### group and user

    [root@db ~]# groupadd -g 501 oinstall
    [root@db ~]# groupadd -g 502 dba
    [root@db ~]# useradd -u 501 -g oinstall -G dba oracle
    [root@db ~]# id oracle
    uid=501(oracle) gid=501(oinstall) groups=501(oinstall),502(dba)
    [root@db ~]# passwd oracle

###	kernel parameters

* `/proc/sys/.../file`: current value of these parameters; non persistent * `/etc/sysctl.conf`: configure file of these parameters; persistent during each startup * `sysctl -p`: persistent during each startup 

#### parameters

shared memory, semaphores, file handles parameter, net parameter 
	
    [root@db ~]# sysctl -p
    net.ipv4.ip_forward = 0
    net.ipv4.conf.default.rp_filter = 1
    net.ipv4.conf.default.accept_source_route = 0
    kernel.sysrq = 0
    kernel.core_uses_pid = 1
    net.ipv4.tcp_syncookies = 1
    error: "net.bridge.bridge-nf-call-ip6tables" is an unknown key
    error: "net.bridge.bridge-nf-call-iptables" is an unknown key
    error: "net.bridge.bridge-nf-call-arptables" is an unknown key
    kernel.msgmnb = 65536
    kernel.msgmax = 65536
    kernel.shmmax = 68719476736
    kernel.shmall = 4294967296

    [root@db ~]# vim /etc/sysctl.conf
    ... ...
    #2013-7-19  kernel setting for oracle database 11gR2
    fs.aio-max-nr = 1048576
    fs.file-max = 6815744
    kernel.shmall = 2097152
    kernel.shmmax = 4294967295
    kernel.shmmni = 4096
    kernel.sem = 250 32000 100 128
    net.ipv4.ip_local_port_range = 9000 65500
    net.core.rmem_default = 262144
    net.core.rmem_max = 4194304
    net.core.wmem_default = 262144
    net.core.wmem_max = 1048576
    
    [root@db ~]# sysctl -p
    net.ipv4.ip_forward = 0
    net.ipv4.conf.default.rp_filter = 1
    net.ipv4.conf.default.accept_source_route = 0
    kernel.sysrq = 0
    kernel.core_uses_pid = 1
    net.ipv4.tcp_syncookies = 1
    kernel.msgmnb = 65536
    kernel.msgmax = 65536
    kernel.shmmax = 68719476736
    kernel.shmall = 4294967296
    fs.aio-max-nr = 1048576
    fs.file-max = 6815744
    kernel.shmall = 2097152
    kernel.shmmax = 4294967295
    kernel.shmmni = 4096
    kernel.sem = 250 32000 100 128
    net.ipv4.ip_local_port_range = 9000 65500
    net.core.rmem_default = 262144
    net.core.rmem_max = 4194304
    net.core.wmem_default = 262144
    net.core.wmem_max = 1048576

### resource limits
* `/etc/security.conf`: resource limits configuration file 
* `/etc/pam.d/login`: login settings * `ulimit`: utility to check or change resource limits 

open file descriptors, number of processes available to a single user, size of the 
stack segment of the process.


    [root@db ~]# ulimit -Sn; ulimit -Hn
    1024
    1024
    [root@db ~]# ulimit -Su; ulimit -Hu
    1024
    62638
    [root@db ~]# ulimit -Ss; ulimit -Hs
    10240
    unlimited

    [root@db ~]# vim /etc/security/limits.conf 
    ... ...
    #2013-7-19  resource limits for oracle database 11gR2
    oracle              soft    nproc   2047
    oracle              hard    nproc   16384
    oracle              soft    nofile  1024
    oracle              hard    nofile  65536
    oracle              soft    stack   10240
    
    [root@db ~]# vim /etc/pam.d/login 
    ... ...
    #2013-7-19 shell limits for oracle database 11gR2
    session    required     /lib64/security/pam_limits.so
    session    required     pam_limits.so
    
### managing packages
for Oracle Linux 6 and Red Hat Enterprise Linux 6 x86-64, the following packages (or later versions) must be installed:

* binutils-2.20.51.0.2-5.11.el6 (x86_64)
* compat-libcap1-1.10-1 (x86_64)
* compat-libstdc++-33-3.2.3-69.el6 (x86_64)
* compat-libstdc++-33-3.2.3-69.el6.i686
* gcc-4.4.4-13.el6 (x86_64)
* gcc-c++-4.4.4-13.el6 (x86_64)
* glibc-2.12-1.7.el6 (i686)
* glibc-2.12-1.7.el6 (x86_64)
* glibc-devel-2.12-1.7.el6 (x86_64)
* glibc-devel-2.12-1.7.el6.i686
* ksh
* libgcc-4.4.4-13.el6 (i686)
* libgcc-4.4.4-13.el6 (x86_64)
* libstdc++-4.4.4-13.el6 (x86_64)
* libstdc++-4.4.4-13.el6.i686
* libstdc++-devel-4.4.4-13.el6 (x86_64)
* libstdc++-devel-4.4.4-13.el6.i686
* libaio-0.3.107-10.el6 (x86_64)
* libaio-0.3.107-10.el6.i686
* libaio-devel-0.3.107-10.el6 (x86_64)
* libaio-devel-0.3.107-10.el6.i686
* make-3.81-19.el6
* sysstat-9.0.4-11.el6 (x86_64)

query packages installed

    [root@db ~]#  rpm -qa --queryformat "%{NAME}-%{VERSION}-%{RELEASE} (%{ARCH})\n" | egrep 'binutils|compat-db43|gcc|glibc|libgcc|libstdc++|libXi|libXp|libaio|libgomp|make|gdbm|sysstat|util-linux-ng|unzip|compat-libstdc++|compat-libstdc++|openmotif21|xorg-x11-libs-compat' | sort
    automake-1.11.1-1.2.el6 (noarch)
    binutils-2.20.51.0.2-5.28.el6 (x86_64)
    binutils-devel-2.20.51.0.2-5.28.el6 (x86_64)
    compat-db43-4.3.29-15.el6 (x86_64)
    compat-glibc-2.5-46.2 (x86_64)
    compat-glibc-headers-2.5-46.2 (x86_64)
    compat-libstdc++-296-2.96-144.el6 (i686)
    compat-libstdc++-33-3.2.3-69.el6 (x86_64)
    gcc-4.4.6-3.el6 (x86_64)
    gcc-c++-4.4.6-3.el6 (x86_64)
    gcc-gfortran-4.4.6-3.el6 (x86_64)
    gdbm-1.8.0-36.el6 (x86_64)
    glibc-2.12-1.47.el6 (i686)
    glibc-2.12-1.47.el6 (x86_64)
    glibc-common-2.12-1.47.el6 (x86_64)
    glibc-devel-2.12-1.47.el6 (x86_64)
    glibc-headers-2.12-1.47.el6 (x86_64)
    libaio-0.3.107-10.el6 (x86_64)
    libgcc-4.4.6-3.el6 (i686)
    libgcc-4.4.6-3.el6 (x86_64)
    libgomp-4.4.6-3.el6 (x86_64)
    libstdc++-4.4.6-3.el6 (x86_64)
    libstdc++-devel-4.4.6-3.el6 (x86_64)
    libXi-1.3-3.el6 (x86_64)
    libXi-devel-1.3-3.el6 (x86_64)
    libXinerama-1.1-1.el6 (x86_64)
    libXinerama-devel-1.1-1.el6 (x86_64)
    libXp-1.0.0-15.1.el6 (x86_64)
    libXp-devel-1.0.0-15.1.el6 (x86_64)
    make-3.81-19.el6 (x86_64)
    sysstat-9.0.4-18.el6 (x86_64)
    unzip-6.0-1.el6 (x86_64)
    util-linux-ng-2.17.2-12.4.el6 (x86_64)
    
to be installed packages: 

* compat-libcap1-1.10-1 (x86_64)
* glibc-devel-2.12-1.47.el6
* ksh
* libstdc++-4.4.6-3.el6
* libstdc++-devel-4.4.6-3.el6
* libaio-0.3.107-10.el6
* libaio-devel-0.3.107-10.el6, libaio-devel-0.3.107-10.el6 (x86_64)
* make-3.81-19.el6

### OFA

    [root@db ~]# mkdir -p /db/oracle/product/11.2.0/db_1
    [root@db ~]# chown -R oracle:oinstall /db/oracle/product/11.2.0/db_1/
    [root@db ~]# chmod -R 755 /db/oracle/

### Profile

    [root@db ~]# su - oracle
    
    [oracle@db ~]$ vim .bash_profile 
    # .bash_profile

    # Get the aliases and functions
    if [ -f ~/.bashrc ]; then
        . ~/.bashrc
    fi

    # User specific environment and startup programs

    PATH=$PATH:$HOME/bin

    export PATH

    #2013-7-19 settings for oracle database 11gR2
    export TMP=/tmp
    export TMPDIR=$TMP
    export ORACLE_BASE=/db/oracle
    export ORACLE_HOME=/db/oracle/product/11.2.0/db_1
    export ORACLE_SID=WXPROD
    export PATH=$PATH:$ORACLE_HOME/bin

### X Window System
### nobody

### Install Database

logon as oracle with X Manager or VNC

## Basic Security

### root account

    [root@db ~]# useradd itsection
    [root@db ~]# usermod -G 10 itsection
    [root@db ~]# grep '^\s*[^# \t].*$' /etc/pam.d/su
    auth		sufficient	pam_rootok.so
    auth		required	pam_wheel.so use_uid
    auth		include		system-auth
    account		sufficient	pam_succeed_if.so uid = 0 use_uid quiet
    account		include		system-auth
    password	include		system-auth
    session		include		system-auth
    session		optional	pam_xauth.so

itsection su test    
   
    [itsection@db ~]$ su - 
    Password: 
    [root@db ~]# 
    
oracle su test

    [oracle@db ~]$ su - 
    Password: 
    su: incorrect password
    [oracle@db ~]$ 
    
### ssh

use oracle as example

    [root@db ~]# su - oracle
    
    [oracle@db ~]$ ssh-keygen 
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/oracle/.ssh/id_rsa): 
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Passphrases do not match.  Try again.
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /home/oracle/.ssh/id_rsa.
    Your public key has been saved in /home/oracle/.ssh/id_rsa.pub.
    The key fingerprint is:
    e5:d9:51:82:97:d9:4d:11:1a:57:af:aa:5f:f0:36:e6 oracle@db.egolife.com
    The key's randomart image is:
    +--[ RSA 2048]----+
    |           ..=.**|
    |          . +o= o|
    |          ....  .|
    |         o o . . |
    |        S o o .  |
    |             +   |
    |            . *  |
    |           . = . |
    |          ... E  |
    +-----------------+
    [oracle@db ~]$ cd .ssh/
    [oracle@db .ssh]$ ll
    total 8
    -rw-------. 1 oracle oinstall 1743 Jul 22 09:23 id_rsa
    -rw-r--r--. 1 oracle oinstall  406 Jul 22 09:23 id_rsa.pub
    [oracle@db .ssh]$ cat id_rsa.pub > authorized_keys
    [oracle@db .ssh]$ chmod 600 authorized_keys 
    [root@db ~]# grep '^\s*[^# \t].*$' /etc/ssh/sshd_config 
    Protocol 2
    SyslogFacility AUTHPRIV
    PermitRootLogin no
    PasswordAuthentication no
    ChallengeResponseAuthentication no
    GSSAPIAuthentication yes
    GSSAPICleanupCredentials yes
    UsePAM yes
    AcceptEnv LANG LC_CTYPE LC_NUMERIC LC_TIME LC_COLLATE LC_MONETARY LC_MESSAGES
    AcceptEnv LC_PAPER LC_NAME LC_ADDRESS LC_TELEPHONE LC_MEASUREMENT
    AcceptEnv LC_IDENTIFICATION LC_ALL LANGUAGE
    AcceptEnv XMODIFIERS
    X11Forwarding yes
    Subsystem	sftp	/usr/libexec/openssh/sftp-server
    [root@db ~]# service sshd restart
    
### iptables

    [root@db ~]# cat /etc/iptables.rule 
    # Generated by iptables-save v1.4.7 on Mon Jul 22 09:56:41 2013
    *filter
    :INPUT ACCEPT [0:0]
    :FORWARD ACCEPT [0:0]
    :OUTPUT ACCEPT [0:0]
    -A INPUT -i lo -j ACCEPT 
    -A INPUT -d 127.0.0.0/8 -j REJECT --reject-with icmp-port-unreachable 
    -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT 
    -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT 
    -A INPUT -p tcp -m tcp --dport 8080 -j ACCEPT 
    -A INPUT -s 172.29.73.0/24 -p tcp -m tcp --dport 25 -j ACCEPT 
    -A INPUT -s 172.29.73.0/24 -p tcp -m tcp --dport 1521 -j ACCEPT 
    -A INPUT -s 172.29.73.0/24 -p tcp -m state --state NEW -m tcp --dport 22 -j ACCEPT 
    -A INPUT -s 172.29.88.135/32 -j ACCEPT 
    -A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT 
    -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7 
    -A INPUT -j REJECT --reject-with icmp-port-unreachable 
    -A FORWARD -j REJECT --reject-with icmp-port-unreachable 
    -A OUTPUT -j ACCEPT 
    COMMIT
    # Completed on Mon Jul 22 09:56:41 2013
    # Generated by iptables-save v1.4.7 on Mon Jul 22 09:56:41 2013
    *nat
    :PREROUTING ACCEPT [1:64]
    :POSTROUTING ACCEPT [12:1378]
    :OUTPUT ACCEPT [12:1378]
    -A PREROUTING -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 8080 
    COMMIT
    # Completed on Mon Jul 22 09:56:41 2013

    [root@db ~]# iptables-restore < /etc/iptables.rule 
    [root@db ~]# iptables-save > /etc/iptables.rule
    
    [root@db ~]# cat /etc/rc.local 
    #!/bin/sh
    #
    # This script will be executed *after* all the other init scripts.
    # You can put your own initialization stuff in here if you don't
    # want to do the full Sys V style init stuff.

    touch /var/lock/subsys/local
    su - c "iptables-restore < /etc/iptables.rule"
    