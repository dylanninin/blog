---
layout: post
title: Access Dapenti via VPN
category : Miscellanies
tags : [Windows, Network, Exception]
---

当登陆VPN时你已经可以正常访问一些在gfw列表中的网站；但很可能国内的一些网站却不能 打开了，比如[打喷嚏](http://dapenti.org)，此时你就需要看下本机的路由设置是否正 确。因为连接VPN后本机的默认路由可能已经更改，此时所有的连接都会经过默认路由出去； 而由于文化、版权等原因，国内很多网站往往是不对境外提供服务的。此时则需要针对这些 网站手动添加路由，这样访问时就不走VPN了；当然这样也可以减少不必要的流量浪费。

## 查看打喷嚏ip

    C:\Users\dylanninin@gmail.com>nslookup dapenti.org
    服务器:  google-public-dns-a.google.com
    Address:  8.8.8.8

    非权威应答:
    名称:    dapenti.org
    Address:  122.226.227.53

## 查看路由命令帮助

    C:\Users\dylanninin@gmail.com>route add

    操作网络路由表。

    ROUTE [-f] [-p] [-4|-6] command [destination]
                  [MASK netmask]  [gateway] [METRIC metric]  [IF interface]

    -f           清除所有网关项的路由表。如果与某个
                 命令结合使用，在运行该命令前，
                 应清除路由表。
 
    -p           与 ADD 命令结合使用时，将路由设置为
                 在系统引导期间保持不变。默认情况下，重新启动系统时，
                 不保存路由。忽略所有其他命令，
                 这始终会影响相应的永久路由。Windows 95
                 不支持此选项。

    -4           强制使用 IPv4。

    -6           强制使用 IPv6。

    command      其中之一:
                 PRINT     打印路由
                 ADD       添加路由
                 DELETE    删除路由
                 CHANGE    修改现有路由
    destination  指定主机。
    MASK         指定下一个参数为"网络掩码"值。
    netmask      指定此路由项的子网掩码值。
                 如果未指定，其默认设置为 255.255.255.255。
    gateway      指定网关。
    interface    指定路由的接口号码。
    METRIC       指定跃点数，例如目标的成本。

    用于目标的所有符号名都可以在网络数据库文件 NETWORKS 中进行查找。用于网关的符号名称都可以在主机名称数据库文件 HOSTS 中进行查找。

    如果命令为 PRINT 或 DELETE。目标或网关可以为通配符，(通配符指定为星号"*")，否则可能会忽略网关参数。

    如果 Dest 包含一个 * 或 ?，则会将其视为 Shell 模式，并且只打印匹配目标路由。"*"匹配任意字符串，而"?"匹配任意一个字符。示例: 157.*.1、157.*、127.*、*224*。

    只有在 PRINT 命令中才允许模式匹配。
    诊断信息注释:
    无效的 MASK 产生错误，即当 (DEST & MASK) != DEST 时。
    示例: > route ADD 157.0.0.0 MASK 155.0.0.0 157.55.80.1 IF 1
             路由添加失败: 指定的掩码参数无效。
             (Destination & Mask) != Destination。

    示例:

    > route PRINT
    > route PRINT -4
    > route PRINT -6
    > route PRINT 157*          .... 只打印那些匹配  157* 的项

    > route ADD 157.0.0.0 MASK 255.0.0.0  157.55.80.1 METRIC 3 IF 2
             destination^      ^mask      ^gateway     metric^    ^
                                                         Interface^
      如果未给出 IF，它将尝试查找给定网关的最佳接口。
    > route ADD 3ffe::/32 3ffe::1

    > route CHANGE 157.0.0.0 MASK 255.0.0.0 157.55.80.5 METRIC 2 IF 2

      CHANGE 只用于修改网关和/或跃点数。

    > route DELETE 157.0.0.0
    > route DELETE 3ffe::/32

## 指定路由规则

因本机使用路由器连接，ip为192.168.1.123，子网掩码为255.255.255.0，网关为192.168.1.1； 这里指定访问打喷嚏走路由192.168.1.1；而非默认的VPN网关。

    C:\Users\dylanninin@gmail.com>route add 122.226.227.53 mask 255.255.255.255 192.168.1.1
 
    操作完成!

此时，就可以正常访问[打喷嚏](http://dapenti.org)了。

## 参考

* chnroute [chnroute](https://github.com/jimmyxu/chnroutes)
