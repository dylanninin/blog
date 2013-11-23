---
layout: post
title: Oracle Database RAC2Single Recovery 
category : Oracle
tags : [Oracle, Database, DBA]
---

###环境介绍

11gR2 RAC（原系统）

                           db1        db2
    public ip         192.168.1.9      192.168.1.10
    vip               192.168.1.11     192.168.1.12
    private ip        192.168.1.9      192.168.1.10
    scan ip                   192.168.1.13

target （目标系统）

    public ip            192.168.1.5

主要步骤（除去post步骤，耗时120~150min，可以多分配几个channel，提高处理速度）

    1）rac backup：原系统RMAN备份，耗时 30min
    
    2）copy backup set to target system(耗时30min) or shared by nfs(耗时5min，可提前准备好)
    
    3）rac2single recovery：RAC恢复到单节点数据库(耗时 80min，可以通过多分配通道提速)
                                     
        prepare：--耗时5min
            path:backup,datafile
            env:ORACLE_SID
            pfile: --耗时5min
                SID
                non-rac
                log_file_name_convert
                db_file_name_convert
                service_names
                other:*_dest*
        recovery：--耗时 70min
            set dbid;
            nomount, restore controlfile;
            mount;
            setnew name,restore database,switch datafile all,recover database; --耗时60min ~ 70min
            restore archivelogs; --不需要此步骤
            recreate controlfile; --不需要此步骤
            open database resetlogs; --耗时5min
    
    4）post：监听配置，spfile启动，全备
        listener configuration
        restart target system
        rman full backup targets system

## 11gR2 RMAN Backup
    
rman backup
    
    [oracle@db1 backup]$ rman target/

    Recovery Manager: Release 11.2.0.3.0 - Production on Thu Oct 17 10:17:42 2013

    Copyright (c) 1982, 2011, Oracle and/or its affiliates.  All rights reserved.

    connected to target database: PROD (DBID=240240185)

    RMAN> show all;

    using target database control file instead of recovery catalog
    RMAN configuration parameters for database with db_unique_name PROD are:
    CONFIGURE RETENTION POLICY TO REDUNDANCY 7;
    CONFIGURE BACKUP OPTIMIZATION OFF; # default
    CONFIGURE DEFAULT DEVICE TYPE TO DISK; # default
    CONFIGURE CONTROLFILE AUTOBACKUP ON;
    CONFIGURE CONTROLFILE AUTOBACKUP FORMAT FOR DEVICE TYPE DISK TO '/data/controlfile/ctl_file_%F';
    CONFIGURE DEVICE TYPE DISK PARALLELISM 1 BACKUP TYPE TO BACKUPSET; # default
    CONFIGURE DATAFILE BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
    CONFIGURE ARCHIVELOG BACKUP COPIES FOR DEVICE TYPE DISK TO 1; # default
    CONFIGURE CHANNEL DEVICE TYPE DISK MAXPIECESIZE 10240 M;
    CONFIGURE MAXSETSIZE TO UNLIMITED; # default
    CONFIGURE ENCRYPTION FOR DATABASE OFF; # default
    CONFIGURE ENCRYPTION ALGORITHM 'AES128'; # default
    CONFIGURE COMPRESSION ALGORITHM 'BASIC' AS OF RELEASE 'DEFAULT' OPTIMIZE FOR LOAD TRUE ; # default
    CONFIGURE ARCHIVELOG DELETION POLICY TO NONE; # default
    CONFIGURE SNAPSHOT CONTROLFILE NAME TO '/u1/app/oracle/product/11.2.0/db1/dbs/snapcf_PROD1.f'; # default

    RMAN> run
    {
    ###backup database###
    backup  incremental level=0 tag='db_bak_lev0'        
            format='/data/backup/db_bak_lev0_%t_%p_%s'
            database;
    ###switch out the current logfile###
    sql 'alter system archive log thread 1 current';
    sql 'alter system archive log thread 2 current';
    ###backup archived log######
    backup archivelog all tag='arc_bak'
           format='/data/backup/archive_log_%t_%p_%s'
           skip inaccessible 
           filesperset 4
           not  backed up 1 times
           delete  input;
    ###backup current controlfile that contains the records for the backups just made###
    backup current controlfile tag='bak_ctlfile' format='/data/backup/ctl_file_%t_%p_%s';
    crosscheck backup;
    delete force noprompt expired backup;
    delete force noprompt obsolete;
    }

    ... ...


    RMAN> list backup of controlfile;


    List of Backup Sets
    ===================


    BS Key  Type LV Size       Device Type Elapsed Time Completion Time
    ------- ---- -- ---------- ----------- ------------ ---------------
    268     Full    18.42M     DISK        00:00:00     17-OCT-13      
            BP Key: 308   Status: AVAILABLE  Compressed: NO  Tag: TAG20131017T104019
            Piece Name: /data/controlfile/ctl_file_c-240240185-20131017-00
      Control File Included: Ckp SCN: 101311620    Ckp time: 17-OCT-13

    BS Key  Type LV Size       Device Type Elapsed Time Completion Time
    ------- ---- -- ---------- ----------- ------------ ---------------
    273     Full    18.39M     DISK        00:00:01     17-OCT-13      
            BP Key: 313   Status: AVAILABLE  Compressed: NO  Tag: BAK_CTLFILE
            Piece Name: /data/backup/ctl_file_829046450_1_273
      Control File Included: Ckp SCN: 101313008    Ckp time: 17-OCT-13

    BS Key  Type LV Size       Device Type Elapsed Time Completion Time
    ------- ---- -- ---------- ----------- ------------ ---------------
    274     Full    18.42M     DISK        00:00:00     17-OCT-13      
            BP Key: 314   Status: AVAILABLE  Compressed: NO  Tag: TAG20131017T104052
            Piece Name: /data/controlfile/ctl_file_c-240240185-20131017-01
      Control File Included: Ckp SCN: 101313063    Ckp time: 17-OCT-13

## copy backup set

###use scp

copy backup set using scp (estimated time: 0.55h (214GB * 1024MB / 110MB / 3600 ))

file system

    [root@target ~]# df -h
    Filesystem            Size  Used Avail Use% Mounted on
    /dev/mapper/vg_erptest1-LV_ROOT
                           50G   16G   31G  35% /
    tmpfs                  32G  144K   32G   1% /dev/shm
    /dev/mapper/vg_erptest1-LV_APPS
                           99G  188M   94G   1% /apps
    /dev/sda2             485M   59M  401M  13% /boot
    /dev/sda1             200M  260K  200M   1% /boot/efi
    /dev/mapper/vg_erptest1-LV_TMP
                          9.9G  151M  9.2G   2% /tmp
    /dev/mapper/vg_erptest1-LV_U1
                          985G  212G  724G  23% /u1

make directory                          
                                       
    [root@target ~]# mkdir /u1/backup
    [root@target ~]# ls -l /u1
    total 35686692
    drwxrwx---. 10 testora dba         4096 Aug 15 14:04 11gR2_BASE
    drwxrwx---.  7 testora dba         4096 Jun  1 09:33 11gR2_BASE_11201
    drwxr-xr-x.  2 root    root        4096 Oct 15 13:49 backup
    drwxr-xr-x.  4 testora dba         4096 Jun 15 14:45 db_expimp
    drwx------.  2 root    root       16384 May 28 01:24 lost+found
    drwxr-xr-x.  3 testmgr dba         4096 Aug 15 14:01 oracle
    drwxr-xr-x. 10 testmgr dba         4096 Sep  5 21:44 patches
    -rw-r--r--.  1 root    root 36543116257 Jun 16 02:34 R1213_DB.tar.gz
    drwxr-xr-x.  3 root    root        4096 May 29 18:18 redhat

copy parameter file

    [oracle@db1 ~]$ sqlplus  /nolog

    SQL*Plus: Release 11.2.0.3.0 Production on Tue Oct 15 14:09:56 2013

    Copyright (c) 1982, 2011, Oracle.  All rights reserved.

    SQL> conn /as sysdba
    Connected.
    SQL> show parameter spfile

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    spfile				     string	 /u1/app/oracle/product/11.2.0/
                             db1/dbs/spfilePROD1.ora
    SQL> create pfile='/home/oracle/initPROD1.ora' from spfile;

    File created.

    SQL> exit
    Disconnected from Oracle Database 11g Enterprise Edition Release 11.2.0.3.0 - 64bit Production
    With the Partitioning, Real Application Clusters, Automatic Storage Management, OLAP,
    Data Mining and Real Application Testing options
    
    [oracle@db1 ~]$ scp initPROD1.ora root@192.168.1.5:/u1/backup/
    root@192.168.1.5's password: 
    initPROD1.ora                                                                                              100% 3121     3.1KB/s   00:00    

copy backup set
    
    [root@db1 ~]# scp /data/backup/* root@192.168.1.5:/u1/backup
    root@192.168.1.5's password: 
    20131016_inc0_7somi1rp_1_1.bkp                                                                      100% 1932KB   1.9MB/s   00:00    
    20131016_inc0_7tomi1rt_1_1.bkp                                                                      100%   72GB 110.7MB/s   11:07    
    20131016_inc0_7uomi2a5_1_1.bkp                                                                      100%   71GB 110.4MB/s   11:01    
    20131016_inc0_7vomi2n6_1_1.bkp                                                                      100%   67GB 109.6MB/s   10:27    
    20131016_inc0_80omi33a_1_1.bkp                                                                      100%   16MB  16.2MB/s   00:01    
    20131016_inc0_81omi33h_1_1.bkp                                                                      100% 2203KB   2.2MB/s   00:00 
    
    [testora@target ~]$ ll /u1/backup/
    total 220713556
    -rwxr-xr-x. 1 root    root     1978368 Oct 16 15:55 20131016_inc0_7somi1rp_1_1.bkp
    -rwxr-xr-x. 1 root    root 77434830848 Oct 16 16:06 20131016_inc0_7tomi1rt_1_1.bkp
    -rwxr-xr-x. 1 root    root 76532965376 Oct 16 16:18 20131016_inc0_7uomi2a5_1_1.bkp
    -rwxr-xr-x. 1 root    root 72021614592 Oct 16 16:28 20131016_inc0_7vomi2n6_1_1.bkp
    -rwxr-xr-x. 1 root    root    17006592 Oct 16 16:28 20131016_inc0_80omi33a_1_1.bkp
    -rwxr-xr-x. 1 root    root     2255872 Oct 16 16:28 20131016_inc0_81omi33h_1_1.bkp
    -rw-r--r--. 1 testora dba         3121 Oct 15 14:11 initPROD1.ora

make soft link    

    [testora@target ~]$ ln -s /u1/backup/  /data/backup
    [testora@target ~]$ ll /data/backup
    lrwxrwxrwx. 1 testora dba 11 Oct 16 16:33 /data/backup -> /u1/backup/
    [testora@target ~]$ ll /data/backup/
    total 220713556
    -rwxr-xr-x. 1 root    root     1978368 Oct 16 15:55 20131016_inc0_7somi1rp_1_1.bkp
    -rwxr-xr-x. 1 root    root 77434830848 Oct 16 16:06 20131016_inc0_7tomi1rt_1_1.bkp
    -rwxr-xr-x. 1 root    root 76532965376 Oct 16 16:18 20131016_inc0_7uomi2a5_1_1.bkp
    -rwxr-xr-x. 1 root    root 72021614592 Oct 16 16:28 20131016_inc0_7vomi2n6_1_1.bkp
    -rwxr-xr-x. 1 root    root    17006592 Oct 16 16:28 20131016_inc0_80omi33a_1_1.bkp
    -rwxr-xr-x. 1 root    root     2255872 Oct 16 16:28 20131016_inc0_81omi33h_1_1.bkp
    -rw-r--r--. 1 testora dba         3121 Oct 15 14:11 initPROD1.ora
    
###shared with nfs 

configure exportfs

    [root@db1 ~]# cat /etc/exports 
    /patch *(rw,root_squash,no_all_squash,sync)
    /data *(rw,no_root_squash,no_all_squash,sync)
    
restart nfs
    
    [root@db1 ~]# service nfs restart
    Shutting down NFS daemon:                                  [  OK  ]
    Shutting down NFS mountd:                                  [  OK  ]
    Shutting down NFS quotas:                                  [  OK  ]
    Shutting down NFS services:                                [  OK  ]
    Starting NFS services:                                     [  OK  ]
    Starting NFS quotas:                                       [  OK  ]
    Starting NFS mountd:                                       [  OK  ]
    Stopping RPC idmapd:                                       [  OK  ]
    Starting RPC idmapd:                                       [  OK  ]
    Starting NFS daemon:                                       [  OK  ]
    [root@db1 ~]# exportfs 
    /patch        	<world>
    /data    	<world>

mount on target system
    
    [root@target ~]# showmount -e 192.168.1.9
    Export list for 192.168.1.9:
    /data/pre1 *
    /patch     *
    [root@target ~]# mount 192.168.1.9:/data/ /data/
    [root@target ~]# ll /data/backup
    total 220713556
    -rw-r-----. 1 nobody nobody     1978368 Oct 16 12:32 20131016_inc0_7somi1rp_1_1.bkp
    -rw-r-----. 1 nobody nobody 77434830848 Oct 16 12:40 20131016_inc0_7tomi1rt_1_1.bkp
    -rw-r-----. 1 nobody nobody 76532965376 Oct 16 12:47 20131016_inc0_7uomi2a5_1_1.bkp
    -rw-r-----. 1 nobody nobody 72021614592 Oct 16 12:54 20131016_inc0_7vomi2n6_1_1.bkp
    -rw-r-----. 1 nobody nobody    17006592 Oct 16 12:54 20131016_inc0_80omi33a_1_1.bkp
    -rw-r-----. 1 nobody nobody     2255872 Oct 16 12:54 20131016_inc0_81omi33h_1_1.bkp

chmod backup directory    
   
    [root@target ~]# chmod -R 777 /data/backup/
    [root@target ~]# ll /data/backup/
    total 220713556
    -rwxrwxrwx. 1 nobody nobody     1978368 Oct 16 12:32 20131016_inc0_7somi1rp_1_1.bkp
    -rwxrwxrwx. 1 nobody nobody 77434830848 Oct 16 12:40 20131016_inc0_7tomi1rt_1_1.bkp
    -rwxrwxrwx. 1 nobody nobody 76532965376 Oct 16 12:47 20131016_inc0_7uomi2a5_1_1.bkp
    -rwxrwxrwx. 1 nobody nobody 72021614592 Oct 16 12:54 20131016_inc0_7vomi2n6_1_1.bkp
    -rwxrwxrwx. 1 nobody nobody    17006592 Oct 16 12:54 20131016_inc0_80omi33a_1_1.bkp
    -rwxrwxrwx. 1 nobody nobody     2255872 Oct 16 12:54 20131016_inc0_81omi33h_1_1.bkp
    
##recovery on target system

###edit parameter file

copy pfile to destination

    [testora@target ~]$ export ORACLE_SID=PROD
    [testora@target ~]$ echo $ORACLE_HOME
    /u1/11gR2_BASE/product/11.2.0
    [testora@target ~]$ cp /data/backup/initPROD1.ora /u1/11gR2_BASE/product/11.2.0/dbs/initPROD.ora
    [testora@target ~]$ cd /u1/11gR2_BASE/product/11.2.0/dbs/

before edit

    [testora@target dbs]$ cat initPROD.ora 
    PROD1.__db_cache_size=40802189312
    PROD1.__java_pool_size=939524096
    PROD1.__large_pool_size=134217728
    PROD1.__oracle_base='/u1/app/oracle'#ORACLE_BASE set from environment
    PROD1.__pga_aggregate_target=1073741824
    PROD1.__sga_target=51539607552
    PROD1.__shared_io_pool_size=402653184
    PROD1.__shared_pool_size=8724152320
    PROD1.__streams_pool_size=268435456
    *._b_tree_bitmap_plans=FALSE# Required 11i setting
    *._disable_fast_validate=TRUE#required by 761570.1
    *._fast_full_scan_enabled=FALSE
    *._immediate_commit_propagation=TRUE
    *._like_with_bind_as_equality=TRUE
    *._lm_global_posts=TRUE
    *._optimizer_autostats_job=false# Turning off auto statistics 
    *._pga_max_size=1048576000#required by 761570.1
    *._sort_elimination_cost_ratio=5
    *._system_trig_enabled=true
    *._trace_files_public=TRUE
    *._use_adaptive_log_file_sync='TRUE'# 'FALSE'
    *.aq_tm_processes=1
    *.audit_file_dest='/u1/app/oracle/admin/prod/adump'
    *.AUDIT_SYS_OPERATIONS=FALSE
    *.cluster_database=TRUE
    *.cluster_database_instances=2
    *.compatible='11.2.0'
    *.control_files='+DATADG/PROD/CONTROLFILE/control01.ctl','+FRADG/PROD/CONTROLFILE/control02.ctl'
    *.cursor_sharing='EXACT'# Required 11i settting
    *.db_block_checking='FALSE'
    *.db_block_checksum='TRUE'
    *.db_block_size=8192
    *.db_files=2000# Max. no. of database files
    *.db_name='PROD'
    *.db_writer_processes=6# improve IO performance
    *.diagnostic_dest='/u1/app/oracle/product/11.2.0/db1/admin/PROD1_db1'
    *.dml_locks=10000
    *.event='44951 trace name context forever, level 1024','31156 trace name context forever, level 0x400'# ref 3-4941349801
    *.filesystemio_options='SETALL'
    *.instance_name='PROD1'
    *.instance_number=1
    *.job_queue_processes=64
    *.log_archive_dest_1='LOCATION=+FRADG/PROD/archivelog/PROD1'
    *.log_archive_format='%t_%s_%r.dbf'
    *.log_buffer=10485760
    *.log_checkpoint_interval=100000
    *.log_checkpoint_timeout=1200# Checkpoint at least every 20 mins.
    *.log_checkpoints_to_alert=TRUE
    *.max_dump_file_size='20480'# trace file size 
    *.nls_comp='binary'# Required 11i setting 
    *.nls_date_format='DD-MON-RR'
    *.nls_length_semantics='BYTE'# Required 11i setting  
    *.nls_numeric_characters='.,'
    *.nls_sort='binary'# Required 11i setting 
    *.nls_territory='america'
    *.o7_dictionary_accessibility=FALSE#MP
    *.olap_page_pool_size=4194304
    *.open_cursors=1600# Consumes process memory, unless using MTS. 
    *.optimizer_secure_view_merging=false
    *.OS_AUTHENT_PREFIX=''
    *.parallel_max_servers=64
    *.parallel_min_servers=0
    *.pga_aggregate_target=1G
    *.plsql_code_type='INTERPRETED'# Default 11i setting
    *.plsql_optimize_level=2# Required 11i setting
    *.processes=5000# Max. no. of users x 2
    *.remote_listener='erpdb-cluster-scan:1521'
    *.sec_case_sensitive_logon=FALSE
    *.service_names='PROD1'
    *.session_cached_cursors=500
    *.sessions=4400# 2 X processes  
    *.sga_target=48G
    *.shared_pool_reserved_size=440M
    *.shared_pool_size=4400M
    *.SQL92_SECURITY=TRUE
    *.thread=1
    *.timed_statistics=true
    *.undo_management='AUTO'# Required 11i setting
    *.undo_tablespace='APPS_UNDOTS1'# Required 11i setting
    *.utl_file_dir='/usr/tmp','/u1/11gR2_BASE/product/11.2.0/appsutil/outbound/PROD1_db1'
    *.workarea_size_policy='AUTO'# Required 11i setting

