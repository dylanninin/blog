#环境
* OS：IBM Power System 550 AIX 5.3 (64 bit)
* Storage：TS 3100/Tivoli Storage Manager Server 5.4.3.0
* Application：Oracle EBS 11.5.10.2 (64 bit)/Oracle RDBMS 9.2.0.6 (64 bit)
* Backup：RMAN (Database/Archivelog)


#简介
IBM Tivoli Storage Manager（TSM）是为解决企业级数据及系统安全而设计的备份全面解决方案。Tivoli ITSM 系统已成为当今数据备份领域的首选产品，并为包括金融、电信在内的许多大型用户和广大的中小型企业用户，解决困扰信息技术部门的备份管理问题。

为了满足企业所面临的上述问题，我们建议使用一台服务器作为 TSM 备份服务器，使用带库作为备份介质，将整个企业 IT 环境内的备份操作交由 TSM 备份服务器完成，由 TSM 备份服务器集中完成所有备份任务的调度、管理以及备份介质的集中管理。

为了解决企业所面临的数据备份问题，备份解决方案需要能够提供：

* 全自动的备份，所有的操作系统，应用，数据库的备份都可以通过设定计划自动运行；
* 集中的备份管理，集中进行整个备份系统的备份策略设置，存储池配置等工作，便于备份系统的管理和维护；
* 全面的数据备份支持，支持大量异构的系统（操作系统，数据库以及各种应用系统）和各种硬件存储设备，能够充分兼容企业内部几乎所有的软硬件平台;
* 友好的用户界面，方便使用和管理操作，提供 GUI，Web-based，以及 CLI 管理和操作平台；
* 支持 LAN、SAN、NAS 等多种存储环境；
* 其他众多先进的技术特性，如完善的介质管理技术、内置关系数据库、备份数据加密及压缩技术等。

#备份检查
以网页方式查看

检查备份路径：Server Administartion >> Object View >> Policy Domains >> Client schedules >> Query Client Events

输入查询条件，查询备份状态如下

    Operation Results
    Scheduled Start      Actual Start         Schedule Name   Node Name     Status   
    -------------------- -------------------- --------------- ------------- ---------
    12/11/12 07:00:00    12/11/12 07:11:09    DELETEEXPIRED   ORAPROD       Completed
    12/11/12 08:00:00    12/11/12 08:08:21    DELEXP_ORATEST  ORATEST       Completed                                
    12/11/12 20:00:00    12/11/12 20:00:08    ARCBAK          ORAPROD       Completed
    12/11/12 21:00:00    12/11/12 21:06:39    ARC_ORATEST     ORATEST       Completed
    12/11/12 23:00:00    12/11/12 23:01:55    FULLBAKUPORACLE ORAPROD       Failed  1                    
    12/12/12 07:00:00    12/12/12 07:04:07    DELETEEXPIRED   ORAPROD       Completed
    12/12/12 08:00:00    12/12/12 08:10:42    DELEXP_ORATEST  ORATEST       Completed

#异常信息
检查异常事件路径：Server Administartion >> Object View >> Server >> Activity Log

