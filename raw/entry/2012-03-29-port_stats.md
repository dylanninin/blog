---
layout: post
title: Get Port Status on Windows and Linux
category : Miscellanies
tags : [Linux, Windows, Utilities]
---

偶尔会碰到myeclipse突然崩溃的情况，但tomcat服务还为关闭，再次启动myeclipse和tomcat时，会提示Address Already Bind。稍总结了下Windows和Linux下查看系统端口使用的一般方法。

## 进程与端口 

* 进程与端口一一对应；除了使用IP标识一台PC外，还需要使用端口标志与哪一个进程进行通信；
* 端口仅针对TCP、UDP应用。

## Window查找指定端口
    
### 主要步骤
    
1）查看被占用的端口号

    netstat -aon | findstr port_number
    
    netstat -aon | findstr 5000
    TCP    127.0.0.1:5000         0.0.0.0:0              LISTENING       3988
    TCP    127.0.0.1:50000        0.0.0.0:0              LISTENING       316

最后一列是该端口对应的进程PID；
             
2）查看该端口对应的进程

    tasklist | findstr pid
                    
    tasklist | findstr 3988
    python.exe                  3988 Console                 0      2,968 K
            
3）关闭进程

打开任务管理器，菜单->查看->选择列，勾选"PID(进程标识符)"即可显示PID，找到后结束该进程即可。
            
### 命令学习

netstat    
          
在命令行下输入: netstat -help，输出如下：

    显示协议统计信息和当前 TCP/IP 网络连接。


    NETSTAT [-a] [-b] [-e] [-n] [-o] [-p proto] [-r] [-s] [-v] [interval]


      -a            显示所有连接和监听端口。
      -b            显示包含于创建每个连接或监听端口的
                    可执行组件。在某些情况下已知可执行组件
                    拥有多个独立组件，并且在这些情况下
                    包含于创建连接或监听端口的组件序列
                    被显示。这种情况下，可执行组件名
                    在底部的 [] 中，顶部是其调用的组件，
                    等等，直到 TCP/IP 部分。注意此选项
                    可能需要很长时间，如果没有足够权限
                    可能失败。
      -e            显示以太网统计信息。此选项可以与 -s
                    选项组合使用。
      -n            以数字形式显示地址和端口号。
      -o            显示与每个连接相关的所属进程 ID。
      -p proto      显示 proto 指定的协议的连接；proto 可以是
                    下列协议之一: TCP、UDP、TCPv6 或 UDPv6。
                    如果与 -s 选项一起使用以显示按协议统计信息，proto 可以是下列协议之一:
                    IP、IPv6、ICMP、ICMPv6、TCP、TCPv6、UDP 或 UDPv6。
      -r            显示路由表。
      -s            显示按协议统计信息。默认地，显示 IP、
                    IPv6、ICMP、ICMPv6、TCP、TCPv6、UDP 和 UDPv6 的统计信息；
                    -p 选项用于指定默认情况的子集。
      -v            与 -b 选项一起使用时将显示包含于
                    为所有可执行组件创建连接或监听端口的
                    组件。
      interval      重新显示选定统计信息，每次显示之间
                    暂停时间间隔(以秒计)。按 CTRL+C 停止重新
                    显示统计信息。如果省略，netstat 显示当前
                    配置信息(只显示一次)

常用命令

* netstat -a 显示所有连接和端口号

* netstat -o  显示端口相关联的进程ID

* netstat -n 以数字形式显示地址和端口号

* netstat -r 显示路由表


## Linux下查找指定端口

### 主要步骤

1）查看端口
    
    netstat -anp | grep "port_number"
    
    #netstat -anp | grep 8100
    tcp        0      0 127.0.0.1:8100              0.0.0.0:*                   LISTEN      2388/soffice.bin 
    
2）查看端口对应的服务
    
    lsof -i:"port_number"
    
    # lsof -i:8100
    COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    soffice.b 2388   oa   15u  IPv4  12894      0t0  TCP dev.egolife.com:xprint-server (LISTEN)
    
端口服务对应列表可以通过/etc/services查找。


有些端口通过netstat查不出来，更可靠的办法是:  
    
    nmap -sT -O localhost
    
    # nmap -sT -O localhost

    Starting Nmap 5.21 ( http://nmap.org ) at 2013-11-01 08:49 CST
    Nmap scan report for localhost (127.0.0.1)
    Host is up (0.000036s latency).
    Hostname localhost resolves to 2 IPs. Only scanned 127.0.0.1
    rDNS record for 127.0.0.1: dev.egolife.com
    Not shown: 984 closed ports
    PORT     STATE SERVICE
    22/tcp   open  ssh
    25/tcp   open  smtp
    81/tcp   open  hosts2-ns
    111/tcp  open  rpcbind
    631/tcp  open  ipp
    873/tcp  open  rsync
    2048/tcp open  dls-monitor
    5222/tcp open  unknown
    5269/tcp open  unknown
    7070/tcp open  realserver
    7443/tcp open  unknown
    7777/tcp open  unknown
    8009/tcp open  ajp13
    8100/tcp open  unknown
    8300/tcp open  unknown
    9090/tcp open  zeus-admin
    No exact OS matches for host (If you know what OS is running on it, see http://nmap.org/submit/ ).
    TCP/IP fingerprint:
    OS:SCAN(V=5.21%D=11/1%OT=22%CT=1%CU=40338%PV=N%DS=0%DC=L%G=Y%TM=5272FA92%P=
    OS:x86_64-unknown-linux-gnu)SEQ(SP=105%GCD=1%ISR=10C%TI=Z%CI=Z%II=I%TS=A)OP
    OS:S(O1=M400CST11NW7%O2=M400CST11NW7%O3=M400CNNT11NW7%O4=M400CST11NW7%O5=M4
    OS:00CST11NW7%O6=M400CST11)WIN(W1=8000%W2=8000%W3=8000%W4=8000%W5=8000%W6=8
    OS:000)ECN(R=Y%DF=Y%T=40%W=8018%O=M400CNNSNW7%CC=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%
    OS:A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=Y%DF=Y%T=40%W=8000%S=O%A=S+%F=AS%O=M400CST
    OS:11NW7%RD=0%Q=)T4(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=
    OS:40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0
    OS:%Q=)T7(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=40%IPL=1
    OS:64%UN=0%RIPL=G%RID=G%RIPCK=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)

    Network Distance: 0 hops

    OS detection performed. Please report any incorrect results at http://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 11.87 seconds
    
3）关闭端口

iptables禁用端口

    iptables -A INPUT -p tcp --dport "port_number" -j DROP
    iptables -A OUTPUT -p tcp --dport "port_number" -j DROP 

关闭端口对应的进程

    kill -9 pid                         #9为信号量，表示立即强行删除一个进程
    pkill  "service_name"               #pkill会关闭所有同名服务，慎用

### 命令学习

使用man/info等查询命令帮助即可
