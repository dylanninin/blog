---
layout: post
title: NIC Channel Bond on Linux
category : Linux
tags : [Linux, Network]
---

##Binding Configure

1.服务器

	dev1 为服务端，ip为 192.168.1.7，计划使用eth2,eth3聚合绑定成虚拟网卡bond0。
	dev2 为客户端，ip为192.168.1.10。
	若无指明，则传输文件测试是从 dev1 传输到 dev2，传输为单文件，大小为9.7G。

2.网络结构

    dev1，dev2的网卡均连接到同一个物理交换机。

3.测试要点

   a.带宽：主要测试双网卡绑定时，带宽是否有增加，传输是否更快；主要使用time查看时间，scp带实时的传输速率显示。
   b.冗余：主要测试双网卡绑定时，其中一个网卡工作异常，是否会走另外一个网卡；主要使用netstat查看数据包。

4.测试点

主要分为单网卡、网卡绑定（分模式0，1,6，以及在6下禁用其中一个网卡）的测试：
  
  * a.单网卡测试
  * b.模式0绑定：负载均衡方式，两块网卡都工作，需要交换机作支持
  * c.模式1绑定：冗余方式，网卡只有一个工作，一个出问题启用另外的
  * d.模式6绑定：负载均衡方式，两块网卡都工作，不需要交换机作支持
  * e.模式6绑定时禁用一个网卡
  * f.模式6绑定时禁用一个网卡，从客户端到服务端传输
  * 注：a,b,c,d,e均是从服务端到客户端传输文件。
  
5. mode

Allows you to specify the bonding policy. The 'value' can be one of:

* balance-rr or 0 — Sets a round-robin policy for fault tolerance and load balancing. Transmissions are received and sent out sequentially on each bonded slave interface beginning with the first one available.
* active-backup or 1 — Sets an active-backup policy for fault tolerance. Transmissions are received and sent out via the first available bonded slave interface. Another bonded slave interface is only used if the active bonded slave interface fails.
* balance-xor or 2 — Sets an XOR (exclusive-or) policy for fault tolerance and load balancing. Using this method, the interface matches up the incoming request's MAC address with the MAC address for one of the slave NICs. Once this link is established, transmissions are sent out sequentially beginning with the first available interface.
* broadcast or 3 — Sets a broadcast policy for fault tolerance. All transmissions are sent on all slave interfaces.
* `802.3ad` or 4 — Sets an IEEE 802.3ad dynamic link aggregation policy. Creates aggregation groups that share the same speed and duplex settings. Transmits and receives on all slaves in the active aggregator. Requires a switch that is 802.3ad compliant.
* balance-tlb or 5 — Sets a Transmit Load Balancing (TLB) policy for fault tolerance and load balancing. The outgoing traffic is distributed according to the current load on each slave interface. Incoming traffic is received by the current slave. If the receiving slave fails, another slave takes over the MAC address of the failed slave.
* balance-alb or 6 — Sets an Active Load Balancing (ALB) policy for fault tolerance and load balancing. Includes transmit and receive load balancing for IPV4 traffic. Receive load balancing is achieved through ARP negotiation.

6.测试结论

 * a.带宽：单网卡和双网卡绑定时相比，带宽并无明显差异。
 * b.冗余：双网卡绑定有冗余效果，正在传输时，其中一个网卡工作异常，会自动走另外一个网卡，暂且没有出现数据包丢失的现象。

Network Interface

	[root@dev1 etc]# uname -a
	Linux dev1.egolife.com 2.6.39-400.17.1.el6uek.x86_64 #1 SMP Fri Feb 22 18:16:18 PST 2013 x86_64 x86_64 x86_64 GNU/Linux

	[root@dev1 etc]# lspci | grep Ethernet
	04:00.0 Ethernet controller: Broadcom Corporation NetXtreme II BCM5709 Gigabit Ethernet (rev 20)
	04:00.1 Ethernet controller: Broadcom Corporation NetXtreme II BCM5709 Gigabit Ethernet (rev 20)
	0e:00.0 Ethernet controller: Intel Corporation 82580 Gigabit Network Connection (rev 01)
	0e:00.1 Ethernet controller: Intel Corporation 82580 Gigabit Network Connection (rev 01)