after edit
    
    [testora@target dbs]$ cat initPROD.ora 
    PROD.__db_cache_size=40802189312
    PROD.__java_pool_size=939524096
    PROD.__large_pool_size=134217728
    PROD.__oracle_base='/u1/11gR2_BASE'#ORACLE_BASE set from environment
    PROD.__pga_aggregate_target=1073741824
    PROD.__sga_target=51539607552
    PROD.__shared_io_pool_size=402653184
    PROD.__shared_pool_size=8724152320
    PROD.__streams_pool_size=268435456
    *._b_tree_bitmap_plans=FALSE# Required 11i setting
    *._disable_fast_validate=TRUE#required by 761570.1
    *._fast_full_scan_enabled=FALSE
    *._immediate_commit_propagation=TRUE
    *._like_with_bind_as_equality=TRUE
    *._lm_global_posts=TRUE
    *._optimizer_autostats_job=false# Turning off auto statistics 
    *._pga_max_size=1048576000#required by 761570.1
    *._sort_elimination_cost_ratio=5
    *._system_trig_enabled=true
    *._trace_files_public=TRUE
    *._use_adaptive_log_file_sync='TRUE'# 'FALSE'
    *.aq_tm_processes=1
    *.audit_file_dest='/u1/11gR2_BASE/admin/prod/adump'
    *.AUDIT_SYS_OPERATIONS=FALSE
    *.compatible='11.2.0'
    *.control_files='/u1/TEST/testora/testdata/control01.ctl','/u1/TEST/testora/testdata/control02.ctl'
    *.cursor_sharing='EXACT'# Required 11i settting
    *.db_block_checking='FALSE'
    *.db_block_checksum='TRUE'
    *.db_block_size=8192
    *.db_files=2000# Max. no. of database files
    *.db_name='PROD'
    *.db_writer_processes=6# improve IO performance
    *.diagnostic_dest='/u1/11gR2_BASE/admin/prod'
    *.dml_locks=10000
    *.event='44951 trace name context forever, level 1024','31156 trace name context forever, level 0x400'# ref 3-4941349801
    *.filesystemio_options='SETALL'
    *.instance_name='PROD'
    *.job_queue_processes=64
    *.log_archive_dest_1='LOCATION=/u1/TEST/testora/archive'
    *.log_archive_format='%t_%s_%r.dbf'
    *.log_buffer=10485760
    *.log_checkpoint_interval=100000
    *.log_checkpoint_timeout=1200# Checkpoint at least every 20 mins.
    *.log_checkpoints_to_alert=TRUE
    *.max_dump_file_size='20480'# trace file size 
    *.nls_comp='binary'# Required 11i setting 
    *.nls_date_format='DD-MON-RR'
    *.nls_length_semantics='BYTE'# Required 11i setting  
    *.nls_numeric_characters='.,'
    *.nls_sort='binary'# Required 11i setting 
    *.nls_territory='america'
    *.o7_dictionary_accessibility=FALSE#MP
    *.olap_page_pool_size=4194304
    *.open_cursors=1600# Consumes process memory, unless using MTS. 
    *.optimizer_secure_view_merging=false
    *.OS_AUTHENT_PREFIX=''
    *.parallel_max_servers=64
    *.parallel_min_servers=0
    *.pga_aggregate_target=1G
    *.plsql_code_type='INTERPRETED'# Default 11i setting
    *.plsql_optimize_level=2# Required 11i setting
    *.processes=5000# Max. no. of users x 2
    *.sec_case_sensitive_logon=FALSE
    *.service_names='PROD'
    *.session_cached_cursors=500
    *.sessions=4400# 2 X processes  
    *.sga_target=48G
    *.shared_pool_reserved_size=440M
    *.shared_pool_size=4400M
    *.SQL92_SECURITY=TRUE
    *.thread=1
    *.timed_statistics=true
    *.undo_management='AUTO'# Required 11i setting
    *.undo_tablespace='APPS_UNDOTS1'# Required 11i setting
    *.utl_file_dir='/usr/tmp','/u1/11gR2_BASE/product/11.2.0/appsutil/PROD'
    *.workarea_size_policy='AUTO'# Required 11i setting
    *.log_file_name_convert=('+DATADG/prodora/proddata','/u1/TEST/testora/testdata')
    *.db_file_name_convert=('+DATADG/prodora/proddata','/u1/TEST/testora/testdata')

copy initPROD.ora to init.ora

    [testora@target dbs]$ cp initPROD.ora init.ora
    
diff between initPROD1.ora and initPROD.ora

    [testora@target ~]$ diff  /data/backup/initPROD1.ora /u1/11gR2_BASE/product/11.2.0/dbs/initPROD.ora
    1,9c1,9
    < PROD1.__db_cache_size=40802189312
    < PROD1.__java_pool_size=939524096
    < PROD1.__large_pool_size=134217728
    < PROD1.__oracle_base='/u1/app/oracle'#ORACLE_BASE set from environment
    < PROD1.__pga_aggregate_target=1073741824
    < PROD1.__sga_target=51539607552
    < PROD1.__shared_io_pool_size=402653184
    < PROD1.__shared_pool_size=8724152320
    < PROD1.__streams_pool_size=268435456
    ---
    > PROD.__db_cache_size=40802189312
    > PROD.__java_pool_size=939524096
    > PROD.__large_pool_size=134217728
    > PROD.__oracle_base='/u1/11gR2_BASE'#ORACLE_BASE set from environment
    > PROD.__pga_aggregate_target=1073741824
    > PROD.__sga_target=51539607552
    > PROD.__shared_io_pool_size=402653184
    > PROD.__shared_pool_size=8724152320
    > PROD.__streams_pool_size=268435456
    23c23
    < *.audit_file_dest='/u1/app/oracle/admin/prod/adump'
    ---
    > *.audit_file_dest='/u1/11gR2_BASE/admin/prod/adump'
    25,26d24
    < *.cluster_database=TRUE
    < *.cluster_database_instances=2
    28c26
    < *.control_files='+DATADG/PROD/CONTROLFILE/control01.ctl','+FRADG/PROD/CONTROLFILE/control02.ctl'
    ---
    > *.control_files='/u1/TEST/testora/testdata/control01.ctl','/u1/TEST/testora/testdata/control02.ctl'
    36c34
    < *.diagnostic_dest='/u1/app/oracle/product/11.2.0/db1/admin/PROD1_db1'
    ---
    > *.diagnostic_dest='/u1/11gR2_BASE/admin/prod'
    40,41c38
    < *.instance_name='PROD1'
    < *.instance_number=1
    ---
    > *.instance_name='PROD'
    43c40
    < *.log_archive_dest_1='LOCATION=+FRADG/PROD/archivelog/PROD1'
    ---
    > *.log_archive_dest_1='LOCATION=/u1/TEST/testora/archive'
    67d63
    < *.remote_listener='erpdb-cluster-scan:1521'
    69c67
    < *.service_names='PROD1'
    ---
    > *.service_names='PROD'
    80c76
    < *.utl_file_dir='/usr/tmp','/u1/11gR2_BASE/product/11.2.0/appsutil/outbound/PROD1_db1'
    ---
    > *.utl_file_dir='/usr/tmp','/u1/11gR2_BASE/product/11.2.0/appsutil/PROD'
    81a78,79
    > *.log_file_name_convert=('+DATADG/prodora/proddata','/u1/TEST/testora/testdata')
    > *.db_file_name_convert=('+DATADG/prodora/proddata','/u1/TEST/testora/testdata')
    
###recovery test
    
    [testora@target ~]$ export ORACLE_SID=PROD
    [testora@target ~]$ rman target/

    Recovery Manager: Release 11.2.0.3.0 - Production on Thu Oct 17 10:48:57 2013

    Copyright (c) 1982, 2011, Oracle and/or its affiliates.  All rights reserved.

    connected to target database (not started)

    RMAN> set dbid=240240185;

    executing command: SET DBID

    RMAN> startup nomount;

    Oracle instance started

    Total System Global Area   51309510656 bytes

    Fixed Size                     2240344 bytes
    Variable Size              10066329768 bytes
    Database Buffers           41204842496 bytes
    Redo Buffers                  36098048 bytes

    RMAN> restore controlfile from '/data/controlfile/ctl_file_c-240240185-20131017-01';

    Starting restore at 17-OCT-13
    using target database control file instead of recovery catalog
    allocated channel: ORA_DISK_1
    channel ORA_DISK_1: SID=2 device type=DISK

    channel ORA_DISK_1: restoring control file
    channel ORA_DISK_1: restore complete, elapsed time: 00:00:01
    output file name=/u1/TEST/testora/testdata/control01.ctl
    output file name=/u1/TEST/testora/testdata/control02.ctl
    Finished restore at 17-OCT-13

    RMAN> alter database mount;

    database mounted
    released channel: ORA_DISK_1

    RMAN> list backup of controlfile;


    List of Backup Sets
    ===================


    BS Key  Type LV Size       Device Type Elapsed Time Completion Time
    ------- ---- -- ---------- ----------- ------------ ---------------
    262     Incr 0  18.42M     DISK        00:00:01     16-OCT-13      
            BP Key: 282   Status: AVAILABLE  Compressed: NO  Tag: TEST INC0 BACKUP
            Piece Name: /data/backup/20131016_inc0_86omij5d_1_1.bkp
      Control File Included: Ckp SCN: 99193819     Ckp time: 16-OCT-13

    BS Key  Type LV Size       Device Type Elapsed Time Completion Time
    ------- ---- -- ---------- ----------- ------------ ---------------
    264     Full    18.39M     DISK        00:00:01     17-OCT-13      
            BP Key: 284   Status: AVAILABLE  Compressed: NO  Tag: CF1
            Piece Name: /data/backup/ctl_file_20131017_88omkbta
      Control File Included: Ckp SCN: 100644641    Ckp time: 17-OCT-13

    BS Key  Type LV Size       Device Type Elapsed Time Completion Time
    ------- ---- -- ---------- ----------- ------------ ---------------
    268     Full    18.42M     DISK        00:00:00     17-OCT-13      
            BP Key: 308   Status: AVAILABLE  Compressed: NO  Tag: TAG20131017T104019
            Piece Name: /data/controlfile/ctl_file_c-240240185-20131017-00
      Control File Included: Ckp SCN: 101311620    Ckp time: 17-OCT-13

    BS Key  Type LV Size       Device Type Elapsed Time Completion Time
    ------- ---- -- ---------- ----------- ------------ ---------------
    273     Full    18.39M     DISK        00:00:01     17-OCT-13      
            BP Key: 313   Status: AVAILABLE  Compressed: NO  Tag: BAK_CTLFILE
            Piece Name: /data/backup/ctl_file_829046450_1_273
      Control File Included: Ckp SCN: 101313008    Ckp time: 17-OCT-13

    RMAN> list backup of spfile;


    List of Backup Sets
    ===================


    BS Key  Type LV Size       Device Type Elapsed Time Completion Time
    ------- ---- -- ---------- ----------- ------------ ---------------
    262     Incr 0  18.42M     DISK        00:00:01     16-OCT-13      
            BP Key: 282   Status: AVAILABLE  Compressed: NO  Tag: TEST INC0 BACKUP
            Piece Name: /data/backup/20131016_inc0_86omij5d_1_1.bkp
      SPFILE Included: Modification time: 15-OCT-13
      SPFILE db_unique_name: PROD

    BS Key  Type LV Size       Device Type Elapsed Time Completion Time
    ------- ---- -- ---------- ----------- ------------ ---------------
    268     Full    18.42M     DISK        00:00:00     17-OCT-13      
            BP Key: 308   Status: AVAILABLE  Compressed: NO  Tag: TAG20131017T104019
            Piece Name: /data/controlfile/ctl_file_c-240240185-20131017-00
      SPFILE Included: Modification time: 15-OCT-13
      SPFILE db_unique_name: PROD

    RMAN> run {set newname for datafile 1 to "/u1/TEST/testora/testdata/system01.dbf"; restore datafile 1;recover datafile 1;}

    executing command: SET NEWNAME

    Starting restore at 17-OCT-13
    allocated channel: ORA_DISK_1
    channel ORA_DISK_1: SID=2 device type=DISK

    channel ORA_DISK_1: starting datafile backup set restore
    channel ORA_DISK_1: specifying datafile(s) to restore from backup set
    channel ORA_DISK_1: restoring datafile 00001 to /u1/TEST/testora/testdata/system01.dbf
    channel ORA_DISK_1: reading from backup piece /data/backup/db_bak_lev0_829046009_1_267
    channel ORA_DISK_1: piece handle=/data/backup/db_bak_lev0_829046009_1_267 tag=DB_BAK_LEV0
    channel ORA_DISK_1: restored backup piece 1
    channel ORA_DISK_1: reading from backup piece /data/backup/db_bak_lev0_829046009_2_267
    channel ORA_DISK_1: piece handle=/data/backup/db_bak_lev0_829046009_2_267 tag=DB_BAK_LEV0
    channel ORA_DISK_1: restored backup piece 2
    channel ORA_DISK_1: reading from backup piece /data/backup/db_bak_lev0_829046009_3_267
    channel ORA_DISK_1: piece handle=/data/backup/db_bak_lev0_829046009_3_267 tag=DB_BAK_LEV0
    channel ORA_DISK_1: restored backup piece 3
    channel ORA_DISK_1: reading from backup piece /data/backup/db_bak_lev0_829046009_4_267
    channel ORA_DISK_1: piece handle=/data/backup/db_bak_lev0_829046009_4_267 tag=DB_BAK_LEV0
    channel ORA_DISK_1: restored backup piece 4
    channel ORA_DISK_1: reading from backup piece /data/backup/db_bak_lev0_829046009_5_267
    channel ORA_DISK_1: piece handle=/data/backup/db_bak_lev0_829046009_5_267 tag=DB_BAK_LEV0
    channel ORA_DISK_1: restored backup piece 5
    channel ORA_DISK_1: reading from backup piece /data/backup/db_bak_lev0_829046009_6_267
    channel ORA_DISK_1: piece handle=/data/backup/db_bak_lev0_829046009_6_267 tag=DB_BAK_LEV0
    channel ORA_DISK_1: restored backup piece 6
    channel ORA_DISK_1: reading from backup piece /data/backup/db_bak_lev0_829046009_7_267
    channel ORA_DISK_1: piece handle=/data/backup/db_bak_lev0_829046009_7_267 tag=DB_BAK_LEV0
    channel ORA_DISK_1: restored backup piece 7
    channel ORA_DISK_1: restore complete, elapsed time: 00:10:35
    Finished restore at 17-OCT-13

    Starting recover at 17-OCT-13
    using channel ORA_DISK_1

    RMAN-00571: ===========================================================
    RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
    RMAN-00571: ===========================================================
    RMAN-03002: failure of recover command at 10/17/2013 11:01:15
    RMAN-06067: RECOVER DATABASE required with a backup or created control file
    
    [root@target testdata]# ll -h
    total 1.1G
    -rw-r-----. 1 testora dba   19M Oct 17 11:01 control01.ctl
    -rw-r-----. 1 testora dba   19M Oct 17 11:01 control02.ctl
    -rw-r-----. 1 testora dba 1001M Oct 17 11:01 system01.dbf
    
    
rman-06067
    
    Error:	RMAN 6067
    Text:	RECOVER DATABASE required with a backup or created controlfile 
    ---------------------------------------------------------------------------
    Cause:	The controlfile has been restored from a backup or was created via 
        ALTER DATABASE CREATE CONTROLFILE. 
    Action:	Use the RECOVER DATABASE command to perform the recovery.
    
