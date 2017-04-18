---
layout: post
title: A Case of OPP Exception
category : Oracle
tags : [Oracle, DBA, EBS, Exception]
---

## Output Post Processor

Concurrent Processing now uses the Output Post Processor (OPP) to enforce post-processing actions for concurrent requests. Post-processing actions are actions taken on concurrent request output. An example of a post-processing action is that used in Concurrent Processing support of XML Publisher. If a request is submitted with an XML Publisher template specified as a layout for the concurrent request output, then after the concurrent manager finishes running the concurrent program, it will contact the OPP to apply the XML Publisher template and create the final output.

### Manager Log

Responsibility Path：System Administartor >> Concurrent >> Manager >> Administer，找到 Output Post Processor，选择Processes，查看日志时，选择 Manager Log即可。

日志如下：
	
	... ...
	[3/18/13 11:06:25 AM] [OPPServiceThread0] Post-processing request 20000374.
	[3/18/13 11:06:26 AM] [123757:RT20000374] Executing post-processing actions for request 20000374.
	[3/18/13 11:06:26 AM] [123757:RT20000374] Starting XML Publisher post-processing action.
	[3/18/13 11:06:26 AM] [123757:RT20000374] 
	Template code: XX_INV_ORGDIAOBO
	Template app:  ONT
	Language:      zh
	Territory:     CN
	Output type:   EXCEL
	[3/18/13 11:06:56 AM] [123757:RT20000374] XML Publisher post-processing action complete.
	[3/18/13 11:06:57 AM] [123757:RT20000374] Completed post-processing actions for request 20000374.
	[3/18/13 11:25:18 AM] [OPPServiceThread0] Post-processing request 20000836.
	[3/18/13 12:04:00 PM] [OPPServiceThread1] Post-processing request 20002627.
	[3/18/13 1:33:00 PM] [OPPServiceThread1] Post-processing request 20004039.
	[3/18/13 2:11:45 PM] [OPPServiceThread0] Post-processing request 20004816.
	[3/18/13 2:32:03 PM] [OPPServiceThread0] Post-processing request 20005431.
	[3/18/13 2:35:31 PM] [OPPServiceThread1] Post-processing request 20005534.
	[3/18/13 2:37:35 PM] [OPPServiceThread1] Post-processing request 20005554.
	[3/18/13 2:49:06 PM] [OPPServiceThread0] Post-processing request 20006105.
	[3/18/13 3:01:03 PM] [OPPServiceThread1] Post-processing request 20006657.
	[3/18/13 3:02:10 PM] [OPPServiceThread1] Post-processing request 20006688.
	[3/18/13 3:03:49 PM] [OPPServiceThread0] Post-processing request 20006730.
	[3/18/13 3:04:47 PM] [OPPServiceThread0] Post-processing request 20004000.
	[3/18/13 3:06:09 PM] [OPPServiceThread1] Post-processing request 20006802.
	[3/18/13 3:13:06 PM] [OPPServiceThread1] Post-processing request 20007065.
	[3/18/13 3:19:41 PM] [OPPServiceThread0] Post-processing request 20007441.
	[3/18/13 3:22:22 PM] [OPPServiceThread1] Post-processing request 20007546.
	[3/18/13 3:24:18 PM] [OPPServiceThread1] Post-processing request 20007695.
	[3/18/13 3:24:24 PM] [OPPServiceThread0] Post-processing request 20007707.
	[3/18/13 3:33:50 PM] [OPPServiceThread0] Post-processing request 20008124.
	[3/18/13 3:39:46 PM] [OPPServiceThread1] Post-processing request 20008351.
	[3/18/13 3:41:24 PM] [OPPServiceThread1] Post-processing request 20008494.
	[3/18/13 3:41:52 PM] [OPPServiceThread1] Post-processing request 20008507.
	[3/18/13 3:52:04 PM] [OPPServiceThread0] Post-processing request 20008915.
	[3/18/13 3:54:02 PM] [OPPServiceThread0] Post-processing request 20009040.
	[3/18/13 3:56:12 PM] [OPPServiceThread1] Post-processing request 20009153.
	[3/18/13 4:00:27 PM] [OPPServiceThread0] Post-processing request 20009271.
	[3/18/13 4:03:57 PM] [OPPServiceThread0] Post-processing request 20009434.
	[3/18/13 4:15:23 PM] [OPPServiceThread0] Post-processing request 20009946.
	[3/18/13 4:17:05 PM] [OPPServiceThread1] Post-processing request 20010020.
	[3/18/13 4:35:11 PM] [OPPServiceThread0] Post-processing request 20010758.
	[3/18/13 4:39:43 PM] [OPPServiceThread1] Post-processing request 20010989.
	[3/18/13 4:39:50 PM] [OPPServiceThread0] Post-processing request 20011015.
	[3/18/13 4:43:12 PM] [OPPServiceThread1] Post-processing request 20011195.
	[3/18/13 4:58:42 PM] [OPPServiceThread1] Post-processing request 20012085.
	[3/18/13 5:03:34 PM] [OPPServiceThread1] Post-processing request 20011940.
	[3/18/13 5:06:45 PM] [OPPServiceThread0] Post-processing request 20012221.
	[3/18/13 5:25:44 PM] [OPPServiceThread0] Post-processing request 20013863.
	[3/18/13 5:55:50 PM] [OPPServiceThread1] Post-processing request 20016234.
	[3/18/13 6:29:53 PM] [OPPServiceThread0] Post-processing request 20018561.
	[3/18/13 7:12:45 PM] [OPPServiceThread1] Post-processing request 20020489.
	[3/18/13 8:21:06 PM] [OPPServiceThread1] Post-processing request 20023085.
	[3/18/13 9:26:56 PM] [OPPServiceThread0] Post-processing request 20023160.
	[3/19/13 7:56:25 AM] [OPPServiceThread0] Post-processing request 20023315.
	[3/19/13 7:56:57 AM] [OPPServiceThread1] Post-processing request 20023317.
	[3/19/13 8:04:21 AM] [OPPServiceThread0] Post-processing request 20023331.
	[3/19/13 8:10:08 AM] [OPPServiceThread0] Post-processing request 20023438.
	[3/19/13 8:18:31 AM] [OPPServiceThread0] Post-processing request 20023572.
	[3/19/13 8:22:35 AM] [OPPServiceThread1] Post-processing request 20023622.
	[3/19/13 8:27:45 AM] [OPPServiceThread0] Post-processing request 20023721.
	[3/19/13 8:29:12 AM] [OPPServiceThread0] Post-processing request 20023796.
	[3/19/13 8:34:49 AM] [OPPServiceThread1] Post-processing request 20023960.
	[3/19/13 8:39:52 AM] [OPPServiceThread0] Post-processing request 20024067.
	[3/19/13 8:40:41 AM] [GSMServiceController:123757] Received shutdown request.
	[3/19/13 8:40:41 AM] [GSMServiceController:123757] Preparing to shutdown service.
	[3/19/13 8:40:41 AM] [GSMServiceController:123757] Stopping all Service Threads.
	[3/19/13 8:40:41 AM] [OPPServiceThread0] Preparing to shut down service thread.
	[3/19/13 8:40:41 AM] [OPPServiceThread1] Preparing to shut down service thread.
	[3/19/13 8:40:41 AM] [OPPServiceThread0] Received immediate shutdown request. Service Thread will shutdown once all running requests have completed.
	... ...

