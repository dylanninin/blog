## mount iscsi storage on aix

1.os and iscsi package

	# uname -a
	AIX erp 3 5 00066345D600	

	# lslpp -L | grep iscsi
	  devices.common.IBM.iscsi.rte
	  devices.iscsi.disk.rte    5.3.0.60    C     F    iSCSI Disk Software 
	  devices.iscsi.tape.rte    5.3.0.30    C     F    iSCSI Tape Software 
	  devices.iscsi_sw.rte      5.3.0.64    C     F    iSCSI Software Device Driver

2.iscsi targets configure

	# vi /etc/iscsi/targets
	"/etc/iscsi/targets" 104 lines, 3562 characters 
	# @(#)25        1.2  src/bos/usr/lib/methods/cfgiscsi/targets.sh, sysxiscsi, bos53A, a2004_37B1 8/30/04 13:58:05
	# IBM_PROLOG_BEGIN_TAG
	# This is an automatically generated prolog.
	#
	# bos53A src/bos/usr/lib/methods/cfgiscsi/targets.sh 1.2
	#
	# Licensed Materials - Property of IBM
	#
	# (C) COPYRIGHT International Business Machines Corp. 2003,2004
	# All Rights Reserved
	#
	# US Government Users Restricted Rights - Use, duplication or
	# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
	#
	# IBM_PROLOG_END_TAG
	# iSCSI targets file
	#
	# Comments may be used in the file, the comment character is '#', 0x23.
	# Anything from a comment char to the end of the line is ignored.
	#
	# Blank lines are ignored.
	#
	# The format for a target line is defined according to the Augmented BNF
	# syntax as # described in rfc2234.
	#
	# The format for the IPv4Address is taken from rfc2373.
	#
	# The line continuation character '\' (i.e., back-slash) can be used to make
	# each TargetLine easier to read. To ensure no parsing errors, the '\'
	# character must be the last character and must be preceeded by white space.
	#
	# ---
	#
	# comment        = %x23 *CHARS LF
	#                  ; #
	#
	# TargetLine     = *WSP HostNameOrAddr 1*WSP PortNumber 1*WSP ISCSIName *WSP LF
	#       or
	"/etc/iscsi/targets" 104 lines, 3562 characters
	#       Assume the target is at address 10.2.1.105
	#       the valid port is 3260
	#       the name of the target is iqn.com.ibm-K167-42.fc1a
	#       the CHAP secret is "This is my password."
	# The target line would look like:
	# 10.2.1.105 3260 iqn.com.ibm-K167-42.fc1a "This is my password."
	#
	# EXAMPLE 3: iSCSI Target with CHAP(MD5) authentication and line continuation
	#       Assume the target is at address 10.2.1.106
	#       the valid port is 3260
	#       the name of the target is iqn.2003-01.com.ibm:00.fcd0ab21.shark128
	#       the CHAP secret is "123ismysecretpassword.fc1b"
	# The target line would look like:
	# 10.2.1.106 3260 iqn.2003-01.com.ibm:00.fcd0ab21.shark128 \
	#               "123ismysecretpassword.fc1b"
	#
	
	172.29.88.61 3260 iqn.2000-01.com.synology:TheMain-2nd.erp

3.cfgmgr discover hardware

	# cfgmgr -v -l iscsi0
	----------------
	attempting to configure device 'iscsi0'
	Time: 0 LEDS: 0x25b0
	invoking /usr/lib/methods/cfgiscsi -l iscsi0 
	Number of running methods: 1
	----------------
	Completed method for: iscsi0, Elapsed time = 1
	return code = 0
	****************** stdout ***********
	hdisk10 
	****************** no stderr ***********
	----------------
	Time: 1 LEDS: 0x539
	Number of running methods: 0
	----------------
	attempting to configure device 'hdisk10'
	Time: 1 LEDS: 0x25f3
	invoking /usr/lib/methods/cfgscsidisk -l hdisk10 
	Number of running methods: 1
	----------------
	Completed method for: hdisk10, Elapsed time = 4
	return code = 0
	****************** no stdout ***********
	****************** no stderr ***********
	----------------
	Time: 5 LEDS: 0x539
	Number of running methods: 0
	----------------
	calling savebase
	return code = 0
	****************** no stdout ***********
	****************** no stderr ***********
	Configuration time: 5 seconds

	# lspv
	hdisk0          00066345812c3186                    rootvg          active
	hdisk1          000663453bb98660                    rootvg          active
	hdisk2          00066345863e157b                    testvg          active
	hdisk3          000664cd863d5728                    prodvg          
	hdisk6          00066345a372bab2                    testvg1         active
	hdisk7          000664cd9ac59525                    None            
	hdisk8          00066345e6513be8                    testvg          active
	hdisk9          none                                None            
	hdisk10         none                    			None            

	# lsattr -El hdisk10          
	clr_q         no                                       Device CLEARS its Queue on error True
	host_addr     172.29.88.61                             Hostname or IP Address           False
	location                                               Location Label                   True
	lun_id        0x0                                      Logical Unit Number ID           False
	max_transfer  0x40000                                  Maximum TRANSFER Size            True
	port_num      0xcbc                                    PORT Number                      False
	pvid          none                                     Physical volume identifier       False
	q_err         yes                                      Use QERR bit                     True
	q_type        simple                                   Queuing TYPE                     True
	queue_depth   1                                        Queue DEPTH                      True
	reassign_to   120                                      REASSIGN time out value          True
	rw_timeout    30                                       READ/WRITE time out value        True
	start_timeout 60                                       START unit time out value        True
	target_name   iqn.2000-01.com.synology:themain-2nd.erp Target NAME                      False

