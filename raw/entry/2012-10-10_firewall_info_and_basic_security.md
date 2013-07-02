#写在前面的话
Firewall，又称防火墙，顾名思义，即作为一道屏障防止火势蔓延。这正如战乱纷繁的诸侯列国在重要的城池一般都有护城河、城墙、高山等层层屏障一样，若遇敌国侵袭，或者各种动乱，则可以逐层抵挡以期缓解局势；说到这儿，你一定想到了，可以拿八达岭长城作比，它似乎确凿已经起到了阻挡蛮夷隔离战火之功。

![greate wall](http://www.dylanninin.com/blog/images/2012/10/greate_wall.jpg)

既然防火墙可以抵挡外来入侵，从另外一个方面想，防火墙同样也可以限制内部资源向外蹦蹿从而引发骚乱，想想《Prison Break》中监狱里的防电网，也想想万里长城的"庆长假，量大，无侧翻"的稳定。

![overflow](http://www.dylanninin.com/blog/images/2012/10/greate_wall_overflow.jpg)

到这里，相信我们已经可以基本理解防火墙的最基本功能，即隔离，或在地域上，或在文化上，或在网络上。在计算机领域，防火墙是一项协助信息安全的设备，可以制定一些特定的规则，允许或限制数据的传输，从而将网络划分成不同的区域，制定出不同区域之间的访问控制策略进而来控制不同区域间传送的数据流。通常，这些区域可以划分为两大类，即不可信任的区域，和可信任或高信任的区域。典型的不可信区域即互联网，因为互联网对每个人、每个设备都是开放的，可以说鱼龙混杂，好坏难分，一不小心你的对话就有可能人被窃听，或者你的QQ号被盗，再或者服务器被黑客入侵等等。通常，一个内部网络可以被称为高信任的区域，因为内部网络的组成十分单纯，网络工程师们已经尽力做了很多预期的设想和限制，而且若不是别有用心，你绝不会冒失地去攻击内部网络的某某服务器。当内部网络即可信任区域需要与外网即不可信任区域通信交流时，若没有任何保护措施，这几乎等同于把服务器放在了黑客面前并说请随意入侵；可想而知，这种情形下，内部网络的可信任性就受到了质疑。此时，防火墙即可担此重任，负责内外网的通信安全。

![firewall](http://www.dylanninin.com/blog/images/2012/10/firewall.png)

在现代操作系统中，大多已经自带了网络防火墙，通过定义一些分组规则，进行互联网、主机之间数据过滤，来保证主机的相对安全。

在内核2.6.x的Linux系统中，自带了iptables防火墙，通常可以利用分组进行过滤，如来源IP地址或端口号、目的IP地址或端口号、服务类型（如WWW或是FTP），也可以是通信协议、来源网域、网段、网卡等。

#VPS防火墙设置

本站VPS使用的操作系统为CentOS 6.2，建站初期已经开启了防火墙服务，并制定了一些规则，过滤掉一些不用或有危害的请求。

在一个简单的博客系统主机中，可以仅开启http（80端口）、https（443端口）、ssh（22端口）这些服务，其中http/https用于web请求，加密或非加密；ssh用来远程登录，其他则禁止。

检查防火墙是否应开启：

	[root@www web]# service iptables status

若没有开启，则运行以下命令，开启防火墙：

	[root@www web]# service iptables start

没有添加自定义规则的防火墙，也是采取了一些默认的接收或者拒绝请求的策略，但通常这些策略太宽泛，因此我们需要自定义规则，进行严格的限制，从而创建一个相对安全的网络环境。

创建文件，添加自定义规则：

	[root@www web]# vim /etc/iptables.rule
	
	*filter
	
	# Allow all loopback (lo0) traffic and drop all traffic to 127/8 that doesn't use lo0
	-A INPUT -i lo -j ACCEPT
	-A INPUT -d 127.0.0.0/8 -j REJECT
	
	# Accept all established inbound connections
	-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
	
	# Allow all outbound traffic - you can modify this to only allow certain traffic
	-A OUTPUT -j ACCEPT
	
	# Allow HTTP and HTTPS connections from anywhere (the normal ports for websites and SSL).
	-A INPUT -p tcp --dport 80 -j ACCEPT
	-A INPUT -p tcp --dport 443 -j ACCEPT
	
	# Allow SSH connections
	#
	# The -dport number should be the same port number you set in sshd_config
	#
	-A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT
	
	# Allow ping
	-A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT
	
	# Log iptables denied calls
	-A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7
	
	# Reject all other inbound - default deny unless explicitly allowed policy
	-A INPUT -j REJECT
	-A FORWARD -j REJECT
	
	COMMIT
	
以上防火墙规则说明已经十分详细，不再赘述。

让防火墙规则生效

	[root@www web]# iptables-restore <  /etc/iptables.rule

查看防火墙规则是否生效：

	[root@www web]# iptables -L
	Chain INPUT (policy ACCEPT)
	target prot opt source destination 
	ACCEPT all -- anywhere anywhere 
	REJECT all -- anywhere loopback/8 reject-with icmp-port-unreachable 
	ACCEPT all -- anywhere anywhere state RELATED,ESTABLISHED 
	ACCEPT tcp -- anywhere anywhere tcp dpt:http 
	ACCEPT tcp -- anywhere anywhere tcp dpt:https 
	ACCEPT tcp -- anywhere anywhere state NEW tcp dpt:ssh 
	ACCEPT icmp -- anywhere anywhere icmp echo-request 
	LOG all -- anywhere anywhere limit: avg 5/min burst 5 LOG level debug prefix `iptables denied: ' 
	REJECT all -- anywhere anywhere reject-with icmp-port-unreachable
	
	Chain FORWARD (policy ACCEPT)
	target prot opt source destination 
	REJECT all -- anywhere anywhere reject-with icmp-port-unreachable
	
	Chain OUTPUT (policy ACCEPT)
	target prot opt source destination 
	ACCEPT all -- anywhere anywhere

最后，要保证服务器开机时就能够自动开启防火墙服务，并执行以上规则。此时需要做以下两点：

##设置自动启动级别

	[root@www web]# chkconfig --list iptables
	iptables 0:off 1:off 2:on 3:on 4:on 5:on 6:off

在2,3,4,5级别上设置为自动开启即可，若有在这些级别上为off的，则设置为on：

	[root@www web]# chkconfig --level 2345  iptables on

##开机启动

编辑rc.local文件，让系统初始化完成后，自动加载以上规则

	[root@www web]# vim  /etc/rc.d/rc.local
	/sbin/iptables-restore <  /etc/iptables.rule

这样，简单的防火墙基础安全防护工作已经完成。

#延伸阅读

* [CentOS Wiki：HowTos/Network/IPTables](http://wiki.centos.org/HowTos/Network/IPTables)
* [新浪共享资料：2小时玩转iptables](http://ishare.iask.sina.com.cn/f/18503162.html)

#参考

* [Linode中文教程：做好VPS的基础安全防护工作](http://www.linode.im/1642.html)
* [维基百科：防火墙](http://zh.wikipedia.org/wiki/%E9%98%B2%E7%81%AB%E5%A2%99)
* [维基百科：runlevel](http://en.wikipedia.org/wiki/Runlevel)