clean failure instance and datafiles

    RMAN> shutdown immediate;
    
    [root@target testdata]# rm control01.ctl control02.ctl system01.dbf
    
###recover database
  
sql script to set newname for datafile  
  
    SELECT FILE#,
           NAME,
           '''' ||NEWNAME || ''',' newname,
           'set newname for datafile ' || FILE# || ' to "' || NEWNAME ||
           '";' RECOVERY
      FROM (SELECT FILE#,
                   NAME,
                   REPLACE(REPLACE(NAME,
                           '+DATADG/prod/datafile/',
                           '/u1/TEST/testora/testdata/'),
                           '+DATADG/prod/undofile/',
                           '/u1/TEST/testora/testdata/'
                           ) NEWNAME
              FROM V$DATAFILE);
              
sql script output

    --new path
    '/u1/TEST/testora/testdata/system01.dbf',
    '/u1/TEST/testora/testdata/system02.dbf',
    '/u1/TEST/testora/testdata/system03.dbf',
    '/u1/TEST/testora/testdata/system04.dbf',
    '/u1/TEST/testora/testdata/system05.dbf',
    '/u1/TEST/testora/testdata/system06.dbf',
    '/u1/TEST/testora/testdata/system07.dbf',
    '/u1/TEST/testora/testdata/system08.dbf',
    '/u1/TEST/testora/testdata/system09.dbf',
    '/u1/TEST/testora/testdata/system10.dbf',
    '/u1/TEST/testora/testdata/system11.dbf',
    '/u1/TEST/testora/testdata/sysaux01.dbf',
    '/u1/TEST/testora/testdata/undo01.dbf',
    '/u1/TEST/testora/testdata/undo02.dbf',
    '/u1/TEST/testora/testdata/undo03.dbf',
    '/u1/TEST/testora/testdata/a_archive01.dbf',
    '/u1/TEST/testora/testdata/a_archive02.dbf',
    '/u1/TEST/testora/testdata/a_archive03.dbf',
    '/u1/TEST/testora/testdata/a_archive04.dbf',
    '/u1/TEST/testora/testdata/a_archive05.dbf',
    '/u1/TEST/testora/testdata/a_int01.dbf',
    '/u1/TEST/testora/testdata/a_int02.dbf',
    '/u1/TEST/testora/testdata/a_int03.dbf',
    '/u1/TEST/testora/testdata/a_int04.dbf',
    '/u1/TEST/testora/testdata/a_int05.dbf',
    '/u1/TEST/testora/testdata/a_int06.dbf',
    '/u1/TEST/testora/testdata/a_int07.dbf',
    '/u1/TEST/testora/testdata/a_int08.dbf',
    '/u1/TEST/testora/testdata/a_media01.dbf',
    '/u1/TEST/testora/testdata/a_media02.dbf',
    '/u1/TEST/testora/testdata/a_media03.dbf',
    '/u1/TEST/testora/testdata/a_media04.dbf',
    '/u1/TEST/testora/testdata/a_media05.dbf',
    '/u1/TEST/testora/testdata/a_media06.dbf',
    '/u1/TEST/testora/testdata/a_media07.dbf',
    '/u1/TEST/testora/testdata/a_media08.dbf',
    '/u1/TEST/testora/testdata/a_media09.dbf',
    '/u1/TEST/testora/testdata/a_media10.dbf',
    '/u1/TEST/testora/testdata/a_nolog01.dbf',
    '/u1/TEST/testora/testdata/a_queue01.dbf',
    '/u1/TEST/testora/testdata/a_queue02.dbf',
    '/u1/TEST/testora/testdata/a_queue03.dbf',
    '/u1/TEST/testora/testdata/a_queue04.dbf',
    '/u1/TEST/testora/testdata/a_queue05.dbf',
    '/u1/TEST/testora/testdata/a_queue06.dbf',
    '/u1/TEST/testora/testdata/a_queue07.dbf',
    '/u1/TEST/testora/testdata/a_queue08.dbf',
    '/u1/TEST/testora/testdata/a_queue09.dbf',
    '/u1/TEST/testora/testdata/a_queue10.dbf',
    '/u1/TEST/testora/testdata/a_queue11.dbf',
    '/u1/TEST/testora/testdata/a_queue12.dbf',
    '/u1/TEST/testora/testdata/a_queue13.dbf',
    '/u1/TEST/testora/testdata/a_queue14.dbf',
    '/u1/TEST/testora/testdata/a_queue15.dbf',
    '/u1/TEST/testora/testdata/a_queue16.dbf',
    '/u1/TEST/testora/testdata/a_queue17.dbf',
    '/u1/TEST/testora/testdata/a_queue18.dbf',
    '/u1/TEST/testora/testdata/a_queue19.dbf',
    '/u1/TEST/testora/testdata/a_queue20.dbf',
    '/u1/TEST/testora/testdata/a_queue21.dbf',
    '/u1/TEST/testora/testdata/a_queue22.dbf',
    '/u1/TEST/testora/testdata/a_queue23.dbf',
    '/u1/TEST/testora/testdata/a_queue24.dbf',
    '/u1/TEST/testora/testdata/a_queue25.dbf',
    '/u1/TEST/testora/testdata/a_ref01.dbf',
    '/u1/TEST/testora/testdata/a_ref02.dbf',
    '/u1/TEST/testora/testdata/a_summ01.dbf',
    '/u1/TEST/testora/testdata/a_summ02.dbf',
    '/u1/TEST/testora/testdata/a_summ03.dbf',
    '/u1/TEST/testora/testdata/a_summ04.dbf',
    '/u1/TEST/testora/testdata/a_summ05.dbf',
    '/u1/TEST/testora/testdata/a_tools01.dbf',
    '/u1/TEST/testora/testdata/a_txn_data01.dbf',
    '/u1/TEST/testora/testdata/a_txn_data02.dbf',
    '/u1/TEST/testora/testdata/a_txn_data03.dbf',
    '/u1/TEST/testora/testdata/a_txn_data04.dbf',
    '/u1/TEST/testora/testdata/a_txn_data05.dbf',
    '/u1/TEST/testora/testdata/a_txn_data06.dbf',
    '/u1/TEST/testora/testdata/a_txn_data07.dbf',
    '/u1/TEST/testora/testdata/a_txn_data08.dbf',
    '/u1/TEST/testora/testdata/a_txn_data09.dbf',
    '/u1/TEST/testora/testdata/a_txn_data10.dbf',
    '/u1/TEST/testora/testdata/a_txn_data11.dbf',
    '/u1/TEST/testora/testdata/a_txn_data12.dbf',
    '/u1/TEST/testora/testdata/a_txn_data13.dbf',
    '/u1/TEST/testora/testdata/a_txn_data14.dbf',
    '/u1/TEST/testora/testdata/a_txn_data15.dbf',
    '/u1/TEST/testora/testdata/a_txn_data16.dbf',
    '/u1/TEST/testora/testdata/a_txn_data17.dbf',
    '/u1/TEST/testora/testdata/a_txn_data18.dbf',
    '/u1/TEST/testora/testdata/a_txn_data19.dbf',
    '/u1/TEST/testora/testdata/a_txn_data20.dbf',
    '/u1/TEST/testora/testdata/a_txn_data21.dbf',
    '/u1/TEST/testora/testdata/a_txn_data22.dbf',
    '/u1/TEST/testora/testdata/a_txn_data23.dbf',
    '/u1/TEST/testora/testdata/a_txn_data24.dbf',
    '/u1/TEST/testora/testdata/a_txn_data25.dbf',
    '/u1/TEST/testora/testdata/a_txn_data26.dbf',
    '/u1/TEST/testora/testdata/a_txn_data28.dbf',
    '/u1/TEST/testora/testdata/a_txn_data29.dbf',
    '/u1/TEST/testora/testdata/a_txn_data30.dbf',
    '/u1/TEST/testora/testdata/a_txn_data31.dbf',
    '/u1/TEST/testora/testdata/a_txn_data32.dbf',
    '/u1/TEST/testora/testdata/a_txn_data33.dbf',
    '/u1/TEST/testora/testdata/a_txn_data34.dbf',
    '/u1/TEST/testora/testdata/a_txn_data35.dbf',
    '/u1/TEST/testora/testdata/a_txn_data36.dbf',
    '/u1/TEST/testora/testdata/a_txn_data37.dbf',
    '/u1/TEST/testora/testdata/a_txn_data38.dbf',
    '/u1/TEST/testora/testdata/a_txn_data39.dbf',
    '/u1/TEST/testora/testdata/a_txn_data40.dbf',
    '/u1/TEST/testora/testdata/a_txn_data41.dbf',
    '/u1/TEST/testora/testdata/a_txn_data42.dbf',
    '/u1/TEST/testora/testdata/a_txn_data43.dbf',
    '/u1/TEST/testora/testdata/a_txn_data44.dbf',
    '/u1/TEST/testora/testdata/a_txn_data45.dbf',
    '/u1/TEST/testora/testdata/a_txn_data46.dbf',
    '/u1/TEST/testora/testdata/a_txn_data47.dbf',
    '/u1/TEST/testora/testdata/a_txn_data48.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind01.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind02.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind03.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind04.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind05.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind06.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind07.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind08.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind09.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind10.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind11.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind12.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind13.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind14.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind15.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind16.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind17.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind18.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind19.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind20.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind21.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind22.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind23.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind24.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind25.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind26.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind27.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind28.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind29.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind30.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind31.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind32.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind33.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind34.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind35.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind36.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind37.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind38.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind39.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind40.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind41.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind42.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind43.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind44.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind45.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind46.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind47.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind48.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind49.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind50.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind51.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind52.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind53.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind54.dbf',
    '/u1/TEST/testora/testdata/a_txn_ind55.dbf',
    '/u1/TEST/testora/testdata/ctxd01.dbf',
    '/u1/TEST/testora/testdata/odm.dbf',
    '/u1/TEST/testora/testdata/olap.dbf',
    '/u1/TEST/testora/testdata/owad01.dbf',
    '/u1/TEST/testora/testdata/portal01.dbf',
    '/u1/TEST/testora/testdata/statspack_01.dbf',
    '/u1/TEST/testora/testdata/tplcux_data_01.dbf',
    '/u1/TEST/testora/testdata/tplcux_idx_01.dbf',
    '/u1/TEST/testora/testdata/interim.dbf',
    '/u1/TEST/testora/testdata/system12.dbf',
    '/u1/TEST/testora/testdata/a_txn_data49.dbf',
    '/u1/TEST/testora/testdata/a_ref03.dbf',
    '/u1/TEST/testora/testdata/a_summ06.dbf',
    '/u1/TEST/testora/testdata/undo04.dbf',
    
    --set newname;
    set newname for datafile 1 to "/u1/TEST/testora/testdata/system01.dbf";
    set newname for datafile 2 to "/u1/TEST/testora/testdata/system02.dbf";
    set newname for datafile 3 to "/u1/TEST/testora/testdata/system03.dbf";
    set newname for datafile 4 to "/u1/TEST/testora/testdata/system04.dbf";
    set newname for datafile 5 to "/u1/TEST/testora/testdata/system05.dbf";
    set newname for datafile 6 to "/u1/TEST/testora/testdata/system06.dbf";
    set newname for datafile 7 to "/u1/TEST/testora/testdata/system07.dbf";
    set newname for datafile 8 to "/u1/TEST/testora/testdata/system08.dbf";
    set newname for datafile 9 to "/u1/TEST/testora/testdata/system09.dbf";
    set newname for datafile 10 to "/u1/TEST/testora/testdata/system10.dbf";
    set newname for datafile 11 to "/u1/TEST/testora/testdata/system11.dbf";
    set newname for datafile 12 to "/u1/TEST/testora/testdata/sysaux01.dbf";
    set newname for datafile 13 to "/u1/TEST/testora/testdata/undo01.dbf";
    set newname for datafile 14 to "/u1/TEST/testora/testdata/undo02.dbf";
    set newname for datafile 15 to "/u1/TEST/testora/testdata/undo03.dbf";
    set newname for datafile 16 to "/u1/TEST/testora/testdata/a_archive01.dbf";
    set newname for datafile 17 to "/u1/TEST/testora/testdata/a_archive02.dbf";
    set newname for datafile 18 to "/u1/TEST/testora/testdata/a_archive03.dbf";
    set newname for datafile 19 to "/u1/TEST/testora/testdata/a_archive04.dbf";
    set newname for datafile 20 to "/u1/TEST/testora/testdata/a_archive05.dbf";
    set newname for datafile 21 to "/u1/TEST/testora/testdata/a_int01.dbf";
    set newname for datafile 22 to "/u1/TEST/testora/testdata/a_int02.dbf";
    set newname for datafile 23 to "/u1/TEST/testora/testdata/a_int03.dbf";
    set newname for datafile 24 to "/u1/TEST/testora/testdata/a_int04.dbf";
    set newname for datafile 25 to "/u1/TEST/testora/testdata/a_int05.dbf";
    set newname for datafile 26 to "/u1/TEST/testora/testdata/a_int06.dbf";
    set newname for datafile 27 to "/u1/TEST/testora/testdata/a_int07.dbf";
    set newname for datafile 28 to "/u1/TEST/testora/testdata/a_int08.dbf";
    set newname for datafile 29 to "/u1/TEST/testora/testdata/a_media01.dbf";
    set newname for datafile 30 to "/u1/TEST/testora/testdata/a_media02.dbf";
    set newname for datafile 31 to "/u1/TEST/testora/testdata/a_media03.dbf";
    set newname for datafile 32 to "/u1/TEST/testora/testdata/a_media04.dbf";
    set newname for datafile 33 to "/u1/TEST/testora/testdata/a_media05.dbf";
    set newname for datafile 34 to "/u1/TEST/testora/testdata/a_media06.dbf";
    set newname for datafile 35 to "/u1/TEST/testora/testdata/a_media07.dbf";
    set newname for datafile 36 to "/u1/TEST/testora/testdata/a_media08.dbf";
    set newname for datafile 37 to "/u1/TEST/testora/testdata/a_media09.dbf";
    set newname for datafile 38 to "/u1/TEST/testora/testdata/a_media10.dbf";
    set newname for datafile 39 to "/u1/TEST/testora/testdata/a_nolog01.dbf";
    set newname for datafile 40 to "/u1/TEST/testora/testdata/a_queue01.dbf";
    set newname for datafile 41 to "/u1/TEST/testora/testdata/a_queue02.dbf";
    set newname for datafile 42 to "/u1/TEST/testora/testdata/a_queue03.dbf";
    set newname for datafile 43 to "/u1/TEST/testora/testdata/a_queue04.dbf";
    set newname for datafile 44 to "/u1/TEST/testora/testdata/a_queue05.dbf";
    set newname for datafile 45 to "/u1/TEST/testora/testdata/a_queue06.dbf";
    set newname for datafile 46 to "/u1/TEST/testora/testdata/a_queue07.dbf";
    set newname for datafile 47 to "/u1/TEST/testora/testdata/a_queue08.dbf";
    set newname for datafile 48 to "/u1/TEST/testora/testdata/a_queue09.dbf";
    set newname for datafile 49 to "/u1/TEST/testora/testdata/a_queue10.dbf";
    set newname for datafile 50 to "/u1/TEST/testora/testdata/a_queue11.dbf";
    set newname for datafile 51 to "/u1/TEST/testora/testdata/a_queue12.dbf";
    set newname for datafile 52 to "/u1/TEST/testora/testdata/a_queue13.dbf";
    set newname for datafile 53 to "/u1/TEST/testora/testdata/a_queue14.dbf";
    set newname for datafile 54 to "/u1/TEST/testora/testdata/a_queue15.dbf";
    set newname for datafile 55 to "/u1/TEST/testora/testdata/a_queue16.dbf";
    set newname for datafile 56 to "/u1/TEST/testora/testdata/a_queue17.dbf";
    set newname for datafile 57 to "/u1/TEST/testora/testdata/a_queue18.dbf";
    set newname for datafile 58 to "/u1/TEST/testora/testdata/a_queue19.dbf";
    set newname for datafile 59 to "/u1/TEST/testora/testdata/a_queue20.dbf";
    set newname for datafile 60 to "/u1/TEST/testora/testdata/a_queue21.dbf";
    set newname for datafile 61 to "/u1/TEST/testora/testdata/a_queue22.dbf";
    set newname for datafile 62 to "/u1/TEST/testora/testdata/a_queue23.dbf";
    set newname for datafile 63 to "/u1/TEST/testora/testdata/a_queue24.dbf";
    set newname for datafile 64 to "/u1/TEST/testora/testdata/a_queue25.dbf";
    set newname for datafile 65 to "/u1/TEST/testora/testdata/a_ref01.dbf";
    set newname for datafile 66 to "/u1/TEST/testora/testdata/a_ref02.dbf";
    set newname for datafile 67 to "/u1/TEST/testora/testdata/a_summ01.dbf";
    set newname for datafile 68 to "/u1/TEST/testora/testdata/a_summ02.dbf";
    set newname for datafile 69 to "/u1/TEST/testora/testdata/a_summ03.dbf";
    set newname for datafile 70 to "/u1/TEST/testora/testdata/a_summ04.dbf";
    set newname for datafile 71 to "/u1/TEST/testora/testdata/a_summ05.dbf";
    set newname for datafile 72 to "/u1/TEST/testora/testdata/a_tools01.dbf";
    set newname for datafile 73 to "/u1/TEST/testora/testdata/a_txn_data01.dbf";
    set newname for datafile 74 to "/u1/TEST/testora/testdata/a_txn_data02.dbf";
    set newname for datafile 75 to "/u1/TEST/testora/testdata/a_txn_data03.dbf";
    set newname for datafile 76 to "/u1/TEST/testora/testdata/a_txn_data04.dbf";
    set newname for datafile 77 to "/u1/TEST/testora/testdata/a_txn_data05.dbf";
    set newname for datafile 78 to "/u1/TEST/testora/testdata/a_txn_data06.dbf";
    set newname for datafile 79 to "/u1/TEST/testora/testdata/a_txn_data07.dbf";
    set newname for datafile 80 to "/u1/TEST/testora/testdata/a_txn_data08.dbf";
    set newname for datafile 81 to "/u1/TEST/testora/testdata/a_txn_data09.dbf";
    set newname for datafile 82 to "/u1/TEST/testora/testdata/a_txn_data10.dbf";
    set newname for datafile 83 to "/u1/TEST/testora/testdata/a_txn_data11.dbf";
    set newname for datafile 84 to "/u1/TEST/testora/testdata/a_txn_data12.dbf";
    set newname for datafile 85 to "/u1/TEST/testora/testdata/a_txn_data13.dbf";
    set newname for datafile 86 to "/u1/TEST/testora/testdata/a_txn_data14.dbf";
    set newname for datafile 87 to "/u1/TEST/testora/testdata/a_txn_data15.dbf";
    set newname for datafile 88 to "/u1/TEST/testora/testdata/a_txn_data16.dbf";
    set newname for datafile 89 to "/u1/TEST/testora/testdata/a_txn_data17.dbf";
    set newname for datafile 90 to "/u1/TEST/testora/testdata/a_txn_data18.dbf";
    set newname for datafile 91 to "/u1/TEST/testora/testdata/a_txn_data19.dbf";
    set newname for datafile 92 to "/u1/TEST/testora/testdata/a_txn_data20.dbf";
    set newname for datafile 93 to "/u1/TEST/testora/testdata/a_txn_data21.dbf";
    set newname for datafile 94 to "/u1/TEST/testora/testdata/a_txn_data22.dbf";
    set newname for datafile 95 to "/u1/TEST/testora/testdata/a_txn_data23.dbf";
    set newname for datafile 96 to "/u1/TEST/testora/testdata/a_txn_data24.dbf";
    set newname for datafile 97 to "/u1/TEST/testora/testdata/a_txn_data25.dbf";
    set newname for datafile 98 to "/u1/TEST/testora/testdata/a_txn_data26.dbf";
    set newname for datafile 99 to "/u1/TEST/testora/testdata/a_txn_data28.dbf";
    set newname for datafile 100 to "/u1/TEST/testora/testdata/a_txn_data29.dbf";
    set newname for datafile 101 to "/u1/TEST/testora/testdata/a_txn_data30.dbf";
    set newname for datafile 102 to "/u1/TEST/testora/testdata/a_txn_data31.dbf";
    set newname for datafile 103 to "/u1/TEST/testora/testdata/a_txn_data32.dbf";
    set newname for datafile 104 to "/u1/TEST/testora/testdata/a_txn_data33.dbf";
    set newname for datafile 105 to "/u1/TEST/testora/testdata/a_txn_data34.dbf";
    set newname for datafile 106 to "/u1/TEST/testora/testdata/a_txn_data35.dbf";
    set newname for datafile 107 to "/u1/TEST/testora/testdata/a_txn_data36.dbf";
    set newname for datafile 108 to "/u1/TEST/testora/testdata/a_txn_data37.dbf";
    set newname for datafile 109 to "/u1/TEST/testora/testdata/a_txn_data38.dbf";
    set newname for datafile 110 to "/u1/TEST/testora/testdata/a_txn_data39.dbf";
    set newname for datafile 111 to "/u1/TEST/testora/testdata/a_txn_data40.dbf";
    set newname for datafile 112 to "/u1/TEST/testora/testdata/a_txn_data41.dbf";
    set newname for datafile 113 to "/u1/TEST/testora/testdata/a_txn_data42.dbf";
    set newname for datafile 114 to "/u1/TEST/testora/testdata/a_txn_data43.dbf";
    set newname for datafile 115 to "/u1/TEST/testora/testdata/a_txn_data44.dbf";
    set newname for datafile 116 to "/u1/TEST/testora/testdata/a_txn_data45.dbf";
    set newname for datafile 117 to "/u1/TEST/testora/testdata/a_txn_data46.dbf";
    set newname for datafile 118 to "/u1/TEST/testora/testdata/a_txn_data47.dbf";
    set newname for datafile 119 to "/u1/TEST/testora/testdata/a_txn_data48.dbf";
    set newname for datafile 120 to "/u1/TEST/testora/testdata/a_txn_ind01.dbf";
    set newname for datafile 121 to "/u1/TEST/testora/testdata/a_txn_ind02.dbf";
    set newname for datafile 122 to "/u1/TEST/testora/testdata/a_txn_ind03.dbf";
    set newname for datafile 123 to "/u1/TEST/testora/testdata/a_txn_ind04.dbf";
    set newname for datafile 124 to "/u1/TEST/testora/testdata/a_txn_ind05.dbf";
    set newname for datafile 125 to "/u1/TEST/testora/testdata/a_txn_ind06.dbf";
    set newname for datafile 126 to "/u1/TEST/testora/testdata/a_txn_ind07.dbf";
    set newname for datafile 127 to "/u1/TEST/testora/testdata/a_txn_ind08.dbf";
    set newname for datafile 128 to "/u1/TEST/testora/testdata/a_txn_ind09.dbf";
    set newname for datafile 129 to "/u1/TEST/testora/testdata/a_txn_ind10.dbf";
    set newname for datafile 130 to "/u1/TEST/testora/testdata/a_txn_ind11.dbf";
    set newname for datafile 131 to "/u1/TEST/testora/testdata/a_txn_ind12.dbf";
    set newname for datafile 132 to "/u1/TEST/testora/testdata/a_txn_ind13.dbf";
    set newname for datafile 133 to "/u1/TEST/testora/testdata/a_txn_ind14.dbf";
    set newname for datafile 134 to "/u1/TEST/testora/testdata/a_txn_ind15.dbf";
    set newname for datafile 135 to "/u1/TEST/testora/testdata/a_txn_ind16.dbf";
    set newname for datafile 136 to "/u1/TEST/testora/testdata/a_txn_ind17.dbf";
    set newname for datafile 137 to "/u1/TEST/testora/testdata/a_txn_ind18.dbf";
    set newname for datafile 138 to "/u1/TEST/testora/testdata/a_txn_ind19.dbf";
    set newname for datafile 139 to "/u1/TEST/testora/testdata/a_txn_ind20.dbf";
    set newname for datafile 140 to "/u1/TEST/testora/testdata/a_txn_ind21.dbf";
    set newname for datafile 141 to "/u1/TEST/testora/testdata/a_txn_ind22.dbf";
    set newname for datafile 142 to "/u1/TEST/testora/testdata/a_txn_ind23.dbf";
    set newname for datafile 143 to "/u1/TEST/testora/testdata/a_txn_ind24.dbf";
    set newname for datafile 144 to "/u1/TEST/testora/testdata/a_txn_ind25.dbf";
    set newname for datafile 145 to "/u1/TEST/testora/testdata/a_txn_ind26.dbf";
    set newname for datafile 146 to "/u1/TEST/testora/testdata/a_txn_ind27.dbf";
    set newname for datafile 147 to "/u1/TEST/testora/testdata/a_txn_ind28.dbf";
    set newname for datafile 148 to "/u1/TEST/testora/testdata/a_txn_ind29.dbf";
    set newname for datafile 149 to "/u1/TEST/testora/testdata/a_txn_ind30.dbf";
    set newname for datafile 150 to "/u1/TEST/testora/testdata/a_txn_ind31.dbf";
    set newname for datafile 151 to "/u1/TEST/testora/testdata/a_txn_ind32.dbf";
    set newname for datafile 152 to "/u1/TEST/testora/testdata/a_txn_ind33.dbf";
    set newname for datafile 153 to "/u1/TEST/testora/testdata/a_txn_ind34.dbf";
    set newname for datafile 154 to "/u1/TEST/testora/testdata/a_txn_ind35.dbf";
    set newname for datafile 155 to "/u1/TEST/testora/testdata/a_txn_ind36.dbf";
    set newname for datafile 156 to "/u1/TEST/testora/testdata/a_txn_ind37.dbf";
    set newname for datafile 157 to "/u1/TEST/testora/testdata/a_txn_ind38.dbf";
    set newname for datafile 158 to "/u1/TEST/testora/testdata/a_txn_ind39.dbf";
    set newname for datafile 159 to "/u1/TEST/testora/testdata/a_txn_ind40.dbf";
    set newname for datafile 160 to "/u1/TEST/testora/testdata/a_txn_ind41.dbf";
    set newname for datafile 161 to "/u1/TEST/testora/testdata/a_txn_ind42.dbf";
    set newname for datafile 162 to "/u1/TEST/testora/testdata/a_txn_ind43.dbf";
    set newname for datafile 163 to "/u1/TEST/testora/testdata/a_txn_ind44.dbf";
    set newname for datafile 164 to "/u1/TEST/testora/testdata/a_txn_ind45.dbf";
    set newname for datafile 165 to "/u1/TEST/testora/testdata/a_txn_ind46.dbf";
    set newname for datafile 166 to "/u1/TEST/testora/testdata/a_txn_ind47.dbf";
    set newname for datafile 167 to "/u1/TEST/testora/testdata/a_txn_ind48.dbf";
    set newname for datafile 168 to "/u1/TEST/testora/testdata/a_txn_ind49.dbf";
    set newname for datafile 169 to "/u1/TEST/testora/testdata/a_txn_ind50.dbf";
    set newname for datafile 170 to "/u1/TEST/testora/testdata/a_txn_ind51.dbf";
    set newname for datafile 171 to "/u1/TEST/testora/testdata/a_txn_ind52.dbf";
    set newname for datafile 172 to "/u1/TEST/testora/testdata/a_txn_ind53.dbf";
    set newname for datafile 173 to "/u1/TEST/testora/testdata/a_txn_ind54.dbf";
    set newname for datafile 174 to "/u1/TEST/testora/testdata/a_txn_ind55.dbf";
    set newname for datafile 175 to "/u1/TEST/testora/testdata/ctxd01.dbf";
    set newname for datafile 176 to "/u1/TEST/testora/testdata/odm.dbf";
    set newname for datafile 177 to "/u1/TEST/testora/testdata/olap.dbf";
    set newname for datafile 178 to "/u1/TEST/testora/testdata/owad01.dbf";
    set newname for datafile 179 to "/u1/TEST/testora/testdata/portal01.dbf";
    set newname for datafile 180 to "/u1/TEST/testora/testdata/statspack_01.dbf";
    set newname for datafile 181 to "/u1/TEST/testora/testdata/tplcux_data_01.dbf";
    set newname for datafile 182 to "/u1/TEST/testora/testdata/tplcux_idx_01.dbf";
    set newname for datafile 183 to "/u1/TEST/testora/testdata/interim.dbf";
    set newname for datafile 184 to "/u1/TEST/testora/testdata/system12.dbf";
    set newname for datafile 185 to "/u1/TEST/testora/testdata/a_txn_data49.dbf";
    set newname for datafile 186 to "/u1/TEST/testora/testdata/a_ref03.dbf";
    set newname for datafile 187 to "/u1/TEST/testora/testdata/a_summ06.dbf";
    set newname for datafile 188 to "/u1/TEST/testora/testdata/undo04.dbf";