根据备份失败时间，输入条件；本例中备份出错为生产环境数据库全备阶段，时间为12/11/12 23:01:55左右。查询该时间段日志，错误信息如下：

    12/11/12 23:09:57     ANR1405W Scratch volume mount request denied - no scratch 
                          volume available. (SESSION: 8460)                        
    12/11/12 23:09:57     ANR0522W Transaction failed for session 8460 for node     
                          ORAPROD (TDP Oracle AIX) - no space available in storage 
                          pool ORADBPOOL and all successor pools. (SESSION: 8460)  
    12/11/12 23:09:57     ANR0403I Session 8460 ended for node ORAPROD (TDP Oracle  
                          AIX). (SESSION: 8460)                                    
    12/11/12 23:10:05     ANR0406I Session 8461 started for node ORAPROD (TDP Oracle
                          AIX) (Tcp/Ip 10.20.1.8(41271)). (SESSION: 8461)          
    12/11/12 23:10:05     ANE4994S (Session: 8461, Node: ORAPROD)  TDP Oracle AIX   
                          ANU0599 TDP for Oracle: (6475950): =>(oraprod) ANU2602E  
                          The object /adsmorc//XSDB_PROD_801788468_dcnskkhk_1_1 was
                          not found on the TSM Server (SESSION: 8461)              
    12/11/12 23:10:05     ANR0403I Session 8461 ended for node ORAPROD (TDP Oracle  
                          AIX). (SESSION: 8461)                                    
    12/11/12 23:10:06     ANR2579E Schedule FULLBAKUPORACLE in domain STANDARD for  
                          node ORAPROD failed (return code 1). (SESSION: 8447)     
    12/11/12 23:10:06     ANR0403I Session 8447 ended for node ORAPROD (AIX).       
                          (SESSION: 8447)                                          
    12/11/12 23:10:06     ANR0406I Session 8462 started for node ORAPROD (AIX)      
                          (Tcp/Ip x.x.x.x(41274)). (SESSION: 8462)               
    12/11/12 23:10:06     ANR0403I Session 8462 ended for node ORAPROD (AIX).       
                          (SESSION: 8462)                     
主要错误： no space available in storage pool ORADBPOOL and all successor pools，即带库中没有临时卷(空闲磁带)用于备份。

#异常处理
此时可进行登陆到带库管理服务器上，进行以下操作，确认备份异常，并进行相应处理。
##登陆
以应用账户ssh登陆到服务器，并运行dsmadmc命令，进入带库管理环境。

	$ set -o vi
	$ dsmadmc
	IBM Tivoli Storage Manager
	Command Line Administrative Interface - Version 5, Release 4, Level 0.0
	(c) Copyright by IBM Corporation and other(s) 1990, 2007. All Rights Reserved.

	Enter your user id:  admin
	Enter your password:  

	Session established with server TSM: AIX-RS/6000
  	Server Version 5, Release 4, Level 3.0
  	Server date/time: 12/12/12   11:33:35  Last access: 12/12/12   11:23:06

##查看日志
###q act begindate 
可查看系统日志，同web页面相应功能。

tsm: TSM>q act begindate=-1	

	Date/Time                Message                                                   
	--------------------     ----------------------------------------------------------
	...
	12/11/12   23:09:56      ANR1405W Scratch volume mount request denied - no scratch 
                          	 volume available. (SESSION: 8460)                        
	12/11/12   23:09:56      ANR1405W Scratch volume mount request denied - no scratch 
                          	 volume available. (SESSION: 8460)                        
	12/11/12   23:09:57      ANR1405W Scratch volume mount request denied - no scratch 
                          	 volume available. (SESSION: 8460)                        
	12/11/12   23:09:57      ANR0522W Transaction failed for session 8460 for node     
                          	 ORAPROD (TDP Oracle AIX) - no space available in storage 
                          	 pool ORADBPOOL and all successor pools. (SESSION: 8460)  
	12/11/12   23:09:57      ANR0403I Session 8460 ended for node ORAPROD (TDP Oracle  
                          	 AIX). (SESSION: 8460)                                      	 
	...

##查看磁带状态
###q libvol 

可查看当前在带库中注册的所有磁带的状态。

* 	Scratch表示此卷（磁带）已被回收，其内容被清除，且从存储池中注销，以备下次使用。
*	private表示此卷当前正在被使用。

tsm: TSM>q libvol

	Library Name     Volume Name     Status               Owner          Last Use      Home        Device                                                                                   																				   Element     Type  
	------------     -----------     ----------------     ----------     ---------     -------     ------
	3573LIB          A00200L3        Private                             Data          4,096       LTO   
	3573LIB          A00201L3        Private                             Data          4,098       LTO   
	3573LIB          A00202L3        Private                             Data          4,100       LTO   
	3573LIB          A00203L3        Private                             Data          4,097       LTO   
	3573LIB          A00204L3        Private                             Data          4,099       LTO   
	3573LIB          A00205L3        Private                             Data          4,105       LTO   
	3573LIB          A00206L3        Private                             Data          4,104       LTO   
 