##Single Interface

ifconfig

	[root@dev1 ~]# ifconfig -a
	eth0      Link encap:Ethernet  HWaddr 6C:AE:8B:78:4C:44  
			  inet addr:172.29.73.7  Bcast:172.29.73.255  Mask:255.255.255.0
			  inet6 addr: fe80::6eae:8bff:fe78:4c44/64 Scope:Link
			  UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
			  RX packets:8679827 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:11695363 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:1000 
			  RX bytes:10981189708 (10.2 GiB)  TX bytes:11622829842 (10.8 GiB)

	eth1      Link encap:Ethernet  HWaddr 6C:AE:8B:78:4C:46  
			  BROADCAST MULTICAST  MTU:1500  Metric:1
			  RX packets:0 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:1000 
			  RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)

	eth2      Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CA  
			  BROADCAST MULTICAST  MTU:1500  Metric:1
			  RX packets:0 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:1000 
			  RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)

	eth3      Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CB  
			  BROADCAST MULTICAST  MTU:1500  Metric:1
			  RX packets:0 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:1000 
			  RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)

	lo        Link encap:Local Loopback  
			  inet addr:127.0.0.1  Mask:255.0.0.0
			  inet6 addr: ::1/128 Scope:Host
			  UP LOOPBACK RUNNING  MTU:16436  Metric:1
			  RX packets:16 errors:0 dropped:0 overruns:0 frame:0
			  TX packets:16 errors:0 dropped:0 overruns:0 carrier:0
			  collisions:0 txqueuelen:0 
			  RX bytes:960 (960.0 b)  TX bytes:960 (960.0 b)

route

	[root@dev1 ~]# route 
	Kernel IP routing table
	Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
	default         172.29.73.1     0.0.0.0         UG    0      0        0 eth0
	link-local      *               255.255.0.0     U     1002   0        0 eth0
	link-local      *               255.255.0.0     U     1007   0        0 eth1
	172.29.73.0     *               255.255.255.0   U     0      0        0 eth0
	192.168.1.0     *               255.255.255.0   U     0      0        0 eth1

ping

	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	^C
	--- 192.168.1.10 ping statistics ---
	43 packets transmitted, 0 received, 100% packet loss, time 42421ms