run recover rman script
    
    RMAN> run {
    set newname for datafile 1 to "/u1/TEST/testora/testdata/system01.dbf";
    set newname for datafile 2 to "/u1/TEST/testora/testdata/system02.dbf";
    set newname for datafile 3 to "/u1/TEST/testora/testdata/system03.dbf";
    set newname for datafile 4 to "/u1/TEST/testora/testdata/system04.dbf";
    set newname for datafile 5 to "/u1/TEST/testora/testdata/system05.dbf";
    set newname for datafile 6 to "/u1/TEST/testora/testdata/system06.dbf";
    set newname for datafile 7 to "/u1/TEST/testora/testdata/system07.dbf";
    set newname for datafile 8 to "/u1/TEST/testora/testdata/system08.dbf";
    set newname for datafile 9 to "/u1/TEST/testora/testdata/system09.dbf";
    set newname for datafile 10 to "/u1/TEST/testora/testdata/system10.dbf";
    set newname for datafile 11 to "/u1/TEST/testora/testdata/system11.dbf";
    set newname for datafile 12 to "/u1/TEST/testora/testdata/sysaux01.dbf";
    set newname for datafile 13 to "/u1/TEST/testora/testdata/undo01.dbf";
    set newname for datafile 14 to "/u1/TEST/testora/testdata/undo02.dbf";
    set newname for datafile 15 to "/u1/TEST/testora/testdata/undo03.dbf";
    set newname for datafile 16 to "/u1/TEST/testora/testdata/a_archive01.dbf";
    set newname for datafile 17 to "/u1/TEST/testora/testdata/a_archive02.dbf";
    set newname for datafile 18 to "/u1/TEST/testora/testdata/a_archive03.dbf";
    set newname for datafile 19 to "/u1/TEST/testora/testdata/a_archive04.dbf";
    set newname for datafile 20 to "/u1/TEST/testora/testdata/a_archive05.dbf";
    set newname for datafile 21 to "/u1/TEST/testora/testdata/a_int01.dbf";
    set newname for datafile 22 to "/u1/TEST/testora/testdata/a_int02.dbf";
    set newname for datafile 23 to "/u1/TEST/testora/testdata/a_int03.dbf";
    set newname for datafile 24 to "/u1/TEST/testora/testdata/a_int04.dbf";
    set newname for datafile 25 to "/u1/TEST/testora/testdata/a_int05.dbf";
    set newname for datafile 26 to "/u1/TEST/testora/testdata/a_int06.dbf";
    set newname for datafile 27 to "/u1/TEST/testora/testdata/a_int07.dbf";
    set newname for datafile 28 to "/u1/TEST/testora/testdata/a_int08.dbf";
    set newname for datafile 29 to "/u1/TEST/testora/testdata/a_media01.dbf";
    set newname for datafile 30 to "/u1/TEST/testora/testdata/a_media02.dbf";
    set newname for datafile 31 to "/u1/TEST/testora/testdata/a_media03.dbf";
    set newname for datafile 32 to "/u1/TEST/testora/testdata/a_media04.dbf";
    set newname for datafile 33 to "/u1/TEST/testora/testdata/a_media05.dbf";
    set newname for datafile 34 to "/u1/TEST/testora/testdata/a_media06.dbf";
    set newname for datafile 35 to "/u1/TEST/testora/testdata/a_media07.dbf";
    set newname for datafile 36 to "/u1/TEST/testora/testdata/a_media08.dbf";
    set newname for datafile 37 to "/u1/TEST/testora/testdata/a_media09.dbf";
    set newname for datafile 38 to "/u1/TEST/testora/testdata/a_media10.dbf";
    set newname for datafile 39 to "/u1/TEST/testora/testdata/a_nolog01.dbf";
    set newname for datafile 40 to "/u1/TEST/testora/testdata/a_queue01.dbf";
    set newname for datafile 41 to "/u1/TEST/testora/testdata/a_queue02.dbf";
    set newname for datafile 42 to "/u1/TEST/testora/testdata/a_queue03.dbf";
    set newname for datafile 43 to "/u1/TEST/testora/testdata/a_queue04.dbf";
    set newname for datafile 44 to "/u1/TEST/testora/testdata/a_queue05.dbf";
    set newname for datafile 45 to "/u1/TEST/testora/testdata/a_queue06.dbf";
    set newname for datafile 46 to "/u1/TEST/testora/testdata/a_queue07.dbf";
    set newname for datafile 47 to "/u1/TEST/testora/testdata/a_queue08.dbf";
    set newname for datafile 48 to "/u1/TEST/testora/testdata/a_queue09.dbf";
    set newname for datafile 49 to "/u1/TEST/testora/testdata/a_queue10.dbf";
    set newname for datafile 50 to "/u1/TEST/testora/testdata/a_queue11.dbf";
    set newname for datafile 51 to "/u1/TEST/testora/testdata/a_queue12.dbf";
    set newname for datafile 52 to "/u1/TEST/testora/testdata/a_queue13.dbf";
    set newname for datafile 53 to "/u1/TEST/testora/testdata/a_queue14.dbf";
    set newname for datafile 54 to "/u1/TEST/testora/testdata/a_queue15.dbf";
    set newname for datafile 55 to "/u1/TEST/testora/testdata/a_queue16.dbf";
    set newname for datafile 56 to "/u1/TEST/testora/testdata/a_queue17.dbf";
    set newname for datafile 57 to "/u1/TEST/testora/testdata/a_queue18.dbf";
    set newname for datafile 58 to "/u1/TEST/testora/testdata/a_queue19.dbf";
    set newname for datafile 59 to "/u1/TEST/testora/testdata/a_queue20.dbf";
    set newname for datafile 60 to "/u1/TEST/testora/testdata/a_queue21.dbf";
    set newname for datafile 61 to "/u1/TEST/testora/testdata/a_queue22.dbf";
    set newname for datafile 62 to "/u1/TEST/testora/testdata/a_queue23.dbf";
    set newname for datafile 63 to "/u1/TEST/testora/testdata/a_queue24.dbf";
    set newname for datafile 64 to "/u1/TEST/testora/testdata/a_queue25.dbf";
    set newname for datafile 65 to "/u1/TEST/testora/testdata/a_ref01.dbf";
    set newname for datafile 66 to "/u1/TEST/testora/testdata/a_ref02.dbf";
    set newname for datafile 67 to "/u1/TEST/testora/testdata/a_summ01.dbf";
    set newname for datafile 68 to "/u1/TEST/testora/testdata/a_summ02.dbf";
    set newname for datafile 69 to "/u1/TEST/testora/testdata/a_summ03.dbf";
    set newname for datafile 70 to "/u1/TEST/testora/testdata/a_summ04.dbf";
    set newname for datafile 71 to "/u1/TEST/testora/testdata/a_summ05.dbf";
    set newname for datafile 72 to "/u1/TEST/testora/testdata/a_tools01.dbf";
    set newname for datafile 73 to "/u1/TEST/testora/testdata/a_txn_data01.dbf";
    set newname for datafile 74 to "/u1/TEST/testora/testdata/a_txn_data02.dbf";
    set newname for datafile 75 to "/u1/TEST/testora/testdata/a_txn_data03.dbf";
    set newname for datafile 76 to "/u1/TEST/testora/testdata/a_txn_data04.dbf";
    set newname for datafile 77 to "/u1/TEST/testora/testdata/a_txn_data05.dbf";
    set newname for datafile 78 to "/u1/TEST/testora/testdata/a_txn_data06.dbf";
    set newname for datafile 79 to "/u1/TEST/testora/testdata/a_txn_data07.dbf";
    set newname for datafile 80 to "/u1/TEST/testora/testdata/a_txn_data08.dbf";
    set newname for datafile 81 to "/u1/TEST/testora/testdata/a_txn_data09.dbf";
    set newname for datafile 82 to "/u1/TEST/testora/testdata/a_txn_data10.dbf";
    set newname for datafile 83 to "/u1/TEST/testora/testdata/a_txn_data11.dbf";
    set newname for datafile 84 to "/u1/TEST/testora/testdata/a_txn_data12.dbf";
    set newname for datafile 85 to "/u1/TEST/testora/testdata/a_txn_data13.dbf";
    set newname for datafile 86 to "/u1/TEST/testora/testdata/a_txn_data14.dbf";
    set newname for datafile 87 to "/u1/TEST/testora/testdata/a_txn_data15.dbf";
    set newname for datafile 88 to "/u1/TEST/testora/testdata/a_txn_data16.dbf";
    set newname for datafile 89 to "/u1/TEST/testora/testdata/a_txn_data17.dbf";
    set newname for datafile 90 to "/u1/TEST/testora/testdata/a_txn_data18.dbf";
    set newname for datafile 91 to "/u1/TEST/testora/testdata/a_txn_data19.dbf";
    set newname for datafile 92 to "/u1/TEST/testora/testdata/a_txn_data20.dbf";
    set newname for datafile 93 to "/u1/TEST/testora/testdata/a_txn_data21.dbf";
    set newname for datafile 94 to "/u1/TEST/testora/testdata/a_txn_data22.dbf";
    set newname for datafile 95 to "/u1/TEST/testora/testdata/a_txn_data23.dbf";
    set newname for datafile 96 to "/u1/TEST/testora/testdata/a_txn_data24.dbf";
    set newname for datafile 97 to "/u1/TEST/testora/testdata/a_txn_data25.dbf";
    set newname for datafile 98 to "/u1/TEST/testora/testdata/a_txn_data26.dbf";
    set newname for datafile 99 to "/u1/TEST/testora/testdata/a_txn_data28.dbf";
    set newname for datafile 100 to "/u1/TEST/testora/testdata/a_txn_data29.dbf";
    set newname for datafile 101 to "/u1/TEST/testora/testdata/a_txn_data30.dbf";
    set newname for datafile 102 to "/u1/TEST/testora/testdata/a_txn_data31.dbf";
    set newname for datafile 103 to "/u1/TEST/testora/testdata/a_txn_data32.dbf";
    set newname for datafile 104 to "/u1/TEST/testora/testdata/a_txn_data33.dbf";
    set newname for datafile 105 to "/u1/TEST/testora/testdata/a_txn_data34.dbf";
    set newname for datafile 106 to "/u1/TEST/testora/testdata/a_txn_data35.dbf";
    set newname for datafile 107 to "/u1/TEST/testora/testdata/a_txn_data36.dbf";
    set newname for datafile 108 to "/u1/TEST/testora/testdata/a_txn_data37.dbf";
    set newname for datafile 109 to "/u1/TEST/testora/testdata/a_txn_data38.dbf";
    set newname for datafile 110 to "/u1/TEST/testora/testdata/a_txn_data39.dbf";
    set newname for datafile 111 to "/u1/TEST/testora/testdata/a_txn_data40.dbf";
    set newname for datafile 112 to "/u1/TEST/testora/testdata/a_txn_data41.dbf";
    set newname for datafile 113 to "/u1/TEST/testora/testdata/a_txn_data42.dbf";
    set newname for datafile 114 to "/u1/TEST/testora/testdata/a_txn_data43.dbf";
    set newname for datafile 115 to "/u1/TEST/testora/testdata/a_txn_data44.dbf";
    set newname for datafile 116 to "/u1/TEST/testora/testdata/a_txn_data45.dbf";
    set newname for datafile 117 to "/u1/TEST/testora/testdata/a_txn_data46.dbf";
    set newname for datafile 118 to "/u1/TEST/testora/testdata/a_txn_data47.dbf";
    set newname for datafile 119 to "/u1/TEST/testora/testdata/a_txn_data48.dbf";
    set newname for datafile 120 to "/u1/TEST/testora/testdata/a_txn_ind01.dbf";
    set newname for datafile 121 to "/u1/TEST/testora/testdata/a_txn_ind02.dbf";
    set newname for datafile 122 to "/u1/TEST/testora/testdata/a_txn_ind03.dbf";
    set newname for datafile 123 to "/u1/TEST/testora/testdata/a_txn_ind04.dbf";
    set newname for datafile 124 to "/u1/TEST/testora/testdata/a_txn_ind05.dbf";
    set newname for datafile 125 to "/u1/TEST/testora/testdata/a_txn_ind06.dbf";
    set newname for datafile 126 to "/u1/TEST/testora/testdata/a_txn_ind07.dbf";
    set newname for datafile 127 to "/u1/TEST/testora/testdata/a_txn_ind08.dbf";
    set newname for datafile 128 to "/u1/TEST/testora/testdata/a_txn_ind09.dbf";
    set newname for datafile 129 to "/u1/TEST/testora/testdata/a_txn_ind10.dbf";
    set newname for datafile 130 to "/u1/TEST/testora/testdata/a_txn_ind11.dbf";
    set newname for datafile 131 to "/u1/TEST/testora/testdata/a_txn_ind12.dbf";
    set newname for datafile 132 to "/u1/TEST/testora/testdata/a_txn_ind13.dbf";
    set newname for datafile 133 to "/u1/TEST/testora/testdata/a_txn_ind14.dbf";
    set newname for datafile 134 to "/u1/TEST/testora/testdata/a_txn_ind15.dbf";
    set newname for datafile 135 to "/u1/TEST/testora/testdata/a_txn_ind16.dbf";
    set newname for datafile 136 to "/u1/TEST/testora/testdata/a_txn_ind17.dbf";
    set newname for datafile 137 to "/u1/TEST/testora/testdata/a_txn_ind18.dbf";
    set newname for datafile 138 to "/u1/TEST/testora/testdata/a_txn_ind19.dbf";
    set newname for datafile 139 to "/u1/TEST/testora/testdata/a_txn_ind20.dbf";
    set newname for datafile 140 to "/u1/TEST/testora/testdata/a_txn_ind21.dbf";
    set newname for datafile 141 to "/u1/TEST/testora/testdata/a_txn_ind22.dbf";
    set newname for datafile 142 to "/u1/TEST/testora/testdata/a_txn_ind23.dbf";
    set newname for datafile 143 to "/u1/TEST/testora/testdata/a_txn_ind24.dbf";
    set newname for datafile 144 to "/u1/TEST/testora/testdata/a_txn_ind25.dbf";
    set newname for datafile 145 to "/u1/TEST/testora/testdata/a_txn_ind26.dbf";
    set newname for datafile 146 to "/u1/TEST/testora/testdata/a_txn_ind27.dbf";
    set newname for datafile 147 to "/u1/TEST/testora/testdata/a_txn_ind28.dbf";
    set newname for datafile 148 to "/u1/TEST/testora/testdata/a_txn_ind29.dbf";
    set newname for datafile 149 to "/u1/TEST/testora/testdata/a_txn_ind30.dbf";
    set newname for datafile 150 to "/u1/TEST/testora/testdata/a_txn_ind31.dbf";
    set newname for datafile 151 to "/u1/TEST/testora/testdata/a_txn_ind32.dbf";
    set newname for datafile 152 to "/u1/TEST/testora/testdata/a_txn_ind33.dbf";
    set newname for datafile 153 to "/u1/TEST/testora/testdata/a_txn_ind34.dbf";
    set newname for datafile 154 to "/u1/TEST/testora/testdata/a_txn_ind35.dbf";
    set newname for datafile 155 to "/u1/TEST/testora/testdata/a_txn_ind36.dbf";
    set newname for datafile 156 to "/u1/TEST/testora/testdata/a_txn_ind37.dbf";
    set newname for datafile 157 to "/u1/TEST/testora/testdata/a_txn_ind38.dbf";
    set newname for datafile 158 to "/u1/TEST/testora/testdata/a_txn_ind39.dbf";
    set newname for datafile 159 to "/u1/TEST/testora/testdata/a_txn_ind40.dbf";
    set newname for datafile 160 to "/u1/TEST/testora/testdata/a_txn_ind41.dbf";
    set newname for datafile 161 to "/u1/TEST/testora/testdata/a_txn_ind42.dbf";
    set newname for datafile 162 to "/u1/TEST/testora/testdata/a_txn_ind43.dbf";
    set newname for datafile 163 to "/u1/TEST/testora/testdata/a_txn_ind44.dbf";
    set newname for datafile 164 to "/u1/TEST/testora/testdata/a_txn_ind45.dbf";
    set newname for datafile 165 to "/u1/TEST/testora/testdata/a_txn_ind46.dbf";
    set newname for datafile 166 to "/u1/TEST/testora/testdata/a_txn_ind47.dbf";
    set newname for datafile 167 to "/u1/TEST/testora/testdata/a_txn_ind48.dbf";
    set newname for datafile 168 to "/u1/TEST/testora/testdata/a_txn_ind49.dbf";
    set newname for datafile 169 to "/u1/TEST/testora/testdata/a_txn_ind50.dbf";
    set newname for datafile 170 to "/u1/TEST/testora/testdata/a_txn_ind51.dbf";
    set newname for datafile 171 to "/u1/TEST/testora/testdata/a_txn_ind52.dbf";
    set newname for datafile 172 to "/u1/TEST/testora/testdata/a_txn_ind53.dbf";
    set newname for datafile 173 to "/u1/TEST/testora/testdata/a_txn_ind54.dbf";
    set newname for datafile 174 to "/u1/TEST/testora/testdata/a_txn_ind55.dbf";
    set newname for datafile 175 to "/u1/TEST/testora/testdata/ctxd01.dbf";
    set newname for datafile 176 to "/u1/TEST/testora/testdata/odm.dbf";
    set newname for datafile 177 to "/u1/TEST/testora/testdata/olap.dbf";
    set newname for datafile 178 to "/u1/TEST/testora/testdata/owad01.dbf";
    set newname for datafile 179 to "/u1/TEST/testora/testdata/portal01.dbf";
    set newname for datafile 180 to "/u1/TEST/testora/testdata/statspack_01.dbf";
    set newname for datafile 181 to "/u1/TEST/testora/testdata/tplcux_data_01.dbf";
    set newname for datafile 182 to "/u1/TEST/testora/testdata/tplcux_idx_01.dbf";
    set newname for datafile 183 to "/u1/TEST/testora/testdata/interim.dbf";
    set newname for datafile 184 to "/u1/TEST/testora/testdata/system12.dbf";
    set newname for datafile 185 to "/u1/TEST/testora/testdata/a_txn_data49.dbf";
    set newname for datafile 186 to "/u1/TEST/testora/testdata/a_ref03.dbf";
    set newname for datafile 187 to "/u1/TEST/testora/testdata/a_summ06.dbf";
    set newname for datafile 188 to "/u1/TEST/testora/testdata/undo04.dbf";
    restore database;
    switch datafile all;
    recover database;
    }
    
