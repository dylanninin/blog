---
layout: post
title: Network Configure on Linux
category : Linux
tags : [Linux, Network]
---

##Configuration Files

Before delving into the interface configuration files, let us first itemize the primary configuration files used in network configuration. Understanding the role these files play in setting up the network stack can be helpful when customizing a Red Hat Enterprise Linux system.

The primary network configuration files are as follows:

 * `/etc/hosts`
The main purpose of this file is to resolve hostnames that cannot be resolved any other way. It can also be used to resolve hostnames on small networks with no DNS server. Regardless of the type of network the computer is on, this file should contain a line specifying the IP address of the loopback device (127.0.0.1) as localhost.localdomain. For more information, refer to the hosts(5) manual page.
 *  `/etc/resolv.conf`
This file specifies the IP addresses of DNS servers and the search domain. Unless configured to do otherwise, the network initialization scripts populate this file. For more information about this file, refer to the resolv.conf(5) manual page.
 *  `/etc/sysconfig/network`
This file specifies routing and host information for all network interfaces. It is used to contain directives which are to have global effect and not to be interface specific. For more information about this file and the directives it accepts, refer to Section D.1.13, “/etc/sysconfig/network”.
 * `/etc/sysconfig/network-scripts/ifcfg-interface-name`
For each network interface, there is a corresponding interface configuration script. Each of these files provide information specific to a particular network interface. Refer to Section 9.2, “Interface Configuration Files” for more information on this type of file and the directives it accepts.

##Interface Configuration Files

Interface configuration files control the software interfaces for individual network devices. As the system boots, it uses these files to determine what interfaces to bring up and how to configure them. These files are usually named ifcfg-name, where name refers to the name of the device that the configuration file controls.

##Channel Bonding Interfaces

Red Hat Enterprise Linux allows administrators to bind multiple network interfaces together into a single channel using the bonding kernel module and a special network interface called a channel bonding interface. Channel bonding enables two or more network interfaces to act as one, simultaneously increasing the bandwidth and providing redundancy.

To create a channel bonding interface, create a file in the `/etc/sysconfig/network-scripts/` directory called ifcfg-bondN, replacing N with the number for the interface, such as 0.

The contents of the file can be identical to whatever type of interface is getting bonded, such as an Ethernet interface. The only difference is that the DEVICE directive is bondN, replacing N with the number for the interface.
The following is a sample channel bonding configuration file:

Example 9.1. Sample ifcfg-bond0 interface configuration file

	DEVICE=bond0
	IPADDR=192.168.1.1
	NETMASK=255.255.255.0
	ONBOOT=yes
	BOOTPROTO=none
	USERCTL=no
	BONDING_OPTS="bonding parameters separated by spaces"

After the channel bonding interface is created, the network interfaces to be bound together must be configured by adding the MASTER and SLAVE directives to their configuration files. The configuration files for each of the channel-bonded interfaces can be nearly identical.

For example, if two Ethernet interfaces are being channel bonded, both eth0 and eth1 may look like the following example:

	DEVICE=ethN
	BOOTPROTO=none
	ONBOOT=yes
	MASTER=bond0
	SLAVE=yes
	USERCTL=no

In this example, replace N with the numerical value for the interface.
For a channel bonding interface to be valid, the kernel module must be loaded. To ensure that the module is loaded when the channel bonding interface is brought up, create a new file as root named bonding.conf in the `/etc/modprobe.d/` directory. Note that you can name this file anything you like as long as it ends with a .conf extension. Insert the following line in this new file:

	alias bondN bonding

Replace N with the interface number, such as 0. For each configured channel bonding interface, there must be a corresponding entry in your new /`etc/modprobe.d/bonding.conf` file.

##Reference

 * [REL Deployment Guide](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html-single/Deployment_Guide/index.html#ch-Network_Interfaces)