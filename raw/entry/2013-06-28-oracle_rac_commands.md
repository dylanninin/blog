---
layout: post
title: Oracle RAC Command
category : Oracle
tags : [Oracle, Database, DBA]
---

## Oracle Clusterware命令

集群层次

* 节点：osnodes
* 网络：oifcfg
* 集群：csrctl, ocrcheck, orchdump, orcconfig
* 应用：srvctl, crs_stat, onsctl

## 节点

olsnodes

    [grid@dev1 ~]$ olsnodes -help
    ... ...

## 网络

oifcfg

    [grid@dev1 ~]$ oifcfg -help
	... ...


## 集群

### crs

	crsctl start|stop crs	
    crsctl enable|disable crs
	crsctl check crs
    
    [grid@dev1 ~]$ crsctl -help
	... ...

## 应用

### crs

    crs_stat 已经deprecated，请使用crsctl status resource

	crs_stat
	crs_stat -v
	crs_stat -v|p service_name
	crs_stat -ls
    
    [grid@dev1 ~]$ crs_stat -help
	... ...

### onsctl
	
	[grid@dev1 ~]$ onsctl help
	... ...

### srvctl	

srvctl help	

	[grid@dev1 ~]$ srvctl --help
	... ...

trace srvctl

	export SRVM_TRACE=TRUE
	srvctl config database -d prod -a

srvctl database:	

 	srvctl config database -d prod -a		
	srvctl start database -d prod
	srvctl start database -d prod -i prod1 -o mount
	
srvctl	instance

	srvctl stop instance -d prod -i prod1 -o immediate
	
srvctl	service

	srvctl start service -d prod -v
	srvctl start service -d prod -v -s service -i prod1
	srvctl stop service -d prod -v -s service -i prod1
	srvctl status service -d prod -v
				
srvctl	asm	
	
	srvctl start asm -n dev1
	srcctl start asm -n erpdb2

    
## 常用命令

### 停止/启动

停止顺序：grid停止database或instance -> root用户停止crs
启动顺序：root用户启动crs -> grid用户启动database或instance

停止/启动RAC所有实例

    srvctl stop|start database -d dbname

停止/启动RAC单个实例

    srvctl stop|start instance -d dbname -i instancename
 
停止/启动CRS

    crsctl stop|start crs
    
### 检查crs resource状态

    crs_stat -t -v
    crsctl stat res -t
    
### 检查HAS资源是否正常

    crsctl check crs
    
### 检查vodedisk, orc的位置

    crsctl query css votedisk
    ocrcheck
    
### 检查orc备份

    ocrconfig -showbackup
    
### 检查网络配置

    srvctl config nodeapps -a
    oifcfg getif
    oifcfg iflis