###power off failure （中间遇电路检修，短暂停电）
    
    [testora@target testora]$ du -sh testdata  
    205G	testdata
    
    [testora@target testora]$ ll -rst testdata/  
    total 214433112
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 14:54 olap.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 14:54 a_queue25.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 14:54 odm.dbf
     6144012 -rw-r-----. 1 testora dba  6291464192 Oct 17 14:55 undo04.dbf
      204812 -rw-r-----. 1 testora dba   209723392 Oct 17 14:55 interim.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 14:56 a_txn_ind32.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 14:56 a_int07.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 14:56 undo01.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 14:56 a_queue10.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 14:57 a_txn_ind41.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 14:57 a_txn_data41.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 14:57 a_txn_data01.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 14:57 a_queue11.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 14:58 a_txn_ind42.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 14:58 a_txn_data42.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 14:58 a_txn_data02.dbf
       40972 -rw-r-----. 1 testora dba    41951232 Oct 17 14:58 ctxd01.dbf
       10252 -rw-r-----. 1 testora dba    10493952 Oct 17 14:58 owad01.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 14:58 portal01.dbf
    23068684 -rw-r-----. 1 testora dba 23622328320 Oct 17 15:01 a_txn_data49.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:01 a_queue12.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:02 a_txn_ind43.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:03 a_txn_data43.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:03 a_txn_data03.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:03 a_queue13.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:03 a_txn_ind44.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:04 a_txn_data44.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:04 a_txn_data04.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:04 a_queue14.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:05 a_txn_ind45.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:05 a_txn_data45.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:05 a_txn_data05.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:05 a_queue15.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:06 a_txn_ind46.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:06 a_txn_data46.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:06 a_txn_data06.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:06 a_queue16.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:07 a_txn_ind47.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:08 a_txn_data47.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:08 a_txn_data07.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:08 a_queue17.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:08 a_txn_ind48.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:09 a_txn_data48.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:09 a_txn_data08.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:09 a_queue18.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:10 a_txn_ind49.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:10 a_txn_ind01.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:10 a_txn_data09.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:10 a_queue19.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:11 a_txn_ind50.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:11 a_txn_ind02.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:11 a_txn_data10.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:11 a_queue20.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:12 a_txn_ind51.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:12 a_txn_ind03.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:12 a_txn_data11.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:12 a_queue21.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:13 a_txn_ind52.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:13 a_txn_ind04.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:13 a_txn_data12.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:13 a_queue22.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:14 a_txn_ind53.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:14 a_txn_ind05.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:14 a_txn_data13.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:14 a_queue23.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:15 a_txn_ind54.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:15 a_txn_ind06.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:15 a_txn_data14.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:15 a_queue09.dbf
      204812 -rw-r-----. 1 testora dba   209723392 Oct 17 15:16 a_media03.dbf
      204812 -rw-r-----. 1 testora dba   209723392 Oct 17 15:16 a_media04.dbf
     5242892 -rw-r-----. 1 testora dba  5368717312 Oct 17 15:16 system12.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:16 a_queue24.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:17 a_txn_ind55.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:17 a_txn_ind07.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:17 a_txn_data15.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:17 a_queue01.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:18 a_txn_ind33.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:18 a_int08.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:18 undo02.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:18 a_queue02.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:18 a_summ01.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:18 a_txn_ind34.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:19 undo03.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:19 a_queue03.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:19 a_txn_ind35.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:20 a_int01.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:20 a_txn_data35.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:20 a_queue04.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:20 a_txn_ind36.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:21 a_int02.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:21 a_txn_data36.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:21 a_queue06.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:21 a_txn_ind38.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:22 a_int04.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:22 a_txn_data38.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:22 a_queue05.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:22 a_txn_ind37.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:23 a_int03.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:23 a_txn_data37.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:23 a_queue07.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:24 a_txn_ind39.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:24 a_int05.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:24 a_txn_data39.dbf
      102412 -rw-r-----. 1 testora dba   104865792 Oct 17 15:24 a_queue08.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:25 a_txn_ind40.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:25 a_int06.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:25 a_txn_data40.dbf
      204812 -rw-r-----. 1 testora dba   209723392 Oct 17 15:25 a_media05.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:26 a_txn_ind26.dbf
     1843212 -rw-r-----. 1 testora dba  1887444992 Oct 17 15:26 a_txn_ind19.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:26 a_txn_data29.dbf
      204812 -rw-r-----. 1 testora dba   209723392 Oct 17 15:26 a_media06.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:27 a_txn_ind27.dbf
     1843212 -rw-r-----. 1 testora dba  1887444992 Oct 17 15:27 a_txn_ind20.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:27 a_txn_data30.dbf
      204812 -rw-r-----. 1 testora dba   209723392 Oct 17 15:27 a_media07.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:28 a_txn_ind28.dbf
     1843212 -rw-r-----. 1 testora dba  1887444992 Oct 17 15:28 a_txn_ind21.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:28 a_txn_data31.dbf
      204812 -rw-r-----. 1 testora dba   209723392 Oct 17 15:28 a_media08.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:29 a_txn_ind29.dbf
     1843212 -rw-r-----. 1 testora dba  1887444992 Oct 17 15:29 a_txn_ind22.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:29 a_txn_data32.dbf
      204812 -rw-r-----. 1 testora dba   209723392 Oct 17 15:29 a_media09.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:30 a_txn_ind30.dbf
     1843212 -rw-r-----. 1 testora dba  1887444992 Oct 17 15:30 a_txn_ind23.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:30 a_txn_data33.dbf
      204812 -rw-r-----. 1 testora dba   209723392 Oct 17 15:30 a_media10.dbf
     1536012 -rw-r-----. 1 testora dba  1572872192 Oct 17 15:31 a_txn_ind31.dbf
     1843212 -rw-r-----. 1 testora dba  1887444992 Oct 17 15:31 a_txn_ind24.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:31 a_txn_data34.dbf
      307212 -rw-r-----. 1 testora dba   314580992 Oct 17 15:32 a_summ02.dbf
     1024012 -rw-r-----. 1 testora dba  1048584192 Oct 17 15:32 system02.dbf
     2048012 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:32 a_txn_ind09.dbf
     2097164 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:32 a_txn_data17.dbf
       18804 -rw-r-----. 1 testora dba    19251200 Oct 17 15:33 control01.ctl
       18804 -rw-r-----. 1 testora dba    19251200 Oct 17 15:33 control02.ctl
      233476 -rw-r-----. 1 testora dba  2097160192 Oct 17 15:33 a_txn_ind08.dbf
      233476 -rw-r-----. 1 testora dba  1048584192 Oct 17 15:33 system01.dbf
      235524 -rw-r-----. 1 testora dba   314580992 Oct 17 15:33 a_archive05.dbf
      234500 -rw-r-----. 1 testora dba  2147491840 Oct 17 15:33 a_txn_data16.dbf
    
    [testora@target testora]$ sqlplus  /nolog
    SQL*Plus: Release 11.2.0.3.0 Production on Thu Oct 17 17:05:35 2013

    Copyright (c) 1982, 2011, Oracle.  All rights reserved.

    SQL> conn /as sysdba
    Connected to an idle instance.
    SQL> startup mount;
    ORACLE instance started.

    Total System Global Area 5.1310E+10 bytes
    Fixed Size		    2240344 bytes
    Variable Size		 1.0066E+10 bytes
    Database Buffers	 4.1205E+10 bytes
    Redo Buffers		   36098048 bytes
    Database mounted.
    
