## ISCSI

Internet SCSI (iSCSI) is a network protocol s that allows you to use of the SCSI protocol over TCP/IP networks. It is good alternative to Fibre Channel-based SANs. You can easily manage, mount and format iSCSI Volume under Linux. It allows access to SAN storage over Ethernet.

## Open-iSCSI Project

Open-iSCSI project is a high-performance, transport independent, multi-platform implementation of iSCSI. Open-iSCSI is partitioned into user and kernel parts.

Instructions are tested on:

* [a] RHEL 5
* [b] CentOS 5
* [c] Fedora 7
* [d] Debian / Ubuntu Linux

### Install Required Package

iscsi-initiator-utils RPM package - The iscsi package provides the server daemon for the iSCSI protocol, as well as the utility programs used to manage it. iSCSI is a protocol for distributed disk access using SCSI commands sent over Internet Protocol networks. This package is available under Redhat Enterprise Linux / CentOS / Fedora Linux and can be installed using yum command:

	# yum install iscsi-initiator-utils

A note about Debian / Ubuntu Linux

If you are using Debian / Ubuntu Linux install open-iscsi package, enter:
	
	$ sudo apt-get install open-iscsi

## CentOS / Red Hat Linux: Install and manage iSCSI Volume

### iSCSI Configuration

There are three steps needed to set up a system to use iSCSI storage:

* iSCSI startup using the init script or manual startup. You need to edit and configure iSCSI via `/etc/iscsi/iscsid.conf` file
* Discover targets.
* Automate target logins for future system reboots.

You also need to obtain iSCSI username, password and storage server IP address (target host)

#### Step # 1: Configure iSCSI

Open /etc/iscsi/iscsid.conf with vi text editor:

	# vi /etc/iscsi/iscsid.conf

Setup username and password:
node.session.auth.username = My_ISCSI_USR_NAME
node.session.auth.password = MyPassword
discovery.sendtargets.auth.username = My_ISCSI_USR_NAME
discovery.sendtargets.auth.password = MyPassword

Where,

* node.session.* is used to set a CHAP username and password for initiator authentication by the target(s).
* discovery.sendtargets.* is used to set a discovery session CHAP username and password for the initiator authentication by the target(s)

You may also need to tweak and set other options. Refer to man page for more information. Now start the iscsi service:

	# /etc/init.d/iscsi start

#### Step # 2: Discover targets

Now use iscsiadm command, which is a command-line tool allowing discovery and login to iSCSI targets, as well as access and management of the open-iscsi database. If your storage server IP address is 192.168.1.5, enter:
	
	# iscsiadm -m discovery -t sendtargets -p 192.168.1.5

	# /etc/init.d/iscsi restart

Now there should be a block device under /dev directory. To obtain new device name, type:

	# fdisk -l

or

	# tail -f /var/log/messages

Output:

	Oct 10 12:42:20 ora9is2 kernel:   Vendor: EQLOGIC   Model: 100E-00           Rev: 3.2
	Oct 10 12:42:20 ora9is2 kernel:   Type:   Direct-Access                      ANSI SCSI revision: 05
	Oct 10 12:42:20 ora9is2 kernel: SCSI device sdd: 41963520 512-byte hdwr sectors (21485 MB)
	Oct 10 12:42:20 ora9is2 kernel: sdd: Write Protect is off
	Oct 10 12:42:20 ora9is2 kernel: SCSI device sdd: drive cache: write through
	Oct 10 12:42:20 ora9is2 kernel: SCSI device sdd: 41963520 512-byte hdwr sectors (21485 MB)
	Oct 10 12:42:20 ora9is2 kernel: sdd: Write Protect is off
	Oct 10 12:42:20 ora9is2 kernel: SCSI device sdd: drive cache: write through
	Oct 10 12:42:20 ora9is2 kernel:  sdd: unknown partition table
	Oct 10 12:42:20 ora9is2 kernel: sd 3:0:0:0: Attached scsi disk sdd
	Oct 10 12:42:20 ora9is2 kernel: sd 3:0:0:0: Attached scsi generic sg3 type 0
	Oct 10 12:42:20 ora9is2 kernel: rtc: lost some interrupts at 2048Hz.
	Oct 10 12:42:20 ora9is2 iscsid: connection0:0 is operational now

`/dev/sdd` is my new block device.

#### Step # 3: Format and Mount iSCSI Volume

You can now partition and create a filesystem on the target using usual fdisk and mkfs.ext3 commands:

	# fdisk /dev/sdd
	# mke2fs -j -m 0 -O dir_index /dev/sdd1

OR
	
	# mkfs.ext3 /dev/sdd1

Tip: If your volume is large size like 1TB, run mkfs.ext3 in background using nohup:

	# nohup mkfs.ext3 /dev/sdd1 &

Mount new partition:
	
	# mkdir /mnt/iscsi
	# mount /dev/sdd1 /mnt/iscsi

#### Step #4: Mount iSCSI drive automatically at boot time

First make sure iscsi service turned on at boot time:

	# chkconfig iscsi on

Open `/etc/fstab` file and append config directive:
	
	/dev/sdd1 /mnt/iscsi ext3 _netdev 0 0

Save and close the file.

### Mount ISCSI on CentOS