### 异常确认

重新提交ECO XML报表，结束状态为 WARNING。查看日志：

	Executing request completion options...
	
	+------------- 1) PUBLISH -------------+
	Beginning post-processing of request 20024067 on node ERPPROD at 19-MAR-2013 08:39:51.
	Post-processing of request 20024067 failed at 19-MAR-2013 08:59:52 with the error message:
	The Output Post-processor is running but has not picked up this request. 
	No further attempts will be made to post-process this request, and the request will be marked 
	with Warning status.
	Setting the profile option Concurrent: OPP Response Timeout to a higher value may be necessary.
	+--------------------------------------+
	
	+------------- 2) PRINT   -------------+
	+--------------------------------------+


	Finished executing request completion options.

## error message

Error Message：ONC-PP NO RESPONSE and TIMEOUT

The Output Post-processor is running but has not picked up this request. 
No further attempts will be made to post-process this request, and the request will be marked  with Warning status.
Setting the profile option Concurrent: OPP Response Timeout to a higher value may be necessary.

### Cause: ONC-PP NO RESPONSE and TIMEOUT

1.The Output Post Processor (OPP) service is not picking up any new requests.

The concurrent manager process generates the XML data file. Upon completion it will trigger the Output Post Processor in order to merge the XML data file and the template which was selected on the Submit Request form.