### continue recovering

    RMAN> run {
    set newname for datafile 1 to "/u1/TEST/testora/testdata/system01.dbf";
    set newname for datafile 2 to "/u1/TEST/testora/testdata/system02.dbf";
    set newname for datafile 3 to "/u1/TEST/testora/testdata/system03.dbf";
    set newname for datafile 4 to "/u1/TEST/testora/testdata/system04.dbf";
    set newname for datafile 5 to "/u1/TEST/testora/testdata/system05.dbf";
    set newname for datafile 6 to "/u1/TEST/testora/testdata/system06.dbf";
    set newname for datafile 7 to "/u1/TEST/testora/testdata/system07.dbf";
    set newname for datafile 8 to "/u1/TEST/testora/testdata/system08.dbf";
    set newname for datafile 9 to "/u1/TEST/testora/testdata/system09.dbf";
    set newname for datafile 10 to "/u1/TEST/testora/testdata/system10.dbf";
    set newname for datafile 11 to "/u1/TEST/testora/testdata/system11.dbf";
    set newname for datafile 12 to "/u1/TEST/testora/testdata/sysaux01.dbf";
    set newname for datafile 13 to "/u1/TEST/testora/testdata/undo01.dbf";
    set newname for datafile 14 to "/u1/TEST/testora/testdata/undo02.dbf";
    set newname for datafile 15 to "/u1/TEST/testora/testdata/undo03.dbf";
    set newname for datafile 16 to "/u1/TEST/testora/testdata/a_archive01.dbf";
    set newname for datafile 17 to "/u1/TEST/testora/testdata/a_archive02.dbf";
    set newname for datafile 18 to "/u1/TEST/testora/testdata/a_archive03.dbf";
    set newname for datafile 19 to "/u1/TEST/testora/testdata/a_archive04.dbf";
    set newname for datafile 20 to "/u1/TEST/testora/testdata/a_archive05.dbf";
    set newname for datafile 21 to "/u1/TEST/testora/testdata/a_int01.dbf";
    set newname for datafile 22 to "/u1/TEST/testora/testdata/a_int02.dbf";
    set newname for datafile 23 to "/u1/TEST/testora/testdata/a_int03.dbf";
    set newname for datafile 24 to "/u1/TEST/testora/testdata/a_int04.dbf";
    set newname for datafile 25 to "/u1/TEST/testora/testdata/a_int05.dbf";
    set newname for datafile 26 to "/u1/TEST/testora/testdata/a_int06.dbf";
    set newname for datafile 27 to "/u1/TEST/testora/testdata/a_int07.dbf";
    set newname for datafile 28 to "/u1/TEST/testora/testdata/a_int08.dbf";
    set newname for datafile 29 to "/u1/TEST/testora/testdata/a_media01.dbf";
    set newname for datafile 30 to "/u1/TEST/testora/testdata/a_media02.dbf";
    set newname for datafile 31 to "/u1/TEST/testora/testdata/a_media03.dbf";
    set newname for datafile 32 to "/u1/TEST/testora/testdata/a_media04.dbf";
    set newname for datafile 33 to "/u1/TEST/testora/testdata/a_media05.dbf";
    set newname for datafile 34 to "/u1/TEST/testora/testdata/a_media06.dbf";
    set newname for datafile 35 to "/u1/TEST/testora/testdata/a_media07.dbf";
    set newname for datafile 36 to "/u1/TEST/testora/testdata/a_media08.dbf";
    set newname for datafile 37 to "/u1/TEST/testora/testdata/a_media09.dbf";
    set newname for datafile 38 to "/u1/TEST/testora/testdata/a_media10.dbf";
    set newname for datafile 39 to "/u1/TEST/testora/testdata/a_nolog01.dbf";
    set newname for datafile 40 to "/u1/TEST/testora/testdata/a_queue01.dbf";
    set newname for datafile 41 to "/u1/TEST/testora/testdata/a_queue02.dbf";
    set newname for datafile 42 to "/u1/TEST/testora/testdata/a_queue03.dbf";
    set newname for datafile 43 to "/u1/TEST/testora/testdata/a_queue04.dbf";
    set newname for datafile 44 to "/u1/TEST/testora/testdata/a_queue05.dbf";
    set newname for datafile 45 to "/u1/TEST/testora/testdata/a_queue06.dbf";
    set newname for datafile 46 to "/u1/TEST/testora/testdata/a_queue07.dbf";
    set newname for datafile 47 to "/u1/TEST/testora/testdata/a_queue08.dbf";
    set newname for datafile 48 to "/u1/TEST/testora/testdata/a_queue09.dbf";
    set newname for datafile 49 to "/u1/TEST/testora/testdata/a_queue10.dbf";
    set newname for datafile 50 to "/u1/TEST/testora/testdata/a_queue11.dbf";
    set newname for datafile 51 to "/u1/TEST/testora/testdata/a_queue12.dbf";
    set newname for datafile 52 to "/u1/TEST/testora/testdata/a_queue13.dbf";
    set newname for datafile 53 to "/u1/TEST/testora/testdata/a_queue14.dbf";
    set newname for datafile 54 to "/u1/TEST/testora/testdata/a_queue15.dbf";
    set newname for datafile 55 to "/u1/TEST/testora/testdata/a_queue16.dbf";
    set newname for datafile 56 to "/u1/TEST/testora/testdata/a_queue17.dbf";
    set newname for datafile 57 to "/u1/TEST/testora/testdata/a_queue18.dbf";
    set newname for datafile 58 to "/u1/TEST/testora/testdata/a_queue19.dbf";
    set newname for datafile 59 to "/u1/TEST/testora/testdata/a_queue20.dbf";
    set newname for datafile 60 to "/u1/TEST/testora/testdata/a_queue21.dbf";
    set newname for datafile 61 to "/u1/TEST/testora/testdata/a_queue22.dbf";
    set newname for datafile 62 to "/u1/TEST/testora/testdata/a_queue23.dbf";
    set newname for datafile 63 to "/u1/TEST/testora/testdata/a_queue24.dbf";
    set newname for datafile 64 to "/u1/TEST/testora/testdata/a_queue25.dbf";
    set newname for datafile 65 to "/u1/TEST/testora/testdata/a_ref01.dbf";
    set newname for datafile 66 to "/u1/TEST/testora/testdata/a_ref02.dbf";
    set newname for datafile 67 to "/u1/TEST/testora/testdata/a_summ01.dbf";
    set newname for datafile 68 to "/u1/TEST/testora/testdata/a_summ02.dbf";
    set newname for datafile 69 to "/u1/TEST/testora/testdata/a_summ03.dbf";
    set newname for datafile 70 to "/u1/TEST/testora/testdata/a_summ04.dbf";
    set newname for datafile 71 to "/u1/TEST/testora/testdata/a_summ05.dbf";
    set newname for datafile 72 to "/u1/TEST/testora/testdata/a_tools01.dbf";
    set newname for datafile 73 to "/u1/TEST/testora/testdata/a_txn_data01.dbf";
    set newname for datafile 74 to "/u1/TEST/testora/testdata/a_txn_data02.dbf";
    set newname for datafile 75 to "/u1/TEST/testora/testdata/a_txn_data03.dbf";
    set newname for datafile 76 to "/u1/TEST/testora/testdata/a_txn_data04.dbf";
    set newname for datafile 77 to "/u1/TEST/testora/testdata/a_txn_data05.dbf";
    set newname for datafile 78 to "/u1/TEST/testora/testdata/a_txn_data06.dbf";
    set newname for datafile 79 to "/u1/TEST/testora/testdata/a_txn_data07.dbf";
    set newname for datafile 80 to "/u1/TEST/testora/testdata/a_txn_data08.dbf";
    set newname for datafile 81 to "/u1/TEST/testora/testdata/a_txn_data09.dbf";
    set newname for datafile 82 to "/u1/TEST/testora/testdata/a_txn_data10.dbf";
    set newname for datafile 83 to "/u1/TEST/testora/testdata/a_txn_data11.dbf";
    set newname for datafile 84 to "/u1/TEST/testora/testdata/a_txn_data12.dbf";
    set newname for datafile 85 to "/u1/TEST/testora/testdata/a_txn_data13.dbf";
    set newname for datafile 86 to "/u1/TEST/testora/testdata/a_txn_data14.dbf";
    set newname for datafile 87 to "/u1/TEST/testora/testdata/a_txn_data15.dbf";
    set newname for datafile 88 to "/u1/TEST/testora/testdata/a_txn_data16.dbf";
    set newname for datafile 89 to "/u1/TEST/testora/testdata/a_txn_data17.dbf";
    set newname for datafile 90 to "/u1/TEST/testora/testdata/a_txn_data18.dbf";
    set newname for datafile 91 to "/u1/TEST/testora/testdata/a_txn_data19.dbf";
    set newname for datafile 92 to "/u1/TEST/testora/testdata/a_txn_data20.dbf";
    set newname for datafile 93 to "/u1/TEST/testora/testdata/a_txn_data21.dbf";
    set newname for datafile 94 to "/u1/TEST/testora/testdata/a_txn_data22.dbf";
    set newname for datafile 95 to "/u1/TEST/testora/testdata/a_txn_data23.dbf";
    set newname for datafile 96 to "/u1/TEST/testora/testdata/a_txn_data24.dbf";
    set newname for datafile 97 to "/u1/TEST/testora/testdata/a_txn_data25.dbf";
    set newname for datafile 98 to "/u1/TEST/testora/testdata/a_txn_data26.dbf";
    set newname for datafile 99 to "/u1/TEST/testora/testdata/a_txn_data28.dbf";
    set newname for datafile 100 to "/u1/TEST/testora/testdata/a_txn_data29.dbf";
    set newname for datafile 101 to "/u1/TEST/testora/testdata/a_txn_data30.dbf";
    set newname for datafile 102 to "/u1/TEST/testora/testdata/a_txn_data31.dbf";
    set newname for datafile 103 to "/u1/TEST/testora/testdata/a_txn_data32.dbf";
    set newname for datafile 104 to "/u1/TEST/testora/testdata/a_txn_data33.dbf";
    set newname for datafile 105 to "/u1/TEST/testora/testdata/a_txn_data34.dbf";
    set newname for datafile 106 to "/u1/TEST/testora/testdata/a_txn_data35.dbf";
    set newname for datafile 107 to "/u1/TEST/testora/testdata/a_txn_data36.dbf";
    set newname for datafile 108 to "/u1/TEST/testora/testdata/a_txn_data37.dbf";
    set newname for datafile 109 to "/u1/TEST/testora/testdata/a_txn_data38.dbf";
    set newname for datafile 110 to "/u1/TEST/testora/testdata/a_txn_data39.dbf";
    set newname for datafile 111 to "/u1/TEST/testora/testdata/a_txn_data40.dbf";
    set newname for datafile 112 to "/u1/TEST/testora/testdata/a_txn_data41.dbf";
    set newname for datafile 113 to "/u1/TEST/testora/testdata/a_txn_data42.dbf";
    set newname for datafile 114 to "/u1/TEST/testora/testdata/a_txn_data43.dbf";
    set newname for datafile 115 to "/u1/TEST/testora/testdata/a_txn_data44.dbf";
    set newname for datafile 116 to "/u1/TEST/testora/testdata/a_txn_data45.dbf";
    set newname for datafile 117 to "/u1/TEST/testora/testdata/a_txn_data46.dbf";
    set newname for datafile 118 to "/u1/TEST/testora/testdata/a_txn_data47.dbf";
    set newname for datafile 119 to "/u1/TEST/testora/testdata/a_txn_data48.dbf";
    set newname for datafile 120 to "/u1/TEST/testora/testdata/a_txn_ind01.dbf";
    set newname for datafile 121 to "/u1/TEST/testora/testdata/a_txn_ind02.dbf";
    set newname for datafile 122 to "/u1/TEST/testora/testdata/a_txn_ind03.dbf";
    set newname for datafile 123 to "/u1/TEST/testora/testdata/a_txn_ind04.dbf";
    set newname for datafile 124 to "/u1/TEST/testora/testdata/a_txn_ind05.dbf";
    set newname for datafile 125 to "/u1/TEST/testora/testdata/a_txn_ind06.dbf";
    set newname for datafile 126 to "/u1/TEST/testora/testdata/a_txn_ind07.dbf";
    set newname for datafile 127 to "/u1/TEST/testora/testdata/a_txn_ind08.dbf";
    set newname for datafile 128 to "/u1/TEST/testora/testdata/a_txn_ind09.dbf";
    set newname for datafile 129 to "/u1/TEST/testora/testdata/a_txn_ind10.dbf";
    set newname for datafile 130 to "/u1/TEST/testora/testdata/a_txn_ind11.dbf";
    set newname for datafile 131 to "/u1/TEST/testora/testdata/a_txn_ind12.dbf";
    set newname for datafile 132 to "/u1/TEST/testora/testdata/a_txn_ind13.dbf";
    set newname for datafile 133 to "/u1/TEST/testora/testdata/a_txn_ind14.dbf";
    set newname for datafile 134 to "/u1/TEST/testora/testdata/a_txn_ind15.dbf";
    set newname for datafile 135 to "/u1/TEST/testora/testdata/a_txn_ind16.dbf";
    set newname for datafile 136 to "/u1/TEST/testora/testdata/a_txn_ind17.dbf";
    set newname for datafile 137 to "/u1/TEST/testora/testdata/a_txn_ind18.dbf";
    set newname for datafile 138 to "/u1/TEST/testora/testdata/a_txn_ind19.dbf";
    set newname for datafile 139 to "/u1/TEST/testora/testdata/a_txn_ind20.dbf";
    set newname for datafile 140 to "/u1/TEST/testora/testdata/a_txn_ind21.dbf";
    set newname for datafile 141 to "/u1/TEST/testora/testdata/a_txn_ind22.dbf";
    set newname for datafile 142 to "/u1/TEST/testora/testdata/a_txn_ind23.dbf";
    set newname for datafile 143 to "/u1/TEST/testora/testdata/a_txn_ind24.dbf";
    set newname for datafile 144 to "/u1/TEST/testora/testdata/a_txn_ind25.dbf";
    set newname for datafile 145 to "/u1/TEST/testora/testdata/a_txn_ind26.dbf";
    set newname for datafile 146 to "/u1/TEST/testora/testdata/a_txn_ind27.dbf";
    set newname for datafile 147 to "/u1/TEST/testora/testdata/a_txn_ind28.dbf";
    set newname for datafile 148 to "/u1/TEST/testora/testdata/a_txn_ind29.dbf";
    set newname for datafile 149 to "/u1/TEST/testora/testdata/a_txn_ind30.dbf";
    set newname for datafile 150 to "/u1/TEST/testora/testdata/a_txn_ind31.dbf";
    set newname for datafile 151 to "/u1/TEST/testora/testdata/a_txn_ind32.dbf";
    set newname for datafile 152 to "/u1/TEST/testora/testdata/a_txn_ind33.dbf";
    set newname for datafile 153 to "/u1/TEST/testora/testdata/a_txn_ind34.dbf";
    set newname for datafile 154 to "/u1/TEST/testora/testdata/a_txn_ind35.dbf";
    set newname for datafile 155 to "/u1/TEST/testora/testdata/a_txn_ind36.dbf";
    set newname for datafile 156 to "/u1/TEST/testora/testdata/a_txn_ind37.dbf";
    set newname for datafile 157 to "/u1/TEST/testora/testdata/a_txn_ind38.dbf";
    set newname for datafile 158 to "/u1/TEST/testora/testdata/a_txn_ind39.dbf";
    set newname for datafile 159 to "/u1/TEST/testora/testdata/a_txn_ind40.dbf";
    set newname for datafile 160 to "/u1/TEST/testora/testdata/a_txn_ind41.dbf";
    set newname for datafile 161 to "/u1/TEST/testora/testdata/a_txn_ind42.dbf";
    set newname for datafile 162 to "/u1/TEST/testora/testdata/a_txn_ind43.dbf";
    set newname for datafile 163 to "/u1/TEST/testora/testdata/a_txn_ind44.dbf";
    set newname for datafile 164 to "/u1/TEST/testora/testdata/a_txn_ind45.dbf";
    set newname for datafile 165 to "/u1/TEST/testora/testdata/a_txn_ind46.dbf";
    set newname for datafile 166 to "/u1/TEST/testora/testdata/a_txn_ind47.dbf";
    set newname for datafile 167 to "/u1/TEST/testora/testdata/a_txn_ind48.dbf";
    set newname for datafile 168 to "/u1/TEST/testora/testdata/a_txn_ind49.dbf";
    set newname for datafile 169 to "/u1/TEST/testora/testdata/a_txn_ind50.dbf";
    set newname for datafile 170 to "/u1/TEST/testora/testdata/a_txn_ind51.dbf";
    set newname for datafile 171 to "/u1/TEST/testora/testdata/a_txn_ind52.dbf";
    set newname for datafile 172 to "/u1/TEST/testora/testdata/a_txn_ind53.dbf";
    set newname for datafile 173 to "/u1/TEST/testora/testdata/a_txn_ind54.dbf";
    set newname for datafile 174 to "/u1/TEST/testora/testdata/a_txn_ind55.dbf";
    set newname for datafile 175 to "/u1/TEST/testora/testdata/ctxd01.dbf";
    set newname for datafile 176 to "/u1/TEST/testora/testdata/odm.dbf";
    set newname for datafile 177 to "/u1/TEST/testora/testdata/olap.dbf";
    set newname for datafile 178 to "/u1/TEST/testora/testdata/owad01.dbf";
    set newname for datafile 179 to "/u1/TEST/testora/testdata/portal01.dbf";
    set newname for datafile 180 to "/u1/TEST/testora/testdata/statspack_01.dbf";
    set newname for datafile 181 to "/u1/TEST/testora/testdata/tplcux_data_01.dbf";
    set newname for datafile 182 to "/u1/TEST/testora/testdata/tplcux_idx_01.dbf";
    set newname for datafile 183 to "/u1/TEST/testora/testdata/interim.dbf";
    set newname for datafile 184 to "/u1/TEST/testora/testdata/system12.dbf";
    set newname for datafile 185 to "/u1/TEST/testora/testdata/a_txn_data49.dbf";
    set newname for datafile 186 to "/u1/TEST/testora/testdata/a_ref03.dbf";
    set newname for datafile 187 to "/u1/TEST/testora/testdata/a_summ06.dbf";
    set newname for datafile 188 to "/u1/TEST/testora/testdata/undo04.dbf";
    restore database;
    switch datafile all;
    recover database;
    }
    Starting restore at 17-OCT-13
    using target database control file instead of recovery catalog
    allocated channel: ORA_DISK_1
    channel ORA_DISK_1: SID=629 device type=DISK

    datafile 2 is already restored to file /u1/TEST/testora/testdata/system02.dbf
    ... ...
    datafile 188 is already restored to file /u1/TEST/testora/testdata/undo04.dbf
    channel ORA_DISK_1: starting datafile backup set restore
    channel ORA_DISK_1: specifying datafile(s) to restore from backup set
    channel ORA_DISK_1: restoring datafile 00001 to /u1/TEST/testora/testdata/system01.dbf
    channel ORA_DISK_1: restoring datafile 00020 to /u1/TEST/testora/testdata/a_archive05.dbf
    channel ORA_DISK_1: restoring datafile 00088 to /u1/TEST/testora/testdata/a_txn_data16.dbf
    channel ORA_DISK_1: restoring datafile 00127 to /u1/TEST/testora/testdata/a_txn_ind08.dbf
    channel ORA_DISK_1: reading from backup piece /data/backup/db_bak_lev0_829058166_1_318
    ... ...
    channel ORA_DISK_1: restore complete, elapsed time: 00:00:35
    Finished restore at 17-OCT-13
    
    datafile 1 switched to datafile copy
    input datafile copy RECID=190 STAMP=829070406 file name=/u1/TEST/testora/testdata/system01.dbf
    ... ...
    
    datafile 188 switched to datafile copy
    input datafile copy RECID=377 STAMP=829070448 file name=/u1/TEST/testora/testdata/undo04.dbf

    Starting recover at 17-OCT-13
    using channel ORA_DISK_1

    starting media recovery

    channel ORA_DISK_1: starting archived log restore to default destination
    channel ORA_DISK_1: restoring archived log
    archived log thread=2 sequence=88
    channel ORA_DISK_1: reading from backup piece /data/backup/archive_log_829058535_1_334
    channel ORA_DISK_1: piece handle=/data/backup/archive_log_829058535_1_334 tag=ARC_BAK
    channel ORA_DISK_1: restored backup piece 1
    channel ORA_DISK_1: restore complete, elapsed time: 00:00:03
    channel ORA_DISK_1: starting archived log restore to default destination
    channel ORA_DISK_1: restoring archived log
    archived log thread=1 sequence=1094
    channel ORA_DISK_1: restoring archived log
    archived log thread=1 sequence=1095
    channel ORA_DISK_1: restoring archived log
    archived log thread=2 sequence=89
    channel ORA_DISK_1: reading from backup piece /data/backup/archive_log_829058537_1_335
    channel ORA_DISK_1: piece handle=/data/backup/archive_log_829058537_1_335 tag=ARC_BAK
    channel ORA_DISK_1: restored backup piece 1
    channel ORA_DISK_1: restore complete, elapsed time: 00:00:01
    archived log file name=/u1/TEST/testora/archive/1_1094_828401849.dbf thread=1 sequence=1094
    archived log file name=/u1/TEST/testora/archive/2_88_828401849.dbf thread=2 sequence=88
    archived log file name=/u1/TEST/testora/archive/1_1095_828401849.dbf thread=1 sequence=1095
    archived log file name=/u1/TEST/testora/archive/2_89_828401849.dbf thread=2 sequence=89
    unable to find archived log
    archived log thread=1 sequence=1096
    RMAN-00571: ===========================================================
    RMAN-00569: =============== ERROR MESSAGE STACK FOLLOWS ===============
    RMAN-00571: ===========================================================
    RMAN-03002: failure of recover command at 10/17/2013 17:21:31
    RMAN-06054: media recovery requesting unknown archived log for thread 1 with sequence 1096 and starting SCN of 101987199
    