1.discover

	[root@erptest1 ~]# iscsiadm -m discovery -t sendtargets -p 172.29.88.61
	172.29.88.61:3260,0 iqn.2000-01.com.synology:themain-2nd.oemfile
	169.254.146.25:3260,0 iqn.2000-01.com.synology:themain-2nd.oemfile
	172.29.88.61:3260,0 iqn.2000-01.com.synology:themain-2nd.cluster
	169.254.146.25:3260,0 iqn.2000-01.com.synology:themain-2nd.cluster
	172.29.88.61:3260,0 iqn.2000-01.com.synology:themain-2nd.transmission
	169.254.146.25:3260,0 iqn.2000-01.com.synology:themain-2nd.transmission
	172.29.88.61:3260,0 iqn.2000-01.com.synology:themain-2nd.mobile
	169.254.146.25:3260,0 iqn.2000-01.com.synology:themain-2nd.mobile
	172.29.88.61:3260,0 iqn.2000-01.com.synology:themain-2nd.mobilefile
	169.254.146.25:3260,0 iqn.2000-01.com.synology:themain-2nd.mobilefile
	172.29.88.61:3260,0 iqn.2000-01.com.synology:themain-2nd.test
	169.254.146.25:3260,0 iqn.2000-01.com.synology:themain-2nd.test
	172.29.88.61:3260,0 iqn.2000-01.com.synology:themain-2nd.erp
	169.254.146.25:3260,0 iqn.2000-01.com.synology:themain-2nd.erp

2.iscsid.conf

	vim /etc/iscsi/iscsid.conf

	. . .
	# *************
	# CHAP Settings
	# *************
	 
	# To enable CHAP authentication set node.session.auth.authmethod
	# to CHAP. The default is None.
	node.session.auth.authmethod = CHAP                
	 
	# To set a CHAP username and password for initiator
	# authentication by the target(s), uncomment the following lines:
	node.session.auth.username = backup
	node.session.auth.password = storageoabak
	. . .
	

3.login

	[root@erptest1 ~]# ll /dev/sd*
	brw-rw----. 1 root disk 8, 0 May 29 18:07 /dev/sda
	brw-rw----. 1 root disk 8, 1 May 29 10:48 /dev/sda1
	brw-rw----. 1 root disk 8, 2 May 29 10:48 /dev/sda2
	brw-rw----. 1 root disk 8, 3 May 29 10:48 /dev/sda3

	[root@erptest1 ~]#iscsiadm -m node -T iqn.2000-01.com.synology:themain-2nd.erp -p 172.29.88.61 --login
	Logging in to [iface: default, target: iqn.2000-01.com.synology:themain-2nd.erp, portal: 172.29.88.61,3260] (multiple)
	Login to [iface: default, target: iqn.2000-01.com.synology:themain-2nd.erp, portal: 172.29.88.61,3260] successful.

	[root@erptest1 ~]# ll /dev/sd*
	brw-rw----. 1 root disk 8,  0 May 29 18:07 /dev/sda
	brw-rw----. 1 root disk 8,  1 May 29 10:48 /dev/sda1
	brw-rw----. 1 root disk 8,  2 May 29 10:48 /dev/sda2
	brw-rw----. 1 root disk 8,  3 May 29 10:48 /dev/sda3
	brw-rw----. 1 root disk 8, 16 May 29 18:00 /dev/sdb

4.fdisk,mkfs ...

	fdisk ...

	mkfs ...

	[root@erptest1 ~]# fdisk -l /dev/sdb

	Disk /dev/sdb: 1099.5 GB, 1099511627776 bytes
	255 heads, 63 sectors/track, 133674 cylinders
	Units = cylinders of 16065 * 512 = 8225280 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disk identifier: 0xc1aa5473
	
	   Device Boot      Start         End      Blocks   Id  System
	/dev/sdb1               1      133674  1073736373+   5  Extended
	/dev/sdb5               1      133674  1073736342   83  Linux

5.mount

	[root@erptest1 ~]# mount -o acl,rw /dev/sdb5 /data/

## 测试

### 1.关于多重联机

多重联机即一个或多个客户端连接一块SAN分配的存储单元，不过为避免数据受损，必须确认在集群
架构下使用才行。

在测试过程中，使用新购置的两台ERP测试服务器共享一块网络存储，发现存在以下问题：

#### 多写

mount 均采用  `mount -o acl,rw /dev/sdb5 /data` 进行挂载；写数据时，都是使用root写入；

* a. 多台客户端可以同时挂载，但挂载后，写入的数据仅有自身可以看到，其他客户端不可见；
* b. 多台客户端可以同时挂载时，各客户端均有写入数据时，当时数据没有丢失，但是重新挂载网络设备时，会出现数据丢失的情况（只能看到最后写入的数据）；

#### 一写多读

* a. 多个客户端同时挂载，仅一个客户端写数据，其他读；在写入时，其他客户端暂时不可见，必须重新挂载；
* b. 关于AIX和Oracle Linux之间共享该网络存储（一写一读），Oracle Linux挂载jfs2文件系统时不识别，添加jfs相关的软件包后挂载失败；在CentOS 6.2上，添加jfs2软件包后可以挂载jfs2文件系统。对比后，发现Oracle Linux启动的内核为uek内核，可能和当前系统运行的内核相关。
 
### 2.其他

另外，测试了下使用SAN存储搭建NFS，多客户端可以同时读写，但速率很低。


## Reference

* [Linux ISCSI howto](http://www.cyberciti.biz/tips/rhel-centos-fedora-linux-iscsi-howto.html)
