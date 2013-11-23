---
layout: post
title: Oracle EBS Adadmin Scripts
category : Oracle
tags : [Oracle, DBA, EBS]
---

## Admin Scripts for instance

location: `<RDBMS ORACLE_HOME>/appsutil/scripts/dbname_node`

	Control 		Functionality
	addbctl.sh 		Control database server
	addlnctl.sh 	Control Oracle Net listener for the database server

## RDBMS ORACLE_HOME Install scripts

location: `<RDBMS ORACLE_HOME>/appsutil/install/dbname_node`

	Install   		Functionality
	adsvdlsn.sh	 	Start Oracle Net listener during installation
	adcrdb.sh	 	Start database and create database control files
	addbprf.sh	 	Set profile option values
	adsvdcnv.sh	 	Perform character set conversion and licensing tasks
	adsvdb.sh	 	Start database during installation

##COMMON_TOP Control scripts 

location: `<COMMON_TOP>/admin/scripts/dbname_node)`

	Install Script  Functionality
	adalnctl.sh	 	Control Oracle Net8 listener for Applications services	 
					All application tier server nodes
	adstrtal.sh	 	Start all Applications server processes	 
					All application tier server nodes
	adstpall.sh	 	Stop all Applications server processes	 
					All application tier server nodes
	adfrmctl.sh	 	Control Forms server	 
					Forms server node
	adfmcctl.sh	 	Control Forms Metrics Client	 
					Forms server node
	adfmsctl.sh	 	Control Forms Metrics Server	 
					HTTP server node
	adtcfctl.sh	 	Control TCF SocketServer	 
					Concurrent processing server node
	adcmctl.sh	 	Control Concurrent managers	 
					Concurrent processing server node
	adrepctl.sh	 	Control Reports server	 
					Concurrent processing server node
	adapcctl.sh	 	Control Apache processes	 
					HTTP server node
	jtffmctl.sh	 	Control Oracle fulfillment server	 
					HTTP server node

##COMMON_TOP Install scripts 

location: `<COMMON_TOP>/admin/install/dbname_node`

	Install		 	Functionality
	adsvalsn.sh	 	Start Net8 listener processes for Applications services	 
					All application tier server nodes
	adsvfrm.sh	 	Start Forms server during install	 
					Forms server node
	adsvfmc.sh	 	Start Forms server during install	 
					Forms server node
	adsvfms.sh	 	Start Forms metric server during install	 
					HTTP server node
	adsvcm.sh	 	Start Concurrent manager during install	 
					Concurrent processing server node
	adsvtcf.sh	 	Start TCF server during install	 
					Concurrent processing server node
	adsvrep.sh	 	Start Reports server during install	 
					Concurrent processing server node
	adsvapc.sh	 	Start Apache server during install	 
					HTTP server node
	jtfsvfm.sh	 	Start Fulfillment server during install	 
					HTTP server node