###q vol                  
可查看当前存储池中的卷的大小及状态。

*	Full状态的卷在达到回收阙值后将会被回收。 


tsm: TSM>q vol
	
	Volume Name                  Storage         Device         Estimated       Pct      Volume 
	                             Pool Name       Class Name      Capacity      Util      Status 
	------------------------     -----------     ----------     ---------     -----     --------
	/usr/tivoli/tsm/server/-     ARCHIVEPOOL     DISK               8.0 M       0.0     On-Line 
	 bin/archive.dsm                                                                            
	/usr/tivoli/tsm/server/-     BACKUPPOOL      DISK               8.0 M       0.0     On-Line 
	 bin/backup.dsm                                                                             
	/usr/tivoli/tsm/server/-     SPACEMGPOOL     DISK               8.0 M       0.0     On-Line 
	 bin/spcmgmt.dsm                                                                            
	A00200L3                     ORADBPOOL       3573CLASS          1.5 T       5.1       Full  
	A00201L3                     ORADBPOOL       3573CLASS          1.5 T      17.8       Full  
	A00202L3                     ORADBPOOL       3573CLASS          1.5 T      15.0       Full  
	A00203L3                     ORADBPOOL       3573CLASS          1.5 T      30.4       Full  
	A00204L3                     ORADBPOOL       3573CLASS          1.5 T       3.1       Full  
	A00205L3                     ORADBPOOL       3573CLASS          1.5 T      40.2     Filling 
	A00206L3                     ORADBPOOL       3573CLASS          1.5 T      13.2       Full  


##异常确认和处理
发生如上错误的原因则是所有磁带均在存储池中处于Full的状态，导致带库中没有Scratch状态的磁带用于备份导致。

此时可执行以下命令手动删除磁带中的内容，更改其状态为Scratch。

###q con
可查看该卷中的内容，判断其中内容是否可以删除。
一般如果卷中只有少量的备份或是测试环境数据，可以考虑清空。

tsm: TSM>q con A00200L3

	Node Name           Type     Filespace      FSID     Client's Name for File                
	                             Name                    
	---------------     ----     ----------     ----     --------------------------------------
	ORATEST             Bkup     /adsmorc          2     // q4nk09k9_1_1   
                    
###delete volume volumename DISCARDDATA=YES
删除一些测试环境备份卷中数据，执行后该卷将从存储池中注销，恢复状态为Scratch。

该环境汇中标为TEST的即为测试环境备份卷。

删除测试环境卷数据

tsm: TSM>delete volume A00200L3 DISCARDDATA=YES

	ANR2221W This command will result in the deletion of all inventory references to the data on volume A00200L3, thereby rendering the data
	unrecoverable.
	
	Do you wish to proceed? (Yes (Y)/No (N)) Y
	ANR2222I Discard Data process started for volume A00200L3 (process ID 40).
	ANS8003I Process number 40 started.

查看删除后卷状态

tsm: TSM>q libvol


	Library Name     Volume Name     Status               Owner          Last Use      Home        Device
	                                                                                   Element     Type  
	------------     -----------     ----------------     ----------     ---------     -------     ------
	3573LIB          A00200L3        Scratch                                           4,096       LTO   
	3573LIB          A00201L3        Private                             Data          4,098       LTO   
	3573LIB          A00202L3        Private                             Data          4,100       LTO   
	3573LIB          A00203L3        Private                             Data          4,097       LTO   
	3573LIB          A00204L3        Private                             Data          4,099       LTO   
	3573LIB          A00205L3        Private                             Data          4,105       LTO   
	3573LIB          A00206L3        Private                             Data          4,104       LTO  

适当删除一些测试环境的备份数据后，有足够的空间则可以正常完成备份任务。

#参考文档
* IBM：IBM TSM backup case
* IBM：IBM Tivoli Storage Management Concepts