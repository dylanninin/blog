---
layout: post
title: DM Multipath Configuration on Linux
category : Linux
tags : [Linux, Storage]
---

## unique scsi identifiers

list all scsi devices

	[root@devdb ~]# cat /proc/partitions 
	major minor  #blocks  name

	   8        0  291991552 sda
	   8        1     204800 sda1
	   8        2     512000 sda2
	   8        3   20971520 sda3
	   8        4  270301184 sda4
	   8       16    5242880 sdb
	   8       64  104857600 sde
	   8       32  104857600 sdc
	   8       80  104857600 sdf
	   8      112  104857600 sdh
	   8       48  104857600 sdd
	   8      128  157286400 sdi
	   8      144  209715200 sdj
	   8      160  419430400 sdk
	   8       96  104857600 sdg
	   8      176    5242880 sdl
	   8      208  104857600 sdn
	   8      224  104857600 sdo
	   8      240  104857600 sdp
	   8      192  104857600 sdm
	  65        0  104857600 sdq
	  65       16  104857600 sdr
	  65       32  157286400 sds
	  65       48  209715200 sdt
	  65       64  419430400 sdu
	 252        0   33554432 dm-0
	 252        1    5242880 dm-1
	 252        2  104857600 dm-2
	 252        3  104857600 dm-3
	 252        4  104857600 dm-4
	 252        5  104857600 dm-5
	 252        6  104857600 dm-6
	 252        7  157286400 dm-7
	 252        8  209715200 dm-8
	 252        9  419430400 dm-9
	 252       10  104857600 dm-10
	 252       11          1 dm-11
	 252       12  209712447 dm-12
	 252       13  122880000 dm-13

obtain clusterware device unique scsi identifiers

	[root@devdb ~]# for i in `ls /dev/sd[a-z]` ; do   echo $i "`/sbin/scsi_id i --whitelisted --device=$i`"; done | sort -k2
	/dev/sdc 36005076802810b121800000000000005
	/dev/sdm 36005076802810b121800000000000005
	/dev/sdd 36005076802810b121800000000000006
	/dev/sdn 36005076802810b121800000000000006
	/dev/sde 36005076802810b121800000000000007
	/dev/sdo 36005076802810b121800000000000007
	/dev/sdf 36005076802810b121800000000000008
	/dev/sdp 36005076802810b121800000000000008
	/dev/sdg 36005076802810b121800000000000009
	/dev/sdq 36005076802810b121800000000000009
	/dev/sdh 36005076802810b12180000000000000a
	/dev/sdr 36005076802810b12180000000000000a
	/dev/sdb 36005076802810b12180000000000000b
	/dev/sdl 36005076802810b12180000000000000b
	/dev/sdi 36005076802810b12180000000000000c
	/dev/sds 36005076802810b12180000000000000c
	/dev/sdj 36005076802810b12180000000000000e
	/dev/sdt 36005076802810b12180000000000000e
	/dev/sdk 36005076802810b12180000000000000f
	/dev/sdu 36005076802810b12180000000000000f
	/dev/sda 3600605b0061b8b301944b4a80d86a2f9

## configure multipathing

enable the multipath configuration file and starts the multipathd daemon

	[root@devdb ~]# mpathconf --enable --with_multipathd y

	[root@devdb ~]# tree -f /etc/multipath*
	/etc/multipath.conf
	/etc/multipath
	├── /etc/multipath/bindings  
	└── /etc/multipath/wwids

multipath.conf 

	[root@devdb ~]# cat /etc/multipath.conf 
	# This is a basic configuration file with some examples, for device mapper
	# multipath.
	# For a complete list of the default configuration values, see
	# /usr/share/doc/device-mapper-multipath-0.4.9/multipath.conf.defaults
	# For a list of configuration options with descriptions, see
	# /usr/share/doc/device-mapper-multipath-0.4.9/multipath.conf.annotated
	#
	# REMEMBER: After updating multipath.conf, you must run
	#
	# service multipathd reload
	#
	# for the changes to take effect in multipathd
	... ...
	blacklist {
		wwid  3600605b0061b8b301944b4a80d86a2f9
	}