list backup of archivelog
    
    RMAN> list backup of archivelog all;


    List of Backup Sets
    ===================


    BS Key  Size       Device Type Elapsed Time Completion Time
    ------- ---------- ----------- ------------ ---------------
    330     156.45M    DISK        00:00:01     17-OCT-13      
            BP Key: 390   Status: AVAILABLE  Compressed: NO  Tag: ARC_BAK
            Piece Name: /data/backup/archive_log_829058535_1_334

      List of Archived Logs in backup set 330
      Thrd Seq     Low SCN    Low Time  Next SCN   Next Time
      ---- ------- ---------- --------- ---------- ---------
      1    1092    101805928  17-OCT-13 101861298  17-OCT-13
      1    1093    101861298  17-OCT-13 101914951  17-OCT-13
      2    87      101311879  17-OCT-13 101861641  17-OCT-13
      2    88      101861641  17-OCT-13 101987191  17-OCT-13

    BS Key  Size       Device Type Elapsed Time Completion Time
    ------- ---------- ----------- ------------ ---------------
    331     441.13M    DISK        00:00:02     17-OCT-13      
            BP Key: 391   Status: AVAILABLE  Compressed: NO  Tag: ARC_BAK
            Piece Name: /data/backup/archive_log_829058535_1_333

      List of Archived Logs in backup set 331
      Thrd Seq     Low SCN    Low Time  Next SCN   Next Time
      ---- ------- ---------- --------- ---------- ---------
      1    1091    101311755  17-OCT-13 101805928  17-OCT-13

    BS Key  Size       Device Type Elapsed Time Completion Time
    ------- ---------- ----------- ------------ ---------------
    332     27.28M     DISK        00:00:00     17-OCT-13      
            BP Key: 392   Status: AVAILABLE  Compressed: NO  Tag: ARC_BAK
            Piece Name: /data/backup/archive_log_829058537_1_335

      List of Archived Logs in backup set 332
      Thrd Seq     Low SCN    Low Time  Next SCN   Next Time
      ---- ------- ---------- --------- ---------- ---------
      1    1094    101914951  17-OCT-13 101987096  17-OCT-13
      1    1095    101987096  17-OCT-13 101987199  17-OCT-13
      2    89      101987191  17-OCT-13 101987202  17-OCT-13
    
datafile size
    
    [testora@target testora]$ du -sh testdata
    271G	testdata
    
###recreate controlfile

    [testora@target ~]$ export ORACLE_SID=PROD
    [testora@target ~]$ sqlplus  /nolog

    SQL*Plus: Release 11.2.0.3.0 Production on Thu Oct 17 11:09:21 2013

    Copyright (c) 1982, 2011, Oracle.  All rights reserved.

    SQL> conn /as sysdba
    Connected.
    SQL> alter database backup controlfile to trace;

    Database altered.

    SQL> show parameter user_dump

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    user_dump_dest			     string	 /u1/11gR2_BASE/admin/prod/diag
                             /rdbms/prod/PROD/trace
    SQL> exit
    Disconnected from Oracle Database 11g Enterprise Edition Release 11.2.0.3.0 - 64bit Production
    With the Partitioning, OLAP, Data Mining and Real Application Testing options
    
    [testora@target ~]$ ll -rst /u1/11gR2_BASE?admin/prod/diag/rdbms/prod/PROD/trace/ | tail
     3268 -rw-r--r--. 1 testora dba  3346203 Oct 17 10:51 PROD_m000_7617.trc
       12 -rw-r--r--. 1 testora dba     8760 Oct 17 11:01 PROD_dbw0_7573.trm
       72 -rw-r--r--. 1 testora dba    70015 Oct 17 11:01 PROD_dbw0_7573.trc
       84 -rw-r--r--. 1 testora dba    83406 Oct 17 11:01 PROD_ora_7609.trm
      476 -rw-r--r--. 1 testora dba   486962 Oct 17 11:01 PROD_ora_7609.trc
      652 -rw-r--r--. 1 testora dba   663569 Oct 17 11:01 PROD_m000_7779.trm
     4352 -rw-r--r--. 1 testora dba  4454728 Oct 17 11:01 PROD_m000_7779.trc
        4 -rw-r--r--. 1 testora dba      268 Oct 17 11:09 PROD_ora_7826.trm
       28 -rw-r--r--. 1 testora dba    26359 Oct 17 11:09 PROD_ora_7826.trc
      112 -rw-r--r--. 1 testora dba   107376 Oct 17 11:09 alert_PROD.log
      
    [testora@target ~]$ pwd
    /home/testora
    [testora@target ~]$ cp /u1/11gR2_BASE/admin/prod/diag/rdbms/prod/PROD/trace/PROD_ora_7826.trc .
    [testora@target ~]$ ls -l
    total 11952
    drwxr-xr-x. 10 testora dba     4096 Jun 21 17:12 itsection
    drwxr-xr-x.  3 testora dba     4096 May 31 00:43 oradiag_testora
    -rw-r--r--.  1 testora dba    26359 Oct 17 11:10 PROD_ora_7826.trc
    -rw-r--r--.  1 testora dba     1139 Jul 15 16:30 rdccs_m000_15683.out
    -rw-r--r--.  1 testora dba 12196573 Jul 15 16:28 rdccs_m000_15683.trc
    [testora@target ~]$ cp PROD_ora_7826.trc controlfile.sql
    
