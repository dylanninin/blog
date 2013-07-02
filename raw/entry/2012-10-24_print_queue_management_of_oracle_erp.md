#写在前面的话
在ERP系统中，打印报表是不可或缺的应用之一。

由于Oracle本身的集成性，很多时候需要第三方工具的支持来一起完成某些任务，打印报表即是其中一个的典型。

在Oracle EBS 11i以上版本中，一个典型的报表打印设置，就涉及到ERP应用中打印队列的管理、ERP主机上打印队列的管理、打印服务器上Remote Print Manager打印队列的管理以及远程打印机的管理。

Oracle ERP打印队列结构图

![Oracle ERP](http://www.dylanninin.com/blog/images/2012/10/printer_of_erp.png)

#打印服务器

##1. Windows打印机管理

在Windows中，有两种方式添加打印机：

* 1）图形界面方式:在控制面板中，添加打印机和传真

* 2）命令行方式:C:\Windows\System32\prnmngr.vbs           

当批量添加打印机时，使用图形界面的方式实在是一件体力活。如在做打印服务器迁移时，将几台打印服务器上的远程打印机迁移到同一台打印服务器，此时使用向导界面则会非常耗时，而且稍有不慎，就可能会勾选错误，导致打印机设置不正确；当然，出现问题也不好排查。所幸的是，Windows也提供了vbs脚本来管理打印机。

###使用命令行管理打印机

使用命令行管理打印机需要Windows操作系统中有`prnmngr.vbs`脚本，一般Windows XP，Windows Server 2003中会自带这些脚本，以下为简单的学习笔记。

	cscript prnmngr.vbs
	cd  /D  C:\Windows\System32
	cscript prnmngr.vbs
	用法: prnmngr [-adxgtl?][c] [-s 服务器][-p 打印机][-m 驱动程序型号]
	             [-r 端口][-u 用户名][-w 密码]
	
	参数:
	-a     - 添加本地打印机
	-ac    - 添加打印机连接
	-d     - 删除打印机
	-g     - 获取默认打印机
	-l     - 列出打印机
	-m     - 驱动程序型号
	-p     - 打印机名
	-r     - 端口名
	-s     - 服务器名
	-t     - 设置默认打印机
	-u     - 用户名
	-w     - 密码
	-x     - 删除所有打印机
	-?     - 显示命令用法
 
	例如:
	prnmngr -a -p "打印机" -m "驱动程序" -r "lpt1:
	prnmngr -d -p "打印机" -s 服务器
	prnmngr -ac -p "\\服务器\打印机"
	prnmngr -d -p "\\服务器\打印机"
	prnmngr -x -s 服务器
	prnmngr -l -s 服务器
	prnmngr -g
	prnmngr -t -p "\\服务器\打印机"

####主要用法

添加本地打印机

	cscript prnmngr.vbs -a -p PrinterName [-s RemoteComputer] -m DriverName -r PortName  [-u UserName] [-w Password]

示例

	cscript prnmngr.vbs -a -p testptq_1 -m "Epson LQ-680Pro ESC/P 2"  -r LPT1:

删除打印机

删除指定打印机

	cscript prnmngr.vbs -d -p PrinterName [-s RemoteComputer] [-u UserName] [-w Password]

删除所有打印机，慎用！

	cscript prnmngr.vbs -x [-s RemoteComputer] [-u UserName] [-w Password]

设置默认打印机

显示默认打印机

	cscript prnmngr.vbs -g
	
设置默认打印机

	cscript prnmngr.vbs -t -p PrinterName

列出所有打印机

	cscript prnmngr.vbs -l [-s RemoteComputer] [-u UserName -w Password]

示例

	cscript prnmngr.vbs -l

添加远程打印机

先创建tcp/ip端口

	cscript prnport.vbs -a -r IP_192.168.1.111_1 -h 192.168.1.111 -o lpr -q testptq

再添加远程打印机

	cscript prnmngr.vbs -a -p testptq -m "Epson LQ-680Pro ESC/P 2" -r IP_192.168.1.111_1

打印机服务脚本

* prnmngr.vbs：添加或删除打印机
* prncnfg.vbs：配置打印机
* prndrvr.vbs：添加或删除打印机驱动程序
* prnjobs.vbs：管理打印作业
* prnqctl.vbs：管理打印测试页、暂停打印机、继续运行打印机或清除打印机队列
* prnport.vbs：添加或删除打印机端口

##2. RPM打印队列管理

在Windows打印服务器管理打印队列，可以使用付费软件Remote Print Manager。用来接收来自ERP服务器的打印请求，接收请求后，在RPM打印队列中进行一些格式的调整或转换，之后，再将这些请求发送给远程打印机进行真正的打印作业。

目前主要接触过RPM Elite 4.5和RPM 5.1.1.99，新版本的功能更加强大，管理也方便。


##3. AIX打印队列管理

###基本概念

print job

* 在打印机上运行的作业单元
* 一个打印任务可以打印单个或多个文件
* 每个打印任务由job id 唯一标识

queue

* 打印队列用来管理打印任务
* 配置：/etc/qconfig
* 队列名和队列设备

queue device

* 队列设备，可以是本地、远程等设备

注：一个单独的打印队列可以与多个队列设备关联

Print spooler

* 管理打印的通用系统

###日常管理

####create

* 命令:smit print

####configure

* /etc/qconfig

* example:

	testptq:
	        device = @testptq
	        up = TRUE
	        host = testptq                                               
	        s_statfilter = /usr/lib/lpd/bsdshort
	        l_statfilter = /usr/lib/lpd/bsdlong
	        rq = testptq                                                             
	@testptq:
	        backend = /usr/lib/lpd/rembak

####control

#####lpstat 
	
lpstat：显示线性打印机的目前状态信息

	usage: lpstat [-drstW][-aDestination,...][-cClassname,...]
	              [-oOutRequirement,...][-pPrinter,...][-uUser,...]
	              [-vPrinter,...] [jobid,...]
			Prints LP status information.

qchk：显示某些打印任务、打印队列的目前状态信息

lpq：显示某些指定用户、任务号的打印任务的状态信息

lpr：使用打印系统打印文件

#####stop

	enq  -D -P 'testoffice:@testptq'  #D Down print queue
	enq  -A -w Delay   #当打印队任务完成时每间隔多少秒更新打印状态信息

#####start

	lpstat -vxxoffice              #status
	enq -U -P 'xxoffice:@testptq'  #start queue
	qchk -P  xxoffice              #status
	enabl    xxoffice:@testptq     #start queue

#####flush

	lpstat -vxxoffice
	qcan -P xxoffice -x 3          #cancel job 3 on queue xxoffice
	cancel       3                 #cancel job 3
	lprm -P xxoffice 3             #cancel job 3 on queue xxoffice
	enq -P xxoffice  -x 3          #cancel job 3 on queue xxoffice

example:

	# lpstat -vxxoffice
	Queue   Dev   Status    Job Files              User         PP %   Blks  Cp Rnk
	------- ----- --------- --- ------------------ ---------- ---- -- ----- --- ---
	xxoffic @xxof DOWN    
	              QUEUED    505 STDIN.966664       testmgr                1   1   1
	              QUEUED    506 STDIN.622782       testmgr                1   1   2
	              QUEUED    507 STDIN.581720       testmgr                1   1   3
	: (FATAL ERROR) 0781-233 Unknown host xxoffice.

	# qcan -P xxoffice -x 505
	: (FATAL ERROR) 0781-233 Unknown host xxoffice.

	# lpstat -vxxoffice     
	Queue   Dev   Status    Job Files              User         PP %   Blks  Cp Rnk
	------- ----- --------- --- ------------------ ---------- ---- -- ----- --- ---
	xxoffic @xxof DOWN    
	
	              QUEUED    506 STDIN.622782       testmgr                1   1   1
	
	              QUEUED    507 STDIN.581720       testmgr                1   1   2
	
	: (FATAL ERROR) 0781-233 Unknown host xxoffice.
	# cancel 506
	# lpstat -vxxoffice
	Queue   Dev   Status    Job Files              User         PP %   Blks  Cp Rnk
	------- ----- --------- --- ------------------ ---------- ---- -- ----- --- ---
	xxoffic @xxof DOWN    
	              QUEUED    507 STDIN.581720       testmgr                1   1   1
	: (FATAL ERROR) 0781-233 Unknown host xxoffice.

#####check
* lpstat       
* ps ef | grep qdaemon
* make sure that system date is correct   #enq -Y to register qconfig file
* make sure /tmp directory is not full
* obsolete queue:/var/spool/lpd/qdir and remove from /etc/qconfig
* hosts can be pinged 

####命令汇总

Commands and equivalents

	Submit print jobs   Status print jobs    Cancel print jobs
	enq                 enq -A               enq -x
	qprt                qchk                 qcan
	lp                  lpstat               lprm
	lpr                 lpq                  cancel

##4. ERP打印队列的管理

在ERP应用中打印队列的设置主要包括打印机驱动、样式、类型以及注册等四个方面，用户在提交报表请求时选择所需要的打印机即可完成想要的打印作业。

其中，打印驱动设置是重点。

打印机的驱动，是ERP应用中打印请求抛向外部（操作系统、打印机等）的出口，可以使用操作系统命令、程序或者子例程的方式实现。

本例中，直接使用操作系统的打印命令，如下：

![](http://www.dylanninin.com/blog/images/2012/10/printer_driver.png)

直接调用操作系统的打印命令进行打印，其中arguments内容如下：

	 /usr/bin/iconv -f UTF-8 -t GB18030 $PROFILES$.FILENAME | lpr -P$PROFILES$.PRINTER -#$PROFILES$.CONC_COPIES -T"$PROFILES$.TITLE"

 配置好打印驱动之后，还需要设置好打印样式、打印类型；之后，就可以在ERP应用中注册打印队列。

##5.CentOS打印队列管理

Oracle ERP也是一个跨平台的应用，除了可以部署在Unix上，如IBM AIX，还可以部署在Linux、Windows平台，如CentOS等。

在CentOS上，提供了与AIX系统上类似的lpstat、cancel等cups打印机管理工具，只要熟悉了AIX上打印作业管理，在其他平台上上手十分容易。

 CentOS中，也提供了两种打印机管理方式，图形界面和命令行。在使用过程中，若批量新建打印队列，则可以先以图形向导设置一个打印队列，测试通过后，再直接编辑配置文件，重启打印服务器即可。

CentOS中，打印机配置文件：`/etc/cups/printers.conf`。编辑后，重启cups服务。

#测试

从Oracle ERP打印机设置中可以看出，在实际使用过程中，打印请求会首先从ERP应用中运行完毕后以打印命令的方式抛向ERP服务器；然后，ERP服务器通过CUPS/lpd服务或协议将请求发送给远程打印服务器，这里为RPM打印管理服务器；在RPM打印管理服务器上，又会进行一些格式的调整或转换，最后才将请求抛给远程打印机进行真正的打印作业。

一个打印作业经过ERP应用、ERP服务器、RPM服务器、打印机最后才能真正变成手上拿着的报表或者单据。若其中任何一个环节出现问题，打印作业则有可能出现异常，因此快速的排查解决问题十分重要。这里提供一个思路，类似于单元测试、集成测试的概念，自底向上，从依赖性最小的环节开始测试，确保没有问题，再测试依赖此服务的其他环节，直到最后能够形成一套完整、可用的打印服务。

在此例中，测试可能需要经过以下步骤：

##1. Windows上打印机管理

新建TCP/IP端口，并创建远程打印机后，打印测试页，进行测试。

注：在测试前，确保远程打印机可以ping通。

##2. RPM上打印队列管理

目前暂未找到直接测试RPM上打印队列的方法

##3. AIX上打印队列管理

使用命令行测试

在ERP应用中，注册的打印队列使用命令行方式向ERP服务器抛送打印请求，这里可以直接在OS上进行测试。

	[root@erpprod]# iconv -f UTF-8 -t GB18030 erp_printer.txt | lpr -Ptestptq -#1 -T"打印测试Oracle ERP"

然后，使用`lpstat`查看OS上打印作业状态，查看RPM上打印作业计数等

注：在测试前，确保打印服务器可以ping通，打印队列和打印服务已经启动；

打印时，可以打印中英文，测试下是否有乱码发生。

##4. ERP上打印队列管理

设置好打印驱动、打印队列后，提交打印请求，更改打印选项，选择测试的打印机，提交请求，查看打印效果。

#脚本

在实际应用中，由于远程打印机、网络、断电重启等原因，时常会出现ERP服务器上打印队列down掉的情况，这时需要手动检查远程打印机的网络是否正常，并重启打印队列。

对于日常维护来说，这会是一件例行事务，若用户要求打印业务需在上班时正常运行，则必须把检查打印队列作为上班时的第一项任务，这样无疑也占用了宝贵的时间。

前面提到过AIX上一些打印队列管理的命令，因此可以编写简单的shell脚本，检查网络、打印队列等，并尝试重启打印队列，再部署成定时任务，出现问题时发送邮件通知。这样可以将时间留给其他更重要的工作。

##1.脚本示意图

![](http://www.dylanninin.com/blog/images/2012/10/checklp.png)

##2.checklp.sh 检查队列

	#!/bin/ksh
	#abstract:
	#check lpstat
	#history:
	#2012-09-04 dylanninin@gmail.com first release
	#variables
	script_basepath=/u1/PROD/prodora/itsection/sys/lpd
	mail_date=$(date +%Y-%m-%d\ %H:%M:%S)
	receipt=dylanninin@gmail.com
	hostname=$(hostname)
	
	#path
	export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
	
	#lpstat
	lpstat_basepath=/var/spool/lpd/stat
	lpstats=${lpstat_basepath}/s.*.@*
	
	#check hosts
	checklp_log=${script_basepath}/checklp.log
	if [ -e ${checklp_log} ]; then
	    true > ${checklp_log}
	else
	    touch ${checklp_log}
	fi
	
	#check ping function
	function check_ping {
	    v_ping=$1
	        if [ ${v_ping} == "" ]; then
	            echo "!!!!!! hostname or ip could not be null or empty!" >> ${checklp_log} 2>&1
	        else
	            ping -c 1 -w 1 ${v_ping} &> /dev/null && result=0 || result=1
	            if [ "${result}" == 0 ]; then
	                echo ">>>>>> Host ${v_ping} is Up!"
	            else
	                echo "!!!!!! Host ${v_ping} is Down!" >> ${checklp_log} 2>&1
	            fi
	        fi
		return
	}
	
	#host list of print queue
	host_list=$(ls -l ${lpstats} | cut -d "@" -f 2 | sort | uniq )
	for v_host in ${host_list}
	do
	     check_ping ${v_host}
	done
	
	office_ip=${script_basepath}/office.ip
	if [ ! -e ${office_ip} ]; then
	    echo "!!!!!! office ip file ${office_ip} does not exist!" >> ${checklp_log} 2>&1
	    exit 0
	fi
	
	#check lpstat
	lplist=$(ls -l ${lpstats} | awk -F "." '{print $2 ":" $3}')
	office_log=${script_basepath}/office.log
	for v_printer in ${lplist}
	do
	    v_queue=$(echo ${v_printer} | cut -d ":" -f 1)
	    v_host=$(echo ${v_printer} | cut -d "@" -f 2)
	    lpstat -W -v${v_queue} > ${office_log} 2>&1
	    v_down=$(grep "DOWN" ${office_log})
	    v_error=$(grep "ERROR" ${office_log})
	    if [ "${v_down}" != "" ]; then
	        v_office=$(echo ${v_queue} | cut -d "-" -f 1)
	        v_ip=$(grep ${v_office} ${officeip} | cut -d ":" -f 2)
	        if [ "${v_ip}" != "" ]; then
	            check_ping ${v_ip}
	        fi
	        echo "${v_down}" >> ${checklp_log} 2>&1
	        #stop queue
	        echo ">>>>>> enq -D -P${v_printer}"
	        enq -D -P${v_printer} > ${restart_log} 2>&1
	        #startup queue
	        echo ">>>>>> enq -U -P${v_printer} ..."
	        enq -U -P${v_printer} > ${restart_log} 2>&1
	    elif [ "${v_error}" != "" ]; then
	        echo "${v_error}" >> ${checklp_log} 2>&1
	    fi
	done
	if [ -e ${office_log} ]; then
	    true > ${office_log}
	fi
	
	#mail
	if [ $(cat ${checklp_log} | wc -l) -gt 0 ]; then
	    cat ${checklp_log} | mail -s "${mail_date}:${hostname} dba daily check of lpstat" ${receipt} 
	fi

##3.office.ip 办事处IP

	xxoffice:192.168.1.111
	xx1office: 192.168.2.111
	xx2office: 192.168.3.111
	... ...
	xxnoffice: 192.168.255.111

##4.restartlp.sh 重启所有队列

	#!/bin/ksh
	#abstract:
	#check lpstat
	#history:
	#2012-09-04     mis_ghb         first release
	#2012-12-04     mis_ghb         restart all lpd queue
	#variables
	script_basepath=/u1/PROD/prodora/itsection/sys/lpd
	mail_date=$(date +%Y-%m-%d\ %H:%M:%S)
	receipt=dylanninin@gmail.com
	hostname=$(hostname)
	
	#path
	export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
	
	#lpstat
	lpstat_basepath=/var/spool/lpd
	lpstats=${lpstat_basepath}/stat/s.*.@*
	lpd_qdir=${lpstat_basepath}/qdir
	
	#check restartlp log file
	restartlp_log=${script_basepath}/restartlp.log
	if [ -e ${restartlp_log} ]; then
	   true > ${restartlp_log}
	else
	   touch ${restartlp_log}
	fi
	
	#check qdir
	qdir_grep=$(ls ${lpd_qdir} | grep -v ".core")
	if [ -e "${qdir_grep}" == "" ]; then
	        ls -l ${lpd_qdir} > ${restartlp_log}
	fi
	
	#check lpstat
	lplist=$(ls -l ${lpstats} | awk -F "." '{print $2 ":" $3}')
	for v_printer in ${lplist}
	do
	    #stop queue
	    echo ">>>>>> enq -D -P${v_printer}"
	    enq -D -P${v_printer} >  ${restart_log} 2>&1
	    #startup queue
	    echo ">>>>>> enq -U -P${v_printer} ..."
	    enq -U -P${v_printer} >  ${restart_log} 2>&1
	done
	
	#mail
	if [ $(cat ${restartlp_log} | wc -l) -gt 0 ]; then
	   cat ${restartlp_log} | mail -s "${mail_date}:${hostname} dba daily check of lpstat" ${receipt} 
	fi

##5.testlp.sh测试打印队列

	#!/bin/ksh
	#abstract:
	#check lpstat
	#history:
	#2012-09-04     mis_ghb         first release
	#variables
	script_basepath=/u1/PROD/prodora/itsection/sys/lpd
	content=${script_basepath}/printer_test.txt
	current_date=$(date +%Y-%m-%d\ %H:%M:%S)
	
	#path
	export PATH=/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin
	
	lpq=$1
	if [ "${lpq}" == "" ]; then
	    echo "print queue must be specified!"
	elif [ ! -e ${content} ]; then
	    echo "print content file ${content} does not exist!"
	else
	    echo "iconv -f UTF-8 -t GB18030 ${content} | lpr -P${lpq} -#1 -T'Print Queue Test on Oracle EBS at ${current_date}'"
	    iconv -f UTF-8 -t GB18030 ${content} | lpr -P${lpq} -#1 -T'Print Queue Test on Oracle EBS at ${current_date}'
	fi

##6. 其他

以上脚本发送的邮件若出现中文乱码，可以使用iconv进行编码转换，如：

	if [ `cat ${sqllog} | wc -l` -gt 0 ]; then
	   iconv -f UTF-8 -t GB18030 ${sqllog} | mail -s "${mail_date}:${hostname} dba daily check of ${script_name}" ${receipt} 
	fi


#参考

* [Microsoft：prnmngr.vbs](http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/prnmngr.mspx?mfr=true)

* IBM AIX Redbook：IBM @server p5 and pSeries Administration and Support for AIX 5L Version 5.3