wwids

	[root@devdb ~]# cat /etc/multipath/wwids 
	# Multipath wwids, Version : 1.0
	# NOTE: This file is automatically maintained by multipath and multipathd.
	# You should not need to edit this file in normal circumstances.
	#
	# Valid WWIDs:
	/36005076802810b121800000000000005/

bindings

	[root@devdb ~]# cat /etc/multipath/bindings 
	# Multipath bindings, Version : 1.0
	# NOTE: this file is automatically maintained by the multipath program.
	# You should not need to edit this file in normal circumstances.
	#
	# Format:
	# alias wwid
	#
	mpatha 3600605b0061b8b301944b4a80d86a2f9
	mpathb SIBM     2145           0200a042c486XX25
	mpathc 36005076802810b121800000000000005

multipath -v3

	[root@devdb ~]# multipath -v3
	... ...
	===== paths list =====
	uuid                              hcil    dev dev_t pri dm_st chk_st vend/prod
	3600605b0061b8b301944b4a80d86a2f9 0:2:0:0 sda 8:0   1   undef ready  IBM,Serve
	36005076802810b121800000000000005 3:0:0:0 sdb 8:16  50  undef ready  IBM,2145 
	36005076802810b121800000000000005 4:0:0:0 sdc 8:32  10  undef ready  IBM,2145 
	... ...

## alias

alias settings

	[root@devdb ~] vim /etc/multipath.conf
	... ...
	defaults {
		user_friendly_names yes
	}
	... ...
	multipaths {
		multipath {
			wwid			36005076802810b121800000000000005
			alias			data
		}
	}
	... ...

stop device mapping

	[root@devdb ~] service multipathd stop

flush device mappings

	[root@devdb ~] multipath -F

start device mapping

	[root@devdb ~] service multipathd start
	
