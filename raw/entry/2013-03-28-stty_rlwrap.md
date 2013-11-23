---
layout: post
title: Stty and rlwrap on Linux
category : Linux
tags : [Linux, Utilities]
---

##退格键
      
在Linux环境下，使用`SQL*Plus`时有时会出现退格键不好使用的情况。此时，可以一般可用使用stty命令来解决。

stty(set tty，设置tty)命令用于检查和修改当前注册的终端的通信参数。UNIX系统为键盘的输入和终端的输出提供了重要的控制手段，可以通过stty命令对特定终端或通信线路设置选项。该命令可以改变并打印终端行设置。

看这个命令的帮助：

	[oracle@dev ~]$ stty --help
	Usage: stty [-F DEVICE] [--file=DEVICE] [SETTING]...
	  or:  stty [-F DEVICE] [--file=DEVICE] [-a|--all]
	  or:  stty [-F DEVICE] [--file=DEVICE] [-g|--save]
	Print or change terminal characteristics.
	
	  -a, --all          print all current settings in human-readable form
	  -g, --save         print all current settings in a stty-readable form
	  -F, --file=DEVICE  open and use the specified DEVICE instead of stdin
	      --help     display this help and exit
	      --version  output version information and exit
	
	Optional - before SETTING indicates negation.  An * marks non-POSIX
	settings.  The underlying system defines which settings are available.
	
	Special characters:
	 * dsusp CHAR    CHAR will send a terminal stop signal once input flushed
	   eof CHAR      CHAR will send an end of file (terminate the input)
	   eol CHAR      CHAR will end the line
	 * eol2 CHAR     alternate CHAR for ending the line
	   erase CHAR    CHAR will erase the last character typed
	   intr CHAR     CHAR will send an interrupt signal
	   kill CHAR     CHAR will erase the current line
	 * lnext CHAR    CHAR will enter the next character quoted
	   quit CHAR     CHAR will send a quit signal
	 * rprnt CHAR    CHAR will redraw the current line
	   start CHAR    CHAR will restart the output after stopping it
	   stop CHAR     CHAR will stop the output
	   susp CHAR     CHAR will send a terminal stop signal
	 * swtch CHAR    CHAR will switch to a different shell layer
	 * werase CHAR   CHAR will erase the last word typed
	
	Special settings:
	  N             set the input and output speeds to N bauds
	 * cols N        tell the kernel that the terminal has N columns
	 * columns N     same as cols N
	   ispeed N      set the input speed to N
	 * line N        use line discipline N
	   min N         with -icanon, set N characters minimum for a completed read
	   ospeed N      set the output speed to N
	 * rows N        tell the kernel that the terminal has N rows
	 * size          print the number of rows and columns according to the kernel
	   speed         print the terminal speed
	   time N        with -icanon, set read timeout of N tenths of a second
	……
	Handle the tty line connected to standard input.  Without arguments,
	prints baud rate, line discipline, and deviations from stty sane.  In
	settings, CHAR is taken literally, or coded as in ^c, 0x37, 0177 or
	127; special values ^- or undef used to disable special characters.
	
	Report bugs to <bug-coreutils@gnu.org>. 
 
与退格键相关的设置是erase，它表示删除最后一个字符。

	$stty erase ^H

说明：按下退格键会显示成^H。 如果在当前窗口执行的话，只对当前的窗口有效，下次登陆的时候还需要重新设置，可以把这个命令写入shell 的配置文件，如`~/.bashrc` 中，这样每次都能生效了。
 
##方向键