edit controlfile

    [testora@target ~]$ cat controlfile.sql 
    CREATE CONTROLFILE REUSE DATABASE "PROD" RESETLOGS  ARCHIVELOG
        MAXLOGFILES 16
        MAXLOGMEMBERS 2
        MAXDATAFILES 512
        MAXINSTANCES 63
        MAXLOGHISTORY 2920
    LOGFILE
      GROUP 1 (
        '/u1/TEST/testora/testdata/redo1_1.dbf',
        '/u1/TEST/testora/testdata/redo1_2.dbf'
      ) SIZE 500M BLOCKSIZE 512,
      GROUP 2 (
        '/u1/TEST/testora/testdata/redo2_1.dbf',
        '/u1/TEST/testora/testdata/redo2_2.dbf'
      ) SIZE 500M BLOCKSIZE 512,
      GROUP 3 (
        '/u1/TEST/testora/testdata/redo3_1.dbf',
        '/u1/TEST/testora/testdata/redo3_2.dbf'
      ) SIZE 500M BLOCKSIZE 512
    -- STANDBY LOGFILE
    DATAFILE
        '/u1/TEST/testora/testdata/system01.dbf',
        '/u1/TEST/testora/testdata/system02.dbf',
        '/u1/TEST/testora/testdata/system03.dbf',
        '/u1/TEST/testora/testdata/system04.dbf',
        '/u1/TEST/testora/testdata/system05.dbf',
        '/u1/TEST/testora/testdata/system06.dbf',
        '/u1/TEST/testora/testdata/system07.dbf',
        '/u1/TEST/testora/testdata/system08.dbf',
        '/u1/TEST/testora/testdata/system09.dbf',
        '/u1/TEST/testora/testdata/system10.dbf',
        '/u1/TEST/testora/testdata/system11.dbf',
        '/u1/TEST/testora/testdata/sysaux01.dbf',
        '/u1/TEST/testora/testdata/undo01.dbf',
        '/u1/TEST/testora/testdata/undo02.dbf',
        '/u1/TEST/testora/testdata/undo03.dbf',
        '/u1/TEST/testora/testdata/a_archive01.dbf',
        '/u1/TEST/testora/testdata/a_archive02.dbf',
        '/u1/TEST/testora/testdata/a_archive03.dbf',
        '/u1/TEST/testora/testdata/a_archive04.dbf',
        '/u1/TEST/testora/testdata/a_archive05.dbf',
        '/u1/TEST/testora/testdata/a_int01.dbf',
        '/u1/TEST/testora/testdata/a_int02.dbf',
        '/u1/TEST/testora/testdata/a_int03.dbf',
        '/u1/TEST/testora/testdata/a_int04.dbf',
        '/u1/TEST/testora/testdata/a_int05.dbf',
        '/u1/TEST/testora/testdata/a_int06.dbf',
        '/u1/TEST/testora/testdata/a_int07.dbf',
        '/u1/TEST/testora/testdata/a_int08.dbf',
        '/u1/TEST/testora/testdata/a_media01.dbf',
        '/u1/TEST/testora/testdata/a_media02.dbf',
        '/u1/TEST/testora/testdata/a_media03.dbf',
        '/u1/TEST/testora/testdata/a_media04.dbf',
        '/u1/TEST/testora/testdata/a_media05.dbf',
        '/u1/TEST/testora/testdata/a_media06.dbf',
        '/u1/TEST/testora/testdata/a_media07.dbf',
        '/u1/TEST/testora/testdata/a_media08.dbf',
        '/u1/TEST/testora/testdata/a_media09.dbf',
        '/u1/TEST/testora/testdata/a_media10.dbf',
        '/u1/TEST/testora/testdata/a_nolog01.dbf',
        '/u1/TEST/testora/testdata/a_queue01.dbf',
        '/u1/TEST/testora/testdata/a_queue02.dbf',
        '/u1/TEST/testora/testdata/a_queue03.dbf',
        '/u1/TEST/testora/testdata/a_queue04.dbf',
        '/u1/TEST/testora/testdata/a_queue05.dbf',
        '/u1/TEST/testora/testdata/a_queue06.dbf',
        '/u1/TEST/testora/testdata/a_queue07.dbf',
        '/u1/TEST/testora/testdata/a_queue08.dbf',
        '/u1/TEST/testora/testdata/a_queue09.dbf',
        '/u1/TEST/testora/testdata/a_queue10.dbf',
        '/u1/TEST/testora/testdata/a_queue11.dbf',
        '/u1/TEST/testora/testdata/a_queue12.dbf',
        '/u1/TEST/testora/testdata/a_queue13.dbf',
        '/u1/TEST/testora/testdata/a_queue14.dbf',
        '/u1/TEST/testora/testdata/a_queue15.dbf',
        '/u1/TEST/testora/testdata/a_queue16.dbf',
        '/u1/TEST/testora/testdata/a_queue17.dbf',
        '/u1/TEST/testora/testdata/a_queue18.dbf',
        '/u1/TEST/testora/testdata/a_queue19.dbf',
        '/u1/TEST/testora/testdata/a_queue20.dbf',
        '/u1/TEST/testora/testdata/a_queue21.dbf',
        '/u1/TEST/testora/testdata/a_queue22.dbf',
        '/u1/TEST/testora/testdata/a_queue23.dbf',
        '/u1/TEST/testora/testdata/a_queue24.dbf',
        '/u1/TEST/testora/testdata/a_queue25.dbf',
        '/u1/TEST/testora/testdata/a_ref01.dbf',
        '/u1/TEST/testora/testdata/a_ref02.dbf',
        '/u1/TEST/testora/testdata/a_summ01.dbf',
        '/u1/TEST/testora/testdata/a_summ02.dbf',
        '/u1/TEST/testora/testdata/a_summ03.dbf',
        '/u1/TEST/testora/testdata/a_summ04.dbf',
        '/u1/TEST/testora/testdata/a_summ05.dbf',
        '/u1/TEST/testora/testdata/a_tools01.dbf',
        '/u1/TEST/testora/testdata/a_txn_data01.dbf',
        '/u1/TEST/testora/testdata/a_txn_data02.dbf',
        '/u1/TEST/testora/testdata/a_txn_data03.dbf',
        '/u1/TEST/testora/testdata/a_txn_data04.dbf',
        '/u1/TEST/testora/testdata/a_txn_data05.dbf',
        '/u1/TEST/testora/testdata/a_txn_data06.dbf',
        '/u1/TEST/testora/testdata/a_txn_data07.dbf',
        '/u1/TEST/testora/testdata/a_txn_data08.dbf',
        '/u1/TEST/testora/testdata/a_txn_data09.dbf',
        '/u1/TEST/testora/testdata/a_txn_data10.dbf',
        '/u1/TEST/testora/testdata/a_txn_data11.dbf',
        '/u1/TEST/testora/testdata/a_txn_data12.dbf',
        '/u1/TEST/testora/testdata/a_txn_data13.dbf',
        '/u1/TEST/testora/testdata/a_txn_data14.dbf',
        '/u1/TEST/testora/testdata/a_txn_data15.dbf',
        '/u1/TEST/testora/testdata/a_txn_data16.dbf',
        '/u1/TEST/testora/testdata/a_txn_data17.dbf',
        '/u1/TEST/testora/testdata/a_txn_data18.dbf',
        '/u1/TEST/testora/testdata/a_txn_data19.dbf',
        '/u1/TEST/testora/testdata/a_txn_data20.dbf',
        '/u1/TEST/testora/testdata/a_txn_data21.dbf',
        '/u1/TEST/testora/testdata/a_txn_data22.dbf',
        '/u1/TEST/testora/testdata/a_txn_data23.dbf',
        '/u1/TEST/testora/testdata/a_txn_data24.dbf',
        '/u1/TEST/testora/testdata/a_txn_data25.dbf',
        '/u1/TEST/testora/testdata/a_txn_data26.dbf',
        '/u1/TEST/testora/testdata/a_txn_data28.dbf',
        '/u1/TEST/testora/testdata/a_txn_data29.dbf',
        '/u1/TEST/testora/testdata/a_txn_data30.dbf',
        '/u1/TEST/testora/testdata/a_txn_data31.dbf',
        '/u1/TEST/testora/testdata/a_txn_data32.dbf',
        '/u1/TEST/testora/testdata/a_txn_data33.dbf',
        '/u1/TEST/testora/testdata/a_txn_data34.dbf',
        '/u1/TEST/testora/testdata/a_txn_data35.dbf',
        '/u1/TEST/testora/testdata/a_txn_data36.dbf',
        '/u1/TEST/testora/testdata/a_txn_data37.dbf',
        '/u1/TEST/testora/testdata/a_txn_data38.dbf',
        '/u1/TEST/testora/testdata/a_txn_data39.dbf',
        '/u1/TEST/testora/testdata/a_txn_data40.dbf',
        '/u1/TEST/testora/testdata/a_txn_data41.dbf',
        '/u1/TEST/testora/testdata/a_txn_data42.dbf',
        '/u1/TEST/testora/testdata/a_txn_data43.dbf',
        '/u1/TEST/testora/testdata/a_txn_data44.dbf',
        '/u1/TEST/testora/testdata/a_txn_data45.dbf',
        '/u1/TEST/testora/testdata/a_txn_data46.dbf',
        '/u1/TEST/testora/testdata/a_txn_data47.dbf',
        '/u1/TEST/testora/testdata/a_txn_data48.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind01.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind02.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind03.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind04.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind05.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind06.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind07.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind08.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind09.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind10.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind11.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind12.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind13.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind14.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind15.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind16.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind17.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind18.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind19.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind20.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind21.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind22.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind23.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind24.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind25.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind26.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind27.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind28.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind29.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind30.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind31.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind32.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind33.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind34.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind35.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind36.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind37.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind38.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind39.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind40.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind41.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind42.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind43.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind44.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind45.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind46.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind47.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind48.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind49.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind50.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind51.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind52.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind53.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind54.dbf',
        '/u1/TEST/testora/testdata/a_txn_ind55.dbf',
        '/u1/TEST/testora/testdata/ctxd01.dbf',
        '/u1/TEST/testora/testdata/odm.dbf',
        '/u1/TEST/testora/testdata/olap.dbf',
        '/u1/TEST/testora/testdata/owad01.dbf',
        '/u1/TEST/testora/testdata/portal01.dbf',
        '/u1/TEST/testora/testdata/statspack_01.dbf',
        '/u1/TEST/testora/testdata/tplcux_data_01.dbf',
        '/u1/TEST/testora/testdata/tplcux_idx_01.dbf',
        '/u1/TEST/testora/testdata/interim.dbf',
        '/u1/TEST/testora/testdata/system12.dbf',
        '/u1/TEST/testora/testdata/a_txn_data49.dbf',
        '/u1/TEST/testora/testdata/a_ref03.dbf',
        '/u1/TEST/testora/testdata/a_summ06.dbf',
        '/u1/TEST/testora/testdata/undo04.dbf'
    CHARACTER SET UTF8
    ;
    
create controlfile in `SQL*Plus`

    [testora@target ~]$ ll
    total 11964
    -rw-r--r--.  1 testora dba    10773 Oct 17 11:19 controlfile.sql
    drwxr-xr-x. 10 testora dba     4096 Jun 21 17:12 itsection
    drwxr-xr-x.  3 testora dba     4096 May 31 00:43 oradiag_testora
    -rw-r--r--.  1 testora dba    26359 Oct 17 11:10 PROD_ora_7826.trc
    -rw-r--r--.  1 testora dba     1139 Jul 15 16:30 rdccs_m000_15683.out
    -rw-r--r--.  1 testora dba 12196573 Jul 15 16:28 rdccs_m000_15683.trc

    [testora@target ~]$ sqlplus  /nolog

    SQL*Plus: Release 11.2.0.3.0 Production on Thu Oct 17 17:30:33 2013

    Copyright (c) 1982, 2011, Oracle.  All rights reserved.

    SQL> conn /as sysdba
    Connected.
    SQL> shutdown immediate;
    ORA-01109: database not open


    Database dismounted.
    ORACLE instance shut down.
   
    SQL> startup nomount;
    ORACLE instance started.

    Total System Global Area 5.1310E+10 bytes
    Fixed Size		    2240344 bytes
    Variable Size		 1.0066E+10 bytes
    Database Buffers	 4.1205E+10 bytes
    Redo Buffers		   36098048 bytes
    SQL> @controlfile.sql

    Control file created.
    
open database
 
    SQL> alter database open resetlogs;
    alter database open resetlogs
    *
    ERROR at line 1:
    ORA-38856: cannot mark instance UNNAMED_INSTANCE_2 (redo thread 2) as enabled
    
create logfile group for thread 2 and then disable it

    [testora@tplat2 oradata]$ sqlplus  /nolog

    SQL*Plus: Release 11.2.0.3.0 Production on Wed Jul 31 16:49:15 2013

    Copyright (c) 1982, 2011, Oracle.  All rights reserved.

    SQL> conn /as sysdba
    Connected.

    SQL> ALTER DATABASE ADD LOGFILE THREAD 2
      GROUP 4 (
        '/u1/TEST/testora/testdata/redo4_1.dbf',
        '/u1/TEST/testora/testdata/redo4_2.dbf'
      ) SIZE 500M BLOCKSIZE 512,
      GROUP 5 (
        '/u1/TEST/testora/testdata/redo5_1.dbf',
        '/u1/TEST/testora/testdata/redo5_2.dbf'
      ) SIZE 500M BLOCKSIZE 512,
       GROUP 6 (
        '/u1/TEST/testora/testdata/redo6_1.dbf',
        '/u1/TEST/testora/testdata/redo6_2.dbf'
      ) SIZE 500M BLOCKSIZE 512;

    Database altered.
    
open database

    SQL> alter database open resetlogs;

    Database altered.

    SQL> alter database disable thread 2;

    Database altered.

    SQL> alter database drop logfile group 4, group 5, group 6;
    
    Database altered.
    
    SQL> shutdown immediate;
    Database closed.
    Database dismounted.
    ORACLE instance shut down.
    SQL> startup;
    ORACLE instance started.

    Total System Global Area 5.1310E+10 bytes
    Fixed Size		    2240344 bytes
    Variable Size		 1.0066E+10 bytes
    Database Buffers	 4.1205E+10 bytes
    Redo Buffers		   36098048 bytes
    Database mounted.
    Database opened.

alert.log

    [testora@target trace]$ pwd
    /u1/11gR2_BASE/admin/prod/diag/rdbms/prod/PROD/trace
    [testora@target trace]$ cat alert_PROD.log
    ...
    WARNING: The following temporary tablespaces contain no files.
             This condition can occur when a backup controlfile has
             been restored.  It may be necessary to add files to these
             tablespaces.  That can be done using the SQL statement:
     
             ALTER TABLESPACE <tablespace_name> ADD TEMPFILE
     
             Alternatively, if these temporary tablespaces are no longer
             needed, then they can be dropped.
               Empty temporary tablespace: TEMP
    ...
    
    SQL> alter tablespace temp add tempfile '/u1/TEST/testora/testdata/temp01.dbf' size 2000M, '/u1/TEST/testora/testdata/temp02.dbf' size
    alter tablespace temp add tempfile '/u1/TEST/testora/testdata/temp01.dbf' size 2000M, '/u1/TEST/testora/testdata/temp02.dbf' size 2000M
    *
    ERROR at line 1:
    ORA-00600: internal error code, arguments: [kghstack_free1], [list of datafile
    #'s], [], [], [], [], [], [], [], [], [], []
    
    SQL> SELECT TABLESPACE_NAME,FILE_ID,FILE_NAME,BYTES,BLOCKS,STATUS FROM DBA_TEMP_FILES ORDER BY 1, 2;
    
    TABLESPACE_NAME   FILE_ID FILE_NAME						         BYTES	     BLOCKS      STATUS    
    ----------------- ------- -------------------------------------- ----------- ----------- -------
    TEMP				     1 /u1/TEST/testora/testdata/temp01.dbf	  2097152000	  256000 ONLINE    
    TEMP				     2 /u1/TEST/testora/testdata/temp02.dbf	  2097152000	  256000 ONLINE    
    
##Post Steps
 
###listener configuration
    
show service_names
    
    SQL> show parameter name;

    NAME				     TYPE	 VALUE
    ------------------------------------ ----------- ------------------------------
    db_file_name_convert		     string	 +DATADG/prodora/proddata, /u1/
                             TEST/testora/testdata
    db_name 			     string	 PROD
    db_unique_name			     string	 PROD
    global_names			     boolean	 FALSE
    instance_name			     string	 PROD
    lock_name_space 		     string
    log_file_name_convert		     string	 +DATADG/prodora/proddata, /u1/
                             TEST/testora/testdata
    processor_group_name		     string
    service_names			     string	 PROD
    
listener configuration
    
    [testora@target ~]$ lsnrctl start

    LSNRCTL for Linux: Version 11.2.0.3.0 - Production on 18-OCT-2013 08:41:27

    Copyright (c) 1991, 2011, Oracle.  All rights reserved.

    Starting /u1/11gR2_BASE/product/11.2.0/bin/tnslsnr: please wait...

    TNSLSNR for Linux: Version 11.2.0.3.0 - Production
    System parameter file is /u1/11gR2_BASE/product/11.2.0/network/admin/ERP_erp/listener.ora
    Log messages written to /u1/11gR2_BASE/diag/tnslsnr/target/listener/alert/log.xml
    Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=target.egolife.com)(PORT=1521)))

    Connecting to (ADDRESS=(PROTOCOL=tcp)(HOST=)(PORT=1521))
    STATUS of the LISTENER
    ------------------------
    Alias                     LISTENER
    Version                   TNSLSNR for Linux: Version 11.2.0.3.0 - Production
    Start Date                18-OCT-2013 08:41:27
    Uptime                    0 days 0 hr. 0 min. 0 sec
    Trace Level               off
    Security                  ON: Local OS Authentication
    SNMP                      OFF
    Listener Parameter File   /u1/11gR2_BASE/product/11.2.0/network/admin/ERP_erp/listener.ora
    Listener Log File         /u1/11gR2_BASE/diag/tnslsnr/target/listener/alert/log.xml
    Listening Endpoints Summary...
      (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=target.egolife.com)(PORT=1521)))
    The listener supports no services
    The command completed successfully

    [testora@target ~]$ env | grep TNS_ADMIN
    TNS_ADMIN=/u1/11gR2_BASE/product/11.2.0/network/admin/ERP_erp
    [testora@target ~]$ export TNS_ADMIN=TNS_ADMIN=/u1/11gR2_BASE/product/11.2.0/network/admin
    [testora@target ~]$ echo $TNS_ADMIN
    TNS_ADMIN=/u1/11gR2_BASE/product/11.2.0/network/admin
    [testora@target ~]$ lsnrctl stop

    LSNRCTL for Linux: Version 11.2.0.3.0 - Production on 18-OCT-2013 08:46:09

    Copyright (c) 1991, 2011, Oracle.  All rights reserved.

    Connecting to (ADDRESS=(PROTOCOL=tcp)(HOST=)(PORT=1521))
    The command completed successfully
    
listener.ora and tnsnames.ora

    [testora@target admin]$ pwd
    /u1/11gR2_BASE/product/11.2.0/network/admin
    [testora@target admin]$ cat listener.ora 
    PROD =
      (DESCRIPTION_LIST =
        (DESCRIPTION =
          (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.5)(PORT = 1521))
        )
      )

    SID_LIST_ERP =
      (SID_LIST =
        (SID_DESC =
          (ORACLE_HOME= /u1/11gR2_BASE/product/11.2.0)
          (SID_NAME = PROD)
        )
      )

    [testora@target admin]$ cat tnsnames.ora 
    PROD =
      (DESCRIPTION =
        (ADDRESS_LIST =
          (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.5)(PORT = 1521))
        )
        (CONNECT_DATA =
          (SERVICE_NAME = prod)
        )
      )
    
start listener
    
    [testora@target ~]$ lsnrctl start

    LSNRCTL for Linux: Version 11.2.0.3.0 - Production on 18-OCT-2013 08:46:14

    Copyright (c) 1991, 2011, Oracle.  All rights reserved.

    Starting /u1/11gR2_BASE/product/11.2.0/bin/tnslsnr: please wait...

    TNSLSNR for Linux: Version 11.2.0.3.0 - Production
    System parameter file is /u1/11gR2_BASE/product/11.2.0/network/admin/listener.ora
    Log messages written to /u1/11gR2_BASE/diag/tnslsnr/target/listener/alert/log.xml
    Listening on: (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=192.168.1.5)(PORT=1521)))

    Connecting to (ADDRESS=(PROTOCOL=tcp)(HOST=)(PORT=1521))
    STATUS of the LISTENER
    ------------------------
    Alias                     LISTENER
    Version                   TNSLSNR for Linux: Version 11.2.0.3.0 - Production
    Start Date                18-OCT-2013 08:46:14
    Uptime                    0 days 0 hr. 0 min. 0 sec
    Trace Level               off
    Security                  ON: Local OS Authentication
    SNMP                      OFF
    Listener Parameter File   /u1/11gR2_BASE/product/11.2.0/network/admin/listener.ora
    Listener Log File         /u1/11gR2_BASE/diag/tnslsnr/target/listener/alert/log.xml
    Listening Endpoints Summary...
      (DESCRIPTION=(ADDRESS=(PROTOCOL=tcp)(HOST=192.168.1.5)(PORT=1521)))
    The listener supports no services
    The command completed successfully
    [testora@target ~]$ tnsping prod

    TNS Ping Utility for Linux: Version 11.2.0.3.0 - Production on 18-OCT-2013 08:46:26

    Copyright (c) 1997, 2011, Oracle.  All rights reserved.

    Used parameter files:
    /u1/11gR2_BASE/product/11.2.0/network/admin/ERP_erp/sqlnet_ifile.ora


    Used TNSNAMES adapter to resolve the alias
    Attempting to contact (DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.1.5)(PORT = 1521))) (CONNECT_DATA = (SERVICE_NAME = prod)))
    OK (10 msec)
    
client test with `PL*SQL` Developer ...

###restart database

    SQL> create pfile from spfile;

    File created.

    SQL> shutdown immediate;
    Database closed.
    Database dismounted.
    ORACLE instance shut down.
    
    SQL> startup;  
    ORACLE instance started.

    Total System Global Area 5.1310E+10 bytes
    Fixed Size		    2240344 bytes
    Variable Size		 1.0066E+10 bytes
    Database Buffers	 4.1205E+10 bytes
    Redo Buffers		   36098048 bytes
    Database mounted.
    Database opened.

##full backup of database ...

##Reference

* Oracle Database Backup and Reference User's Guide