show multipath topology

	[root@devdb ~]# multipath -ll
	data (36005076802810b121800000000000005) dm-5 IBM,2145
	size=400G features='0' hwhandler='0' wp=rw
	|-+- policy='round-robin 0' prio=50 status=active
	| `- 4:0:0:9 sdd 65:64 active ready running
	`-+- policy='round-robin 0' prio=10 status=enabled
	  `- 3:0:0:9 sdc 8:160 active ready running

show created devices

	[root@devdb ~]# dmsetup ls | sort
	data	(252:9)
	erpdb_asm_crsdg	(252:1)
	erpdb_asm_dg_1	(252:3)
	erpdb_asm_dg_2	(252:6)
	erpdb_asm_dg_3	(252:2)
	erpdb_asm_dg_4	(252:4)
	erpdb_asm_dg_5	(252:10)
	erpdb_asm_fradg	(252:5)
	erpdb_fs_arch_db1	(252:7)
	patch	(252:8)
	patchp1	(252:11)
	patchp5	(252:12)
	vg_devdb-LV_DB	(252:13)
	vg_devdb-LV_SWAP	(252:0)
	
## adminstartion commands

mpathconf

	[root@devdb ~]# mpathconf --help
	usage: /sbin/mpathconf <command>

	Commands:
	Enable: --enable 
	Disable: --disable
	Set user_friendly_names (Default n): --user_friendly_names <y|n>
	Set find_multipaths (Default n): --find_multipaths <y|n>
	Load the dm-multipath modules on enable (Default y): --with_module <y|n>
	start/stop/reload multipathd (Default n): --with_multipathd <y|n>
	chkconfig on/off multipathd (Default y): --with_chkconfig <y|n>

multipath

	[root@dev1 etc]# multipath -l
	multipath-tools v0.4.9 (04/04, 2009)
	Usage:
	  multipath [-c] [-d] [-r] [-v lvl] [-p pol] [-b fil] [-q] [dev]
	  multipath -l|-ll|-f [-v lvl] [-b fil] [dev]
	  multipath -F [-v lvl]
	  multipath -h
	
	Where:
	  -h      print this usage text
	  -l      show multipath topology (sysfs and DM info)
	  -ll     show multipath topology (maximum info)
	  -f      flush a multipath device map
	  -F      flush all multipath device maps
	  -c      check if a device should be a path in a multipath device
	  -q      allow queue_if_no_path when multipathd is not running
	  -d      dry run, do not create or update devmaps
	  -r      force devmap reload
	  -p      policy failover|multibus|group_by_serial|group_by_prio
	  -b fil  bindings file location
	  -p pol  force all maps to specified path grouping policy :
	          . failover            one path per priority group
	          . multibus            all paths in one priority group
	          . group_by_serial     one priority group per serial
	          . group_by_prio       one priority group per priority lvl
	          . group_by_node_name  one priority group per target node
	  -v lvl  verbosity level
	          . 0 no output
	          . 1 print created devmap names only
	          . 2 default verbosity
	          . 3 print debug information
	  dev     action limited to:
	          . multipath named 'dev' (ex: mpath0) or
	          . multipath whose wwid is 'dev' (ex: 60051..)
	          . multipath including the path named 'dev' (ex: /dev/sda)
	          . multipath including the path with maj:min 'dev' (ex: 8:0)

multipathd

	[root@devdb ~]# multipathd -k
	multipathd> help
	multipath-tools v0.4.9 (04/04, 2009)
	CLI commands reference:
	 list|show paths
	 list|show paths format $format
	 list|show status
	 list|show daemon
	 list|show maps|multipaths
	 list|show maps|multipaths status
	 list|show maps|multipaths stats
	 list|show maps|multipaths format $format
	 list|show maps|multipaths topology
	 list|show topology
	 list|show map|multipath $map topology
	 list|show config
	 list|show blacklist
	 list|show devices
	 list|show wildcards
	 add path $path
	 remove|del path $path
	 add map|multipath $map
	 remove|del map|multipath $map
	 switch|switchgroup map|multipath $map group $group
	 reconfigure
	 suspend map|multipath $map
	 resume map|multipath $map
	 resize map|multipath $map
	 disablequeueing map|multipath $map
	 restorequeueing map|multipath $map
	 disablequeueing maps|multipaths
	 restorequeueing maps|multipaths
	 reinstate path $path
	 fail path $path
	 paths count
	 forcequeueing daemon
	 restorequeueing daemon
	 quit|exit
	 map|multipath $map getprstatus
	 map|multipath $map setprstatus
	 map|multipath $map unsetprstatus

## full configure

	[root@devdb ~]# grep -v '^#' /etc/multipath.conf
	defaults {
		polling_interval 	30
		path_selector		"round-robin 0"
		path_grouping_policy	multibus
		path_checker		readsector0
		rr_min_io		100
		max_fds			8192
		rr_weight		priorities
		failback		immediate
		no_path_retry		fail
		user_friendly_names	yes
	}
	blacklist {
			wwid 3600605b0061b8b301944b4a80d86a2f9
		devnode "^(ram|raw|loop|fd|md|dm-|sr|scd|st)[0-9]*"
		devnode "^hd[a-z]"
	}
	devices {
		device {
			vendor "IBM"
			product "2145"
			path_grouping_policy group_by_prio
			getuid_callout "/lib/udev/scsi_id --whitelisted --device=/dev/%n"
			path_selector "round-robin 0"
			path_checker tur
			features "1 queue_if_no_path"
			hardware_handler "0"
			prio alua
			failback immediate
			rr_weight uniform
			rr_min_io 1000
			rr_min_io_rq 1
		}
	}

	multipaths {
		multipath {
			wwid			36005076802810b121800000000000005
			alias			erpdb_asm_dg_1
		}
		multipath {
			wwid			36005076802810b121800000000000006
			alias			erpdb_asm_dg_2
		}
		multipath {
			wwid			36005076802810b121800000000000007
			alias			erpdb_asm_dg_3
		}
		multipath {
			wwid			36005076802810b121800000000000008
			alias			erpdb_asm_dg_4
		}
		multipath {
			wwid			36005076802810b121800000000000009
			alias			erpdb_asm_dg_5
		}
		multipath {
			wwid			36005076802810b12180000000000000a
			alias			erpdb_asm_fradg
		}
		multipath {
			wwid			36005076802810b12180000000000000b
			alias			erpdb_asm_crsdg
		}
		multipath {
			wwid			36005076802810b12180000000000000c
			alias			erpdb_fs_arch_db1
		}
		multipath {
			wwid			36005076802810b12180000000000000e
			alias			patch
		}
		multipath {
			wwid			36005076802810b12180000000000000f
			alias			data
		}
	