Windows下使用方向键是没有问题的，但是在Linux下，方向键是使用不了。此时可以安装一下rlwrap工具。

	SQL> ^[[A	----[按方向键会显示异常]

rlwrap本身是个遵循GPL 标准的Shell 脚本，可以运行任何你提供给它的命令包括参数，并添加命令历史浏览功能。

1) 关于rlwrap

	[root@dev ~]# yum info rlwrap
	Loaded plugins: fastestmirror, refresh-packagekit, security
	Determining fastest mirrors
	base                                                                                                                                             | 1.3 kB     00:00     
	extras                                                                                                                                           | 1.3 kB     00:00     
	Installed Packages
	Name        : rlwrap
	Arch        : x86_64
	Version     : 0.37
	Release     : 1.el6
	Size        : 196 k
	Repo        : installed
	From repo   : extras
	Summary     : Wrapper for GNU readline
	URL         : http://utopia.knoware.nl/~hlub/rlwrap/
	License     : GPLv2+
	Description : rlwrap is a 'readline wrapper' that uses the GNU readline library to
	            : allow the editing of keyboard input for any other command. Input
	            : history is remembered across invocations, separately for each command;
	            : history completion and search work as in bash and completion word
	            : lists can be specified on the command line.

2) 安装rlwrap

	[root@dev soft]# yum install -y rlwrap
 
3) 测试

	[oracle@dev ~]$ rlwrap sqlplus / as sysdba
	
	SQL*Plus: Release 10.2.0.1.0 - Production on Wed Jun 27 17:42:50 2012
	
	Copyright (c) 1982, 2005, Oracle.  All rights reserved.
	
	
	Connected to:
	Oracle Database 10g Enterprise Edition Release 10.2.0.1.0 - Production
	With the Partitioning, OLAP and Data Mining options
	
	SQL> select * from v$version;
	
	BANNER
	----------------------------------------------------------------
	Oracle Database 10g Enterprise Edition Release 10.2.0.1.0 - Prod
	PL/SQL Release 10.2.0.1.0 - Production
	CORE	10.2.0.1.0	Production
	TNS for Linux: Version 10.2.0.1.0 - Production
	NLSRTL Version 10.2.0.1.0 - Production
	
	SQL> select * from v$version; --[按方向键可用正常输入]

现在就可以上下翻动了。 

4) 设置别名

但是这样没事都需要加上rlwrap 也是很麻烦的，可以对rlwrap 做一个别名，放到shell 的配置文件里，在`~/.bashrc` 文件里添加如下内容：

	alias sqlplus='rlwrap sqlplus'

5) 让参数生效

	[oracle@dev ~]$  source ~/.bashrc   

6) 测试

	[oracle@dev ~]$ type sqlplus
	sqlplus is aliased to `rlwrap sqlplus'
	
	[oracle@dev ~]$ $ sqlplus / as sysdba
	SQL*Plus: Release 10.2.0.1.0 - Production on Wed Jun 27 17:42:50 2012
	
	Copyright (c) 1982, 2005, Oracle.  All rights reserved.
	
	
	Connected to:
	Oracle Database 10g Enterprise Edition Release 10.2.0.1.0 - Production
	With the Partitioning, OLAP and Data Mining options
	
	SQL> select * from v$version;
	
	BANNER
	----------------------------------------------------------------
	Oracle Database 10g Enterprise Edition Release 10.2.0.1.0 - Prod
	PL/SQL Release 10.2.0.1.0 - Production
	CORE	10.2.0.1.0	Production
	TNS for Linux: Version 10.2.0.1.0 - Production
	NLSRTL Version 10.2.0.1.0 - Production
	
	SQL> select * from v$version; --[按方向键可用正常输入]
 
其他一些组合键：

	Ctrl+A：ahead，到行的顶端，相当于 Home
	Ctrl+E：end，到行的末端，相当于end
	Ctrl+B：behind，后退一个字符，相当于left
	Ctrl+F：forward，前进一个子放入，相当于right
	Ctrl+P：prev.，上一行历史记录，相当于up
	Ctrl+N：next.，下一行历史记录，相当于down
	Ctrl+U：undo，回复操作，这行就被清空掉了
	Ctrl+W：剪切
	Ctrl+Y：粘贴
	Ctrl+L：cLear，清屏

##参考

* [Linux下`SQL*Plus`退格、方向键问题](http://blog.csdn.net/tianlesoftware/article/details/6168219)
* [利用Uniread解决Linux下的`SQL*Plus`命令历史回调功能](http://dbanotes.net/tech-memo/uniread-howto.html)
* [Another tool for ‘Command Line History’](http://dbanotes.net/database/another_tool_for_command_line_history.html#more-99)