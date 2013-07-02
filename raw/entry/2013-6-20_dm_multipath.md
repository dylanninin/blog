#DM Multipath介绍

##1.1概念

设备映射器多路径（DM-Multipath）可让您将服务器节点和存储阵列间的多个 I/O 路径配置为一个单一设备。这些 I/O 路径是可包含独立电缆、交换机以及控制器的物理 SAN 连接。多路径集合了 I/O 路径，并生成由这些整合路径组成的新设备。

##1.2概述

可使用 DM-Multipath 提供：

* 冗余
DM-Multipath 可在主动/被动配置中提供出错冗余。在主动/被动配置中，只有一半的路径在每次 I/O 时都使用。如果 I/O 路径的任意元素（电缆、交换机或者控制器）出现故障，就会将 DM-Multipath 切换到备用路径。

* 改进的性能
可将 DM-Multipath 配置为主动/主动模式，其中将 I/O 以轮叫调度算法方式分布到所有路径中。在有些配置中，DM-Multipath 可在 I/O 路径中检测负载并动态重新平衡负载。

“带一个 RAID 设备的主动/被动多路径配置” 演示在服务器和 RAID 设备之间有两个 I/O 路径的主动/被动配置。这里服务器中有两个 HBA，两个 SAN 交换机以及两个 RAID 控制器。

!![multipath-server](images/multipath-server1.png)

##1.3存储阵列支持

默认情况下，DM-Multipath 支持大多数常用的、支持 DM-Multipath 的存储阵列。您可在 multipath.conf.defaults 文件中找到这些支持的设备。如果您的存储阵列支持 DM-Multipath 且未在这个文件中默认设置，可能需要将其添加到 DM-Multipath 配置文件 multipath.conf 中。

##1.4组件。


	----------------------  ------------------------------------------------
	组件	 					描述	
	---------------------- -------------------------------------------------
	dm-multipath 内核模块	 为路径和路径组群重新指定 I/O 并支持出错冗余。
	mpathconf 程序	 	 配置并启用设备映射器多路径
	multipath 命令		 列出并配置 multipath 设备。通常使用 /etc/rc.sysinit 启动，还可以在添加块设备时使用 udev 程序启动。
	multipathd 守护进程	   监视器路径，如果路径故障并返回，它可能会启动路径组群切换。可为多路径设备提供互动修改。对 /etc/multipath.conf 文件的任何修改都必须启动它。
	kpartx 命令	 		 为设备中的分区生成设备映射器设备。这个命令对带 DM-MP 的 DOS 分区是很必要的。kpartx 在其自身软件包中就存在，但 device-mapper-multipath 软件包要依赖它

##1.5设置概述

DM-Multipath 包含适用于常见多路径配置已编译的默认设置。安装 DM-multipath 通常很简单。

以下是为您的系统配置 DM-multipath 的基本步骤：

* 安装 device-mapper-multipath rpm。
* 使用 mpathconf 命令创建配置文件并启用多路径。如果您不需要编辑该配置文件，您还可以使用这个命令启动多路径守护进程。
* 如需要，请编辑 multipath.conf 配置文件，修改默认值并保存更新的文件：
* 启动多路径守护进程


#Reference

* [Configuration and Administration zh ](https://access.redhat.com/site/documentation/zh-CN/Red_Hat_Enterprise_Linux/6/html-single/DM_Multipath/)
* [Configuration and Administration en ](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html-single/DM_Multipath/index.html)
