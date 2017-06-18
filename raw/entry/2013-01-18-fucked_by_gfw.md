---
layout: post
title: Fucked By GFW
category : Miscellanies
tags : [Network, Exception]
---

Today there's a network problem within my [Linode](http://www.linode.com/) VPS. And now this issue has been resolved with its' support.

## traceroute within my pc

traceroute to 198.74.50.175 from my PC within PRC.

	Xshell:\> tracert -d 198.74.50.175
	tracerote to 198.74.50.175, 30 hops max

	  1    <1 ms   <1 ms   <1 ms 	192.168.1.1 
	  2     5 ms     6 ms     1 ms  14.153.124.1 
	  3    46 ms     1 ms     4 ms  113.106.43.221 
	  4     3 ms     3 ms     8 ms  119.145.220.58 
	  5    50 ms     9 ms     7 ms  119.145.45.177 
	  6     4 ms     4 ms     4 ms  202.97.33.214 
	  7     *        *        *     timeout
	  8     *        *        *     timeout
	  9     *        *        *     timeout
	 10     *        *        *     timeout
	 11     *        *        *     timeout
	 12     *        *        *     timeout
	 13     *        *        *     timeout

## the last hop

The last accessible hop is 202.97.33.214:

	Hostname:	202.97.33.214
	ISP:	Chinanet Backbone Network

![backbone_of_chinanet](http://dylanninin.com/assets/images/2013/backbone_of_chinanet.png)


## my ip status

check blacklist status

![blacklist_status](http://dylanninin.com/assets/images/2013/blacklist_status.png)

## traceroute within linode

traceroute to 8.8.8.8 from my linode(login with Lish Web Console)

	[root@www ~]# traceroute 8.8.8.8                                                                  
	traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets                                        
	 1  router1-fmt.linode.com (184.105.143.85) 1.843ms  1.808ms  1.892ms                            
	 2  10gigabitethernet2-3.core1.fmt1.he.net (64.62.250.5) 8.029 ms  8.260ms  8.496ms               
	 3  10gigabitethernet1-1.core1.pao1.he.net (184.105.213.66) 1.830ms  1.862ms  1.888ms            
	 4  184.105.224.254 (184.105.224.254) 1.706ms  1.678ms  1.652ms                                  
	 5  216.239.49.250 (216.239.49.250) 4.857ms 2.088 ms 209.85.240.114 (209.85.240.114)  2.172ms    
	 6  209.85.250.63 (209.85.250.63) 2.145ms 209.85.250.64(209.85.250.64) 2.047ms 209.85.250.63(20
	9.85.250.63)  1.489ms                                                                               
	 7  216.239.49.198 (216.239.49.198)  21.191 ms  21.493 ms 216.239.47.186 (216.239.47.186)  21.266 ms 
	 8  72.14.233.202 (72.14.233.202)  24.267 ms 72.14.233.200 (72.14.233.200)  23.998 ms 72.14.233.202 (
	72.14.233.202)  24.180 ms                                                                            
	 9  216.239.48.165 (216.239.48.165)  24.205 ms 64.233.174.129 (64.233.174.129)  24.362 ms 64.233.174.
	131 (64.233.174.131)  25.005 ms                                                                      
	10  * * *                                                                                            
	11  google-public-dns-a.google.com (8.8.8.8)  24.454 ms  24.407 ms  24.473 ms  
	
## route within linode

route within my linode(login with Lish Web Console)

	[root@www ~]# route -n                                                               
	Kernel IP routing table                                                                       
	Destination     Gateway         Genmask         Flags Metric Ref    Use Iface                        
	0.0.0.0         198.74.50.1     0.0.0.0         UG    0      0        0 eth0                         
	169.254.0.0     0.0.0.0         255.255.0.0     U     1003   0        0 eth0                         
	198.74.50.0     0.0.0.0         255.255.255.0   U     0      0        0 eth0                         


## ifconfig within linode

ifconfig within my linode(login with Lish Web Console)
                                                     
	[root@www ~]# ifconfig                                                                                                          
	eth0      Link encap:Ethernet  HWaddr F2:3C:91:AE:F2:41                                                                         
	          inet addr:198.74.50.175  Bcast:198.74.50.255  Mask:255.255.255.0                                                      
	          inet6 addr: 2600:3c01::f03c:91ff:feae:f241/64 Scope:Global                                                            
	          inet6 addr: fe80::f03c:91ff:feae:f241/64 Scope:Link                                                                   
	          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1                                                                    
	          RX packets:21495 errors:0 dropped:0 overruns:0 frame:0                                                                
	          TX packets:21738 errors:0 dropped:0 overruns:0 carrier:0                                                              
	          collisions:0 txqueuelen:1000                                                                                          
	          RX bytes:2800173 (2.6 MiB)  TX bytes:3993300 (3.8 MiB)                                                                
	          Interrupt:48                                                                                                          
	                                                                                                                                
	lo        Link encap:Local Loopback                                                                                             
	          inet addr:127.0.0.1  Mask:255.0.0.0                                                                                   
	          inet6 addr: ::1/128 Scope:Host                                                                                        
	          UP LOOPBACK RUNNING  MTU:16436  Metric:1                                                                              
	          RX packets:669 errors:0 dropped:0 overruns:0 frame:0                                                                  
	          TX packets:669 errors:0 dropped:0 overruns:0 carrier:0                                                                
	          collisions:0 txqueuelen:0                                                                                             
	          RX bytes:72979 (71.2 KiB)  TX bytes:72979 (71.2 KiB)  

Well, there's some issues lately with the GFW.

## reference

* [Using the Linode Shell(Lish)](http://library.linode.com/troubleshooting/using-lish-the-linode-shell)
* [whatismyipaddress.com](http://whatismyipaddress.com)