The number of concurrent requests that the Output Post Processor can handle in parallel depends upon:

* the number of Processes
* the number of Threads Per Process

The default values are 2 Processes and 5 Threads Per Process so a total of 10 reports can be processed in parallel.

In case there are other concurrent requests running which have already invoked the OPP then it might happen that no additional requests can be picked up for a period of time. The pending request will be picked up as soon as one of the running jobs completes. By default a timeout will occur if it takes longer then 120 seconds (2 min.) for the Output Post Processor to pick up the request from the concurrent manager process. In that case, the concurrent request will complete with status Warning and the request log file will contain Error Message (see above).

2.The Output Post Processor JAVA process is still running, but it is unresponsive. 

This can be due to errors in previous requests or just to the amount of time the manager has been running. The OPP becomes unresponsive (stale) after running for more than one week.

### Solution

* Option 1: Increase the value (in seconds) for the profile option 'Concurrent:OPP Response Timeout'.
* Option 2: Increase the number of processes or threads (or both) of the OPP via Oracle Applications Manager.


### ERPProd

#### 查看当前设置

在Administer Concurrent Managers中找到Output Post Processor，可以看到该程序的OS Pid，即Concurrent值；并在OS上查找该进行，可以看到OPP的设置信息。如下：

	# ps -ef | grep 123757
	 prodmgr 5488788 1269866   0   Feb 03      - 114:55 /usr/java14/bin/java -mx512m -Ddbcfile=/u1/PROD/prodmgr/prodappl/fnd/11.5.0/secure/PROD_erpprod/prod.dbc -Dcpid=123757 -Dlogfile=/u1/PROD/prodmgr/prodcomn/admin/log/PROD_erpprod/FNDOPP123757.txt -DLONG_RUNNING_JVM=true -DOVERRIDE_DBC=true -DFND_JDBC_BUFFER_MIN=1 -DFND_JDBC_BUFFER_MAX=2 oracle.apps.fnd.cp.gsf.GSMServiceController 


或者在数据库中执行以下SQL：

	SELECT *
	FROM fnd_concurrent_queues fcq, fnd_concurrent_processes fcp
	WHERE process_status_code not in ('K', 'S')
	AND fcq.concurrent_queue_id = fcp.concurrent_queue_id
	AND fcq.application_id = fcp.queue_application_id
	and concurrent_queue_name = 'FNDCPOPP';

#### 更改OPP设置

登陆ERP，选择System Administrator >> Dashboard >> Site Map >> Administration : Application Services : Generic Services，选择 Output Post Processor，即可查看更改OPP设置。

The OPP Service is multi-threaded and will start a new thread for each concurrent request it processes. You can control the number of simultaneous threads for an OPP Service Instance by adjusting the Threads per Process parameter for the instance. If all the OPP process have reached their respective maximum number of threads, the requests waiting to be processed remain in a queue to be processed as soon as threads become available. If request throughput has become slow, you may want to increase the number of Threads per Process for the OPP. We recommend you keep the number of Threads per Process between 1 and 20. You may find that you get even better performance by increasing the number of OPP processes.

系统原先设置为： 1 Process * 5 Threads Per Process。

现调整为： 2 Process * 10 Threads Per Process。

#### 重启OPP

在Administer Concurrent Managers中找到Output Post Processor，可以选择Restart，但长期不响应，很长时间处于restarting状态，这里就只能采取杀死OPP进程，再重新启动OPP的办法。

#### 报表测试

再次提交ECO XML报表，则可以正常完成和输出报表。

## Reference

* Concurrent Requests Fail Due to Output Post Processing (OPP) Timeout [ID 352518.1]