eth2

	[root@dev1 ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth2
	DEVICE=eth2
	HWADDR=90:E2:BA:43:4F:CA
	TYPE=Ethernet
	UUID=c57d0153-e9d7-42a0-bc6b-4cc3295d4796
	IPADDR=192.168.1.7
	BROADCAST=192.168.1.255
	NETMASK=255.255.255.0
	ONBOOT=no
	NM_CONTROLLED=no
	BOOTPROTO=static
	IPV6INIT=no
	USERCTL=no

	[root@dev1 ~]# ifup eth2

	[root@dev1 ~]# ifconfig eth2
	eth2      Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CA  
	          inet addr:192.168.1.7  Bcast:192.168.1.255  Mask:255.255.255.0
	          inet6 addr: fe80::92e2:baff:fe43:4fca/64 Scope:Link
	          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
	          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:6 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000 
	          RX bytes:0 (0.0 b)  TX bytes:412 (412.0 b)
	
	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	64 bytes from 192.168.1.10: icmp_seq=1 ttl=64 time=1.42 ms
	^C
	--- 192.168.1.10 ping statistics ---
	1 packets transmitted, 1 received, 0% packet loss, time 626ms
	rtt min/avg/max/mdev = 1.423/1.423/1.423/0.000 ms

speed test

	[root@dev1 ~]# ll -h /u2
	total 9.7G
	drwx------. 2 root root  16K Jun 26 15:28 lost+found
	-rw-r--r--. 1 root root 9.7G Jun 26 16:39 oracle_1213_apps.tar.gz

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	The authenticity of host '192.168.1.10 (192.168.1.10)' can't be established.
	RSA key fingerprint is d2:6f:03:40:a0:78:a9:71:1e:c4:6f:73:e4:d8:4f:7b.
	Are you sure you want to continue connecting (yes/no)? yes
	Warning: Permanently added '192.168.1.10' (RSA) to the list of known hosts.
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 110.7MB/s   01:29    
	
	real	1m35.725s
	user	0m58.625s
	sys		0m39.648s

##Configure bond0 with eth2, eth3

###Channel Bonding Configure

bond0

	[root@dev1 ~]# cat /etc/sysconfig/network-scripts/ifcfg-bond0
	DEVICE=bond0
	BOOTPROTO=none
	IPADDR=192.168.1.7
	BROADCAST=192.168.1.255
	NETMASK=255.255.255.0
	ONBOOT=yes
	TYPE=Ethernet
	USERCTL=no
	IPV6INIT=no
	PEERDNS=yes

binding eth2,eth3 to bond0

	[root@dev1 ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth2
	DEVICE=eth2
	TYPE=Ethernet
	ONBOOT=yes
	BOOTPROTO=no

	[root@dev1 ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth3
	DEVICE=eth3
	TYPE=Ethernet
	ONBOOT=yes
	BOOTPROTO=no

modprobe with mode 0


	[root@dev1 ~]# cat /etc/modprobe.conf 
	alias eth2 pcnet32
	alias eth3 pcnet32
	alias scsi_hostadapter mptbase
	alias scsi_hostadapter3 mptspi
	alias scsi_hostadapter4 ata_piix
	alias peth0 pcnet32
	alias bond0 bonding
	options bond0 miimon=100 mode=0
	
注：

* miimon 是链路监测的时间间隔单位是毫秒，miimon=100的意思就是，每100毫秒检测网卡和交换机之间是否连通，如不通则使用另外的链路。
* mode:
	mode=0 表示负载均衡方式，两块网卡都工作，需要交换机作支持  
  	mode=1 表示冗余方式，网卡只有一个工作，一个出问题启用另外的
	mode=6 表示负载均衡方式，两块网卡都工作，不需要交换机作支持

enslave

    [root@dev1 ~]# ifenslave bond1 eth2 eth3
    Master 'bond1': Error: handshake with driver failed. Aborting

    [root@dev1 ~]# dmesg | tail
    ADDRCONF(NETDEV_UP): bond0: link is not ready
    Loading kernel module for a network device with CAP_SYS_MODULE (deprecated).  Use CAP_NET_ADMIN and alias netdev-bond1 instead
    ADDRCONF(NETDEV_UP): eth2: link is not ready
    ADDRCONF(NETDEV_UP): eth3: link is not ready
    igb: eth2 NIC Link is Up 1000 Mbps Full Duplex, Flow Control: None
    ADDRCONF(NETDEV_CHANGE): eth2: link becomes ready
    igb: eth3 NIC Link is Up 1000 Mbps Full Duplex, Flow Control: None
    ADDRCONF(NETDEV_CHANGE): eth3: link becomes ready
    eth2: no IPv6 routers present
    
restart network

	[root@dev1 ~]# service network restart
	Shutting down interface bond0:                             [  OK  ]
	Shutting down interface eth0:                              [  OK  ]
	Shutting down loopback interface:                          [  OK  ]
	Bringing up loopback interface:                            [  OK  ]
	Bringing up interface bond0:                               [  OK  ]
	Bringing up interface eth0:                                [  OK  ]
	Bringing up interface eth2:                                [  OK  ]
	Bringing up interface eth3:                                [  OK  ]

enslave
    
    [root@dev1 ~]# ifenslave bond1 eth2 eth3
    
ping

	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	^C
	--- 192.168.1.10 ping statistics ---
	43 packets transmitted, 0 received, 100% packet loss, time 42421ms
    
	[root@dev1 ~]# ifconfig bond0
	bond0     Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CA  
	          inet addr:192.168.1.7  Bcast:192.168.1.255  Mask:255.255.255.0
	          inet6 addr: fe80::92e2:baff:fe43:4fca/64 Scope:Link
	          UP BROADCAST RUNNING MASTER MULTICAST  MTU:1500  Metric:1
	          RX packets:729735 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:7551346 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:0 
	          RX bytes:52531377 (50.0 MiB)  TX bytes:10862582133 (10.1 GiB)

注：
	
	bond0: the mac address is set to the mac address of the first slave nic.

route

	[root@dev1 ~]# route 
	Kernel IP routing table
	Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
	default         172.29.73.1     0.0.0.0         UG    0      0        0 eth0
	link-local      *               255.255.0.0     U     1002   0        0 eth0
	link-local      *               255.255.0.0     U     1004   0        0 eth2
	link-local      *               255.255.0.0     U     1005   0        0 eth3
	link-local      *               255.255.0.0     U     1007   0        0 bond0
	172.29.73.0     *               255.255.255.0   U     0      0        0 eth0
	192.168.1.0     *               255.255.255.0   U     0      0        0 bond0

###mode 0

ping

	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	64 bytes from 192.168.1.10: icmp_seq=1 ttl=64 time=1.69 ms
	64 bytes from 192.168.1.10: icmp_seq=2 ttl=64 time=0.287 ms
	^C
	--- 192.168.1.10 ping statistics ---
	2 packets transmitted, 2 received, 0% packet loss, time 1395ms
	rtt min/avg/max/mdev = 0.287/0.992/1.697/0.705 ms

test

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 109.5MB/s   01:30    
	
	real	1m32.922s
	user	0m58.353s
	sys		0m46.081s

ifconfig to view traffic throughout

	[root@dev1 ~]# ifconfig bond0
	bond0     Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CA  
	          inet addr:192.168.1.7  Bcast:192.168.1.255  Mask:255.255.255.0
	          inet6 addr: fe80::92e2:baff:fe43:4fca/64 Scope:Link
	          UP BROADCAST MASTER MULTICAST  MTU:1500  Metric:1
	          RX packets:3879393 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:14996073 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:0 
	          RX bytes:307412626 (293.1 MiB)  TX bytes:21719128132 (20.2 GiB)

	[root@dev1 ~]# ifconfig eth2
	eth2      Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CA  
	          inet addr:192.168.1.7  Bcast:192.168.1.255  Mask:255.255.255.0
	          UP BROADCAST RUNNING SLAVE MULTICAST  MTU:1500  Metric:1
	          RX packets:3879390 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:10718053 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000 
	          RX bytes:307412446 (293.1 MiB)  TX bytes:15398686700 (14.3 GiB)
	
	[root@dev1 ~]# ifconfig eth3	
	eth3      Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CA  
	          UP BROADCAST RUNNING SLAVE MULTICAST  MTU:1500  Metric:1
	          RX packets:3 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:4278020 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000 
	          RX bytes:180 (180.0 b)  TX bytes:6320441432 (5.8 GiB)
	
bring down eth2, eth3

	[root@dev1 ~]# ifdown eth2
	
	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	64 bytes from 192.168.1.10: icmp_seq=1 ttl=64 time=1.13 ms
	64 bytes from 192.168.1.10: icmp_seq=2 ttl=64 time=0.256 ms
	64 bytes from 192.168.1.10: icmp_seq=3 ttl=64 time=0.236 ms
	^C
	--- 192.168.1.10 ping statistics ---
	3 packets transmitted, 3 received, 0% packet loss, time 2596ms
	rtt min/avg/max/mdev = 0.236/0.542/1.134/0.418 ms


	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 112.0MB/s   01:28    
	
	real	1m31.001s
	user	0m59.142s
	sys		0m30.835s

	[root@dev1 ~]# ifdown eth3

	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	^C
	--- 192.168.1.10 ping statistics ---
	7 packets transmitted, 0 received, 100% packet loss, time 6996ms

	[root@dev1 ~]# ifup eth2

	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	64 bytes from 192.168.1.10: icmp_seq=1 ttl=64 time=2005 ms
	64 bytes from 192.168.1.10: icmp_seq=2 ttl=64 time=1005 ms
	64 bytes from 192.168.1.10: icmp_seq=3 ttl=64 time=5.55 ms
	64 bytes from 192.168.1.10: icmp_seq=4 ttl=64 time=0.283 ms
	^C
	--- 192.168.1.10 ping statistics ---
	4 packets transmitted, 4 received, 0% packet loss, time 3950ms
	rtt min/avg/max/mdev = 0.283/754.118/2005.167/830.199 ms, pipe 3

	[root@dev1 ~]# ifup eth3

	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	64 bytes from 192.168.1.10: icmp_seq=1 ttl=64 time=0.253 ms
	64 bytes from 192.168.1.10: icmp_seq=2 ttl=64 time=0.290 ms
	^C
	--- 192.168.1.10 ping statistics ---
	2 packets transmitted, 2 received, 0% packet loss, time 1639ms
	rtt min/avg/max/mdev = 0.253/0.271/0.290/0.024 ms
	
	[root@dev1 ~]# ifconfig 
	bond0     Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CA  
	          inet addr:192.168.1.7  Bcast:192.168.1.255  Mask:255.255.255.0
	          inet6 addr: fe80::92e2:baff:fe43:4fca/64 Scope:Link
	          UP BROADCAST RUNNING MASTER MULTICAST  MTU:1500  Metric:1
	          RX packets:4544721 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:22217942 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:0 
	          RX bytes:355677703 (339.2 MiB)  TX bytes:32559983059 (30.3 GiB)
	
	eth0      Link encap:Ethernet  HWaddr 6C:AE:8B:78:4C:44  
	          inet addr:172.29.73.7  Bcast:172.29.73.255  Mask:255.255.255.0
	          inet6 addr: fe80::6eae:8bff:fe78:4c44/64 Scope:Link
	          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
	          RX packets:854 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:497 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000 
	          RX bytes:80825 (78.9 KiB)  TX bytes:76148 (74.3 KiB)
	
	eth2      Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CA  
	          UP BROADCAST SLAVE MULTICAST  MTU:1500  Metric:1
	          RX packets:3879467 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:10718143 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000 
	          RX bytes:307419536 (293.1 MiB)  TX bytes:15398694004 (14.3 GiB)
	
	eth3      Link encap:Ethernet  HWaddr 90:E2:BA:43:4F:CA  
	          UP BROADCAST RUNNING SLAVE MULTICAST  MTU:1500  Metric:1
	          RX packets:665254 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:11499799 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:1000 
	          RX bytes:48258167 (46.0 MiB)  TX bytes:17161289055 (15.9 GiB)
	
	lo        Link encap:Local Loopback  
	          inet addr:127.0.0.1  Mask:255.0.0.0
	          inet6 addr: ::1/128 Scope:Host
	          UP LOOPBACK RUNNING  MTU:16436  Metric:1
	          RX packets:293 errors:0 dropped:0 overruns:0 frame:0
	          TX packets:293 errors:0 dropped:0 overruns:0 carrier:0
	          collisions:0 txqueuelen:0 
	          RX bytes:31960 (31.2 KiB)  TX bytes:31960 (31.2 KiB)

bring down bind0

	[root@dev1 ~]# ifdown bond0

	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	^C
	--- 192.168.1.10 ping statistics ---
	3 packets transmitted, 0 received, 100% packet loss, time 2719ms

bring up bond0

	[root@dev1 ~]# ifup bond0

	[root@dev1 ~]# ping 192.168.1.10
	PING 192.168.1.10 (192.168.1.10) 56(84) bytes of data.
	64 bytes from 192.168.1.10: icmp_seq=1 ttl=64 time=0.402 ms
	64 bytes from 192.168.1.10: icmp_seq=2 ttl=64 time=0.293 ms
	64 bytes from 192.168.1.10: icmp_seq=3 ttl=64 time=0.290 ms
	^C
	--- 192.168.1.10 ping statistics ---
	3 packets transmitted, 3 received, 0% packet loss, time 2490ms
	rtt min/avg/max/mdev = 0.290/0.328/0.402/0.054 ms

	[root@dev1 ~]# netstat -i
	Kernel Interface table
	Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
	bond0      1500   0  4544721      0      0      0 22217942      0      0      0 BMmRU
	eth0       1500   0      995      0      0      0      622      0      0      0 BMRU
	eth2       1500   0  3879467      0      0      0 10718143      0      0      0 BMsRU
	eth3       1500   0   665254      0      0      0 11499799      0      0      0 BMsRU
	lo        16436   0      293      0      0      0      293      0      0      0 LRU

###mode 1

	[root@dev1 ~]# cat /etc/modprobe.conf 
	alias eth2 pcnet32
	alias eth3 pcnet32
	alias scsi_hostadapter mptbase
	alias scsi_hostadapter3 mptspi
	alias scsi_hostadapter4 ata_piix
	alias peth0 pcnet32
	alias bond0 bonding
	options bond0 miimon=100 mode=1

	[root@dev1 ~]# service network restart
	... ...
	
	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 110.7MB/s   01:29    
	
	real	1m31.298s
	user	0m55.667s
	sys		0m43.423s

	[root@dev1 ~]# netstat -i
	Kernel Interface table
	Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
	bond0      1500   0  8764945      0      0      0 29542976      0      0      0 BMmRU
	eth0       1500   0      201      0      0      0      167      0      0      0 BMRU
	eth2       1500   0  3879467      0      0      0 14399423      0      0      0 BMsRU
	eth3       1500   0  4885478      0      0      0 15143553      0      0      0 BMsRU
	lo        16436   0      293      0      0      0      293      0      0      0 LRU

	[root@dev1 ~]# ifdown eth2

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 112.0MB/s   01:28    
	
	real	1m31.059s
	user	0m59.240s
	sys		0m30.670s

	[root@dev1 ~]# netstat -i
	Kernel Interface table
	Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
	bond0      1500   0  9432589      0      0      0 36767111      0      0      0 BMmRU
	eth0       1500   0      440      0      0      0      329      0      0      0 BMRU
	eth3       1500   0  5553122      0      0      0 22367688      0      0      0 BMsRU
	lo        16436   0      293      0      0      0      293      0      0      0 LRU

###mode 6

	[root@dev1 ~]# cat /etc/modprobe.conf 
	alias eth2 pcnet32
	alias eth3 pcnet32
	alias scsi_hostadapter mptbase
	alias scsi_hostadapter3 mptspi
	alias scsi_hostadapter4 ata_piix
	alias peth0 pcnet32
	alias bond0 bonding
	options bond0 miimon=100 mode=6

	[root@dev1 ~]# service network restart
	... ...

scp test

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 110.7MB/s   01:29    
	
	real	1m31.287s
	user	0m56.114s
	sys		0m44.767s

netstat

	[root@dev1 ~]# netstat -i
	Kernel Interface table
	Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
	bond0      1500   0 13269295      0      0      0 44134140      0      0      0 BMmRU
	eth0       1500   0      211      0      0      0      162      0      0      0 BMRU
	eth2       1500   0  3879467      0      0      0 18195589      0      0      0 BMsRU
	eth3       1500   0  9389828      0      0      0 25938551      0      0      0 BMsRU
	lo        16436   0      293      0      0      0      293      0      0      0 LRU

bring down eth3

	[root@dev1 ~]# ifdown eth3
	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 112.0MB/s   01:28    
	
	real	1m30.996s
	user	0m58.047s
	sys		0m39.067s

netstat

	[root@dev1 ~]# ifup eth3
	[root@dev1 ~]# netstat -i
	Kernel Interface table
	Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
	bond0      1500   0 13990944      0      0      0 51618873      0      0      0 BMmRU
	eth0       1500   0      447      0      0      0      324      0      0      0 BMRU
	eth2       1500   0  4601116      0      0      0 25680322      0      0      0 BMsRU
	eth3       1500   0  9389828      0      0      0 25938551      0      0      0 BMsRU
	lo        16436   0      293      0      0      0      293      0      0      0 LRU

when file transfering, bring down eth2

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 100.6MB/s   01:38    
	
	real	1m40.639s
	user	0m59.232s
	sys		0m38.922s

	[root@dev1 ~]# ifup eth2

after completing transfering

	[root@dev1 ~]# netstat -i
	Kernel Interface table
	Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
	bond0      1500   0 14854993      0      0      0 58942784      0      0      0 BMmRU
	eth0       1500   0     5220      0      0      0     2745      0      0      0 BMRU
	eth2       1500   0  4868378      0      0      0 26232685      0      0      0 BMsU
	eth3       1500   0  9986615      0      0      0 32710099      0      0      0 BMsRU
	lo        16436   0      325      0      0      0      325      0      0      0 LRU

from client to server, while file transfering, bring down eth2
	
	[root@erpdb2 /]# time scp /tmp/oracle_1213_apps.tar.gz 192.168.1.7:/tmp
	root@192.168.1.7's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 108.3MB/s   01:31    
	
	real	1m37.377s
	user	0m58.969s
	sys		0m33.968s

	[root@dev1 ~]# ifdown eth3

after completing transfering

	[root@dev1 ~]# ifup eth3

	[root@dev1 ~]# netstat -i
	Kernel Interface table
	Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
	bond0      1500   0 22419759      0      0      0 59667621      0      0      0 BMmRU
	eth0       1500   0     5412      0      0      0     2882      0      0      0 BMRU
	eth2       1500   0 11898827      0      0      0 26932401      0      0      0 BMsRU
	eth3       1500   0 10520932      0      0      0 32735220      0      0      0 BMsU
	lo        16436   0      325      0      0      0      325      0      0      0 LRU

##Test Summary

eth2

	[root@dev1 ~]# ll -h /u2
	total 9.7G
	drwx------. 2 root root  16K Jun 26 15:28 lost+found
	-rw-r--r--. 1 root root 9.7G Jun 26 16:39 oracle_1213_apps.tar.gz

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	The authenticity of host '192.168.1.10 (192.168.1.10)' can't be established.
	RSA key fingerprint is d2:6f:03:40:a0:78:a9:71:1e:c4:6f:73:e4:d8:4f:7b.
	Are you sure you want to continue connecting (yes/no)? yes
	Warning: Permanently added '192.168.1.10' (RSA) to the list of known hosts.
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 110.7MB/s   01:29    
	
	real	1m35.725s
	user	0m58.625s
	sys		0m39.648s

bonding mode 0 载均衡方式，两块网卡都工作，需要交换机作支持

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 110.7MB/s   01:29    
	
	real	1m31.298s
	user	0m55.667s
	sys		0m43.423s

bonding mode 1 表示冗余方式，网卡只有一个工作，一个出问题启用另外的

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 110.7MB/s   01:29    
	
	real	1m31.298s
	user	0m55.667s
	sys		0m43.423s

bonding mode 6 表示负载均衡方式，两块网卡都工作，不需要交换机作支持

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 110.7MB/s   01:29    
	
	real	1m31.287s
	user	0m56.114s
	sys		0m44.767s

bonding mode 6, when file transfering, bring down eth2

	[root@dev1 ~]# time scp /u2/oracle_1213_apps.tar.gz 192.168.1.10:/tmp
	root@192.168.1.10's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 100.6MB/s   01:38    
	
	real	1m40.639s
	user	0m59.232s
	sys		0m38.922s

after completing transfering

	[root@dev1 ~]# ifup eth2

	[root@dev1 ~]# netstat -i
	Kernel Interface table
	Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
	bond0      1500   0 14854993      0      0      0 58942784      0      0      0 BMmRU
	eth0       1500   0     5220      0      0      0     2745      0      0      0 BMRU
	eth2       1500   0  4868378      0      0      0 26232685      0      0      0 BMsU
	eth3       1500   0  9986615      0      0      0 32710099      0      0      0 BMsRU
	lo        16436   0      325      0      0      0      325      0      0      0 LRU

binding mode 6, from client to server, while file transfering, bring down eth2
	
	[root@erpdb2 /]# time scp /tmp/oracle_1213_apps.tar.gz 192.168.1.7:/tmp
	root@192.168.1.7's password: 
	oracle_1213_apps.tar.gz                                                                                                                 100% 9855MB 108.3MB/s   01:31    
	
	real	1m37.377s
	user	0m58.969s
	sys		0m33.968s

	[root@dev1 ~]# ifdown eth3

after completing transfering

	[root@dev1 ~]# ifup eth3

	[root@dev1 ~]# netstat -i
	Kernel Interface table
	Iface       MTU Met    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
	bond0      1500   0 22419759      0      0      0 59667621      0      0      0 BMmRU
	eth0       1500   0     5412      0      0      0     2882      0      0      0 BMRU
	eth2       1500   0 11898827      0      0      0 26932401      0      0      0 BMsRU
	eth3       1500   0 10520932      0      0      0 32735220      0      0      0 BMsU
	lo        16436   0      325      0      0      0      325      0      0      0 LRU

##Reference

* [Oracle RAC与网卡绑定](http://blog.csdn.net/tianlesoftware/article/details/6189639)
* [Linux 双网卡绑定测试](http://www.cnblogs.com/killkill/archive/2009/02/15/1390717.html)
* [Redhat Deployment_Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html-single/Deployment_Guide/index.html#sec-Using_Channel_Bonding)