4.mkvg

	#chdev -l hdisk10 -a pv=yes
	hdisk10 changed

	# lsattr -El hdisk10
	clr_q         no                                       Device CLEARS its Queue on error True
	host_addr     172.29.88.61                             Hostname or IP Address           False
	location                                               Location Label                   True
	lun_id        0x0                                      Logical Unit Number ID           False
	max_transfer  0x40000                                  Maximum TRANSFER Size            True
	port_num      0xcbc                                    PORT Number                      False
	pvid          00066345e9028f430000000000000000         Physical volume identifier       False
	q_err         yes                                      Use QERR bit                     True
	q_type        simple                                   Queuing TYPE                     True
	queue_depth   1                                        Queue DEPTH                      True
	reassign_to   120                                      REASSIGN time out value          True
	rw_timeout    30                                       READ/WRITE time out value        True
	start_timeout 60                                       START unit time out value        True
	target_name   iqn.2000-01.com.synology:themain-2nd.erp Target NAME                      False

	# lquerypv -h /dev/hdisk10
	00000000   C9C2D4C1 00000000 00000000 00000000  |................|
	00000010   00000000 00000000 00000000 00000000  |................|
	00000020   00000000 00000000 00000000 00000000  |................|
	00000030   00000000 00000000 00000000 00000000  |................|
	00000040   00000000 00000000 00000000 00000000  |................|
	00000050   00000000 00000000 00000000 00000000  |................|
	00000060   00000000 00000000 00000000 00000000  |................|
	00000070   00000000 00000000 00000000 00000000  |................|
	00000080   00066345 E9028F43 00000000 00000000  |..cE...C........|
	00000090   00000000 00000000 00000000 00000000  |................|
	000000A0   00000000 00000000 00000000 00000000  |................|
	000000B0   00000000 00000000 00000000 00000000  |................|
	000000C0   00000000 00000000 00000000 00000000  |................|
	000000D0   00000000 00000000 00000000 00000000  |................|
	000000E0   00000000 00000000 00000000 00000000  |................|
	000000F0   00000000 00000000 00000000 00000000  |................|

	# mkvg -y datavg hdisk10
	0516-1184 mkvg: IO failure on hdisk10.
	0516-862 mkvg: Unable to create volume group.

	# lsdev -l hdisk10                             
	hdisk10 Available  Other iSCSI Disk Drive

	# errpt -a | more
	---------------------------------------------------------------------------
	LABEL:          SC_DISK_ERR2
	IDENTIFIER:     B6267342
	
	Date/Time:       Wed May 29 14:24:25 BEIST 2013
	Sequence Number: 154487
	Machine Id:      00066345D600
	Node Id:         erp
	Class:           H
	Type:            PERM
	Resource Name:   hdisk10         
	Resource Class:  disk
	Resource Type:   osdisk
	Location:        
	VPD:             
	        Manufacturer................SYNOLOGY
	        Machine Type and Model......iSCSI Storage
	        ROS Level and ID............332E3100
	        Device Specific.(Z0)........000005021FB00032
	
	Description
	DISK OPERATION ERROR
	
	Probable Causes
	DASD DEVICE
	
	Failure Causes
	DISK DRIVE
	DISK DRIVE ELECTRONICS
	
	        Recommended Actions
	        PERFORM PROBLEM DETERMINATION PROCEDURES
	
	Detail Data
	PATH ID
	           0
	SENSE DATA
	0A00 2E00 0000 0047 0000 0100 0000 0000 0000 0000 0000 0000 0102 0000 7000 0500 
	0000 0000 0000 0000 2000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 
	0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 
	0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 
	0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 
	0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000 
	0000 0000 0000 0000 0000 0000 1C00 0000 0004 0000 0000 0000 0000 0000 0000 0000 
	0000 0029 0017 
	---------------------------------------------------------------------------

5.mkfs

	# mkfs -o log=INLINE -Vjfs2 /dev/hdisk10
	mkfs: destroy /dev/hdisk10 (yes)? yes
	logform: Format inline log for  <y>?y
	File system created successfully.
	1072660308 kilobytes total disk space.
	Device /dev/hdisk10:
	  Standard empty filesystem
	  Size:           2145320616 512-byte (DEVBLKSIZE) blocks

6.mount/umount

	# mount -o log=NULL /dev/hdisk10 /data
	mount: 0506-323 Cannot get information about log device NULL.
	# mount -V jfs2 -o log=INLINE /dev/hdisk10 /data

	# umount /data

	# rmdev -Rdl hdisk10
	hdisk10 deleted

	# cfgmgr -l iscsi0
	# lspv
	hdisk0          00066345812c3186                    rootvg          active
	hdisk1          000663453bb98660                    rootvg          active
	hdisk2          00066345863e157b                    testvg          active
	hdisk3          000664cd863d5728                    prodvg          
	hdisk6          00066345a372bab2                    testvg1         active
	hdisk7          000664cd9ac59525                    None            
	hdisk8          00066345e6513be8                    testvg          active
	hdisk9          none                                None            
	hdisk10         00066345eef33fa1                    None        
    
	# mount -V jfs2 -o log=INLINE /dev/hdisk10 /data

## Reference

* [AIX 5.3/6.1 ISCSI howto](http://dawangliang.blog.163.com/blog/static/1879031682011543446756/)
* [AIX 5.3 iSCSI softwre initiator](http://publib.boulder.ibm.com/infocenter/pseries/v5r3/index.jsp?topic=/com.ibm.aix.commadmn/doc/commadmndita/iscsi_config.htm)
* [AIX 5.3 iSCSI target file reference](http://publib.boulder.ibm.com/infocenter/pseries/v5r3/index.jsp?topic=/com.ibm.aix.commadmn/doc/commadmndita/iscsi_config.htm)
