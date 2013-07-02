#gzip

gzip 可以说是应用度最广的压缩命令了！目前 gzip 可以解开 compress, zip 与 gzip 等软件所压缩的文件。

##gzip help

	[root@server Workspace]# gzip -h
	Usage: gzip [OPTION]... [FILE]...
	Compress or uncompress FILEs (by default, compress FILES in-place).
	
	Mandatory arguments to long options are mandatory for short options too.
	
	  -c, --stdout      write on standard output, keep original files unchanged
	  -d, --decompress  decompress
	  -f, --force       force overwrite of output file and compress links
	  -h, --help        give this help
	  -l, --list        list compressed file contents
	  -L, --license     display software license
	  -n, --no-name     do not save or restore the original name and time stamp
	  -N, --name        save or restore the original name and time stamp
	  -q, --quiet       suppress all warnings
	  -r, --recursive   operate recursively on directories
	  -S, --suffix=SUF  use suffix SUF on compressed files
	  -t, --test        test compressed file integrity
	  -v, --verbose     verbose mode
	  -V, --version     display version number
	  -1, --fast        compress faster
	  -9, --best        compress better
	    --rsyncable   Make rsync-friendly archive
	
	With no FILE, or when FILE is -, read standard input.
	
	Report bugs to <bug-gzip@gnu.org>.

##用法

压缩

	[test@server ~]$ gzip -v netstat.log 
	netstat.log:	 93.0% -- replaced with netstat.log.gz
	[test@server ~]$ ll
	total 4
	-rw-rw-r-- 1 test test 1868 Mar 11 17:11 netstat.log.gz

继续压缩

	[test@server ~]$ gzip -v netstat.log.gz 
	gzip: netstat.log.gz already has .gz suffix -- unchanged
	[test@server ~]$ gzip -v -S .gz netstat.log.gz -c > netstat.log.gz.gz
	netstat.log.gz:	  0.2%
	[test@server ~]$ ll
	total 8
	-rw-rw-r-- 1 test test 1799 Mar 11 16:12 netstat.log.gz
	-rw-rw-r-- 1 test test 1837 Mar 11 16:17 netstat.log.gz.gz

解压缩

	[test@server ~]$ gzip -v -d netstat.log.gz 
	netstat.log.gz:	 93.0% -- replaced with netstat.log

测试完整性
	
	[test@server ~]$ gzip -v -t netstat.log.gz 
	netstat.log.gz:	 OK

	[test@server ~]$ touch dummy.gz;gzip -v -t dummy.gz

	gzip: dummy.gz: unexpected end of file

列表文件

	[test@server ~]$ gzip -v -l netstat.log.gz 
	method  crc     date  time           compressed        uncompressed  ratio uncompressed_name
	defla 73d6b845 Mar 11 16:12                1799               25013  93.0% netstat.log

##特点

1.仅能对单个文件（即输入一个文件，输出一个文件）

	[test@server ~]$ mkdir -p foo/bar
	[test@server ~]$ free > foo/free.log
	[test@server ~]$ netstat > foo/bar/netstat.log
	[test@server ~]$ tree .
	.
	└── foo
	    ├── bar
	    │   └── netstat.log
	    └── free.log
	
	2 directories, 2 files
	[test@server ~]$ gzip foo/
	gzip: foo/ is a directory -- ignored
	[test@server ~]$ gzip foo/*
	gzip: foo/bar is a directory -- ignored

2.通过递归，支持对文件夹的压缩(`gzip -r`)，但解压缩需单独一一进行

	[test@server ~]$ gzip -v -r foo/
	foo//bar/netstat.log:	 92.5% -- replaced with foo//bar/netstat.log.gz
	foo//free.log:	 44.8% -- replaced with foo//free.log.gz

3.默认情况下，gzip压缩后的文件后缀名为.gz(`gzip -S ".your_suffix"`)

	[test@server ~]$ gzip -v -S ".gzip" passwd 
	passwd:	 61.4% -- replaced with passwd.gzip

gzip默认后缀为.gz，当更改后缀名后，解压时，需要指定后缀名

	[test@server ~]$ gzip -v -d passwd.gzip 
	gzip: passwd.gzip: unknown suffix -- ignored
	[test@server ~]$ gzip -v -d -S ".gzip" passwd.gzip 
	passwd.gzip:	 61.4% -- replaced with passwd

4.压缩、解压缩时，保留原有文件权限

压缩前，文件权限

	[root@server ~]# ll
	total 4
	-rw-r--r-- 1 root root   5 Mar 11 16:49 whoami.log

更改权限为777

	[root@server ~]# chmod 777 whoami.log 
	[root@server ~]# chown test:test whoami.log 

压缩后，文件权限

	[root@server ~]# gzip -v whoami.log 
	whoami.log:	120.0% -- replaced with whoami.log.gz
	[root@server ~]# ll
	total 4
	-rwxrwxrwx 1 test test  36 Mar 11 16:49 whoami.log.gz

解压后，文件权限

	[root@server ~]# gzip -v -d whoami.log.gz 
	whoami.log.gz:	120.0% -- replaced with whoami.log
	[root@server ~]# ll
	total 4
	-rwxrwxrwx 1 test test   5 Mar 11 16:49 whoami.log

注：在使用 gzip -c 配合 > 重定向时，相当于创建文件，此时文件权限为于当前用户设定的权限。

5.压缩时，默认状态下，原文件会被压缩后的文件替换；解压时类似

此时，可以使用`gzip -c > your_file_name`来重定向输出文件，同时保存原有文件。不指定文件时，默认会输出到标准输出stdout上。

压缩

	[test@server ~]$ gzip -v -S .gz netstat.log.gz -c > netstat.log.gz.gz
	netstat.log.gz:	  0.2%
	[test@server ~]$ ll
	total 8
	-rw-rw-r-- 1 test test 1799 Mar 11 16:12 netstat.log.gz
	-rw-rw-r-- 1 test test 1837 Mar 11 16:17 netstat.log.gz.gz

解压缩

	[root@server ~]# gzip -vdc whoami.log.gz > whoami
	whoami.log.gz:	120.0%
	[root@server Workspace]# ll
	total 8
	-rw-r--r-- 1 root root  5 Mar 11 17:08 whoami
	-rw-r--r-- 1 test test 36 Mar 11 17:04 whoami.log.gz


6.压缩后的文本文件可以直接使用zcat读出(zcat your_file_name.gz)

	[test@server ~]$ zcat netstat.log.gz 
	Active Internet connections (w/o servers)
	Proto Recv-Q Send-Q Local Address               Foreign Address             State  
	... ...

- - -

#bzip2

若说 gzip 是为了取代 compress 并提供更好的压缩比而成立的，那么 bzip2 则是为了取代 gzip 并提供更佳的压缩比而来的。 bzip2 真是很不错用的东西～这玩意的压缩比竟然比 gzip 还要好～至於 bzip2 的用法几乎与 gzip 相同！

##bzip help

	[root@server svn]# bzip2 --help
	bzip2, a block-sorting file compressor.  Version 1.0.5, 10-Dec-2007.
	
	   usage: bzip2 [flags and input files in any order]
	
	   -h --help           print this message
	   -d --decompress     force decompression
	   -z --compress       force compression
	   -k --keep           keep (don't delete) input files
	   -f --force          overwrite existing output files
	   -t --test           test compressed file integrity
	   -c --stdout         output to standard out
	   -q --quiet          suppress noncritical error messages
	   -v --verbose        be verbose (a 2nd -v gives more)
	   -L --license        display software version & license
	   -V --version        display software version & license
	   -s --small          use less memory (at most 2500k)
	   -1 .. -9            set block size to 100k .. 900k
	   --fast              alias for -1
	   --best              alias for -9
	
	   If invoked as `bzip2', default action is to compress.
	              as `bunzip2',  default action is to decompress.
	              as `bzcat', default action is to decompress to stdout.
	
	   If no file names are given, bzip2 compresses or decompresses
	   from standard input to standard output.  You can combine
	   short flags, so `-v -4' means the same as -v4 or -4v, &c.

##使用
gzip的替代工具bzip2，压缩比较gzip高，用法与gzip类似，不再赘述。

1.压缩后的文本文件可以直接使用bzcat读出

	[root@server ~]# bzcat netstat.log.bz2 
	Active Internet connections (w/o servers)
	Proto Recv-Q Send-Q Local Address               Foreign Address             State  
	... ...

- - -

#tar

##tar help

	[test@server ~]$ tar --help
	Usage: tar [OPTION...] [FILE]...
	GNU `tar' saves many files together into a single tape or disk archive, and can
	restore individual files from the archive.
	
	Examples:
	  tar -cf archive.tar foo bar  # Create archive.tar from files foo and bar.
	  tar -tvf archive.tar         # List all files in archive.tar verbosely.
	  tar -xf archive.tar          # Extract all files from archive.tar.
	
	... ...

##用法

tar用法很多，具体用法，可用使用tar --help或者man tar查看。

tar仅作打包用，即可用将多个文件，文件夹打包成单个文件，并不会压缩文件，若需要压缩，可用结合前面提到的gzip,bzip2命令。

##增量备份与恢复

	[test@server ~]$ mkdir backup
	[test@server ~]$ ll
	total 8
	drwxrwxr-x 2 test test 4096 Mar 11 17:34 backup
	drwxrwxr-x 3 test test 4096 Mar 11 17:29 inc0

增量备份

	[test@server ~]$ tar -cjvpf backup/inc0.tar.bz2 -g backup/snapshot.snar inc0/
	tar: inc0: Directory is new
	tar: inc0/foo: Directory is new
	tar: inc0/foo/bar: Directory is new
	tar: inc0/foo/bar/foobar: Directory is new
	inc0/
	inc0/foo/
	inc0/foo/bar/
	inc0/foo/bar/foobar/
	inc0/netstat.log.gz
	inc0/netstat.log.gz.gz
	inc0/test.tar

	[test@server ~]$ cd backup/
	[test@server backup]$ ll
	total 8
	-rw-rw-r-- 1 test test 3324 Mar 11 17:34 inc0.tar.bz2
	-rw-rw-r-- 1 test test  274 Mar 11 17:34 snapshot.snar

更新inc0下的文件

	[test@server ~]$ mkdir -p inc0/foo/fooo/barrr
	[test@server ~]$ uptime > inc0/foo/bar/uptime.log
	[test@server ~]$ rm inc0/test.tar 

基于inc0做增量备份

	[test@server ~]$ tar -cjvpf backup/inc1.tar.bz2 -g backup/snapshot.snar inc0/
	tar: inc0/foo/fooo: Directory is new
	tar: inc0/foo/fooo/barrr: Directory is new
	inc0/
	inc0/foo/
	inc0/foo/bar/
	inc0/foo/bar/foobar/
	inc0/foo/fooo/
	inc0/foo/fooo/barrr/
	inc0/foo/bar/uptime.log

	[test@server ~]$ cd backup/
	[test@server backup]$ ll
	total 12
	-rw-rw-r-- 1 test test 3324 Mar 11 17:34 inc0.tar.bz2
	-rw-rw-r-- 1 test test  397 Mar 11 17:36 inc1.tar.bz2
	-rw-rw-r-- 1 test test  412 Mar 11 17:36 snapshot.snar

	[test@server backup]$ tar -jtvf  inc0.tar.bz2 
	drwxrwxr-x test/test        51 2013-03-11 17:29 inc0/
	drwxrwxr-x test/test         6 2013-03-11 17:21 inc0/foo/
	drwxrwxr-x test/test         9 2013-03-11 17:21 inc0/foo/bar/
	drwxrwxr-x test/test         1 2013-03-11 17:21 inc0/foo/bar/foobar/
	-rw-rw-r-- test/test      1868 2013-03-11 17:11 inc0/netstat.log.gz
	-rw-rw-r-- test/test      1906 2013-03-11 17:11 inc0/netstat.log.gz.gz
	-rw-rw-r-- test/test     10240 2013-03-11 17:21 inc0/test.tar

	[test@server backup]$ tar -jtvf  inc1.tar.bz2 
	drwxrwxr-x test/test        41 2013-03-11 17:35 inc0/
	drwxrwxr-x test/test        12 2013-03-11 17:34 inc0/foo/
	drwxrwxr-x test/test        21 2013-03-11 17:35 inc0/foo/bar/
	drwxrwxr-x test/test         1 2013-03-11 17:21 inc0/foo/bar/foobar/
	drwxrwxr-x test/test         8 2013-03-11 17:34 inc0/foo/fooo/
	drwxrwxr-x test/test         1 2013-03-11 17:34 inc0/foo/fooo/barrr/
	-rw-rw-r-- test/test        71 2013-03-11 17:35 inc0/foo/bar/uptime.log

恢复文件

	[test@server ~]$ mkdir restore
	[test@server ~]$ tar -xjvpf backup/inc0.tar.bz2 -C restore/
	inc0/
	inc0/foo/
	inc0/foo/bar/
	inc0/foo/bar/foobar/
	inc0/netstat.log.gz
	inc0/netstat.log.gz.gz
	inc0/test.tar

	[test@server ~]$ tar -xjvpf backup/inc1.tar.bz2 -C restore/
	inc0/
	inc0/foo/
	inc0/foo/bar/
	inc0/foo/bar/foobar/
	inc0/foo/fooo/
	inc0/foo/fooo/barrr/
	inc0/foo/bar/uptime.log

	[test@server ~]$ tree restore/
	restore/
	└── inc0
	    ├── foo
	    │   ├── bar
	    │   │   ├── foobar
	    │   │   └── uptime.log
	    │   └── fooo
	    │       └── barrr
	    ├── netstat.log.gz
	    ├── netstat.log.gz.gz
	    └── test.tar
	
	6 directories, 4 files

修改文件，再次做增量备份

	[test@server ~]$ cat inc0/foo/bar/uptime.log 
	 17:35:09 up 65 days,  6:38,  2 users,  load average: 0.00, 0.00, 0.00
	[test@server ~]$ uptime >> inc0/foo/bar/uptime.log 
	[test@server ~]$ tar -cjvpf backup/inc2.tar.bz2 -g backup/snapshot.snar inc0/
	inc0/
	inc0/foo/
	inc0/foo/bar/
	inc0/foo/bar/foobar/
	inc0/foo/fooo/
	inc0/foo/fooo/barrr/
	inc0/foo/bar/uptime.log

恢复文件

	[test@server ~]$ cat restore/inc0/foo/bar/uptime.log 
	 17:35:09 up 65 days,  6:38,  2 users,  load average: 0.00, 0.00, 0.00
	[test@server ~]$ tar -xjvpf backup/inc2.tar.bz2 -C restore/
	inc0/
	inc0/foo/
	inc0/foo/bar/
	inc0/foo/bar/foobar/
	inc0/foo/fooo/
	inc0/foo/fooo/barrr/
	inc0/foo/bar/uptime.log

	[test@server ~]$ cat restore/inc0/foo/bar/uptime.log 
	 17:35:09 up 65 days,  6:38,  2 users,  load average: 0.00, 0.00, 0.00
	 17:43:39 up 65 days,  6:47,  2 users,  load average: 0.01, 0.01, 0.00

	[test@server ~]$ mkdir restore2
	[test@server ~]$ tar -xjvpf backup/inc2.tar.bz2 -C restore2
	inc0/
	inc0/foo/
	inc0/foo/bar/
	inc0/foo/bar/foobar/
	inc0/foo/fooo/
	inc0/foo/fooo/barrr/
	inc0/foo/bar/uptime.log
	[test@server ~]$ tree restore2/
	restore2/
	└── inc0
	    └── foo
	        ├── bar
	        │   ├── foobar
	        │   └── uptime.log
	        └── fooo
	            └── barrr
	
	6 directories, 1 file
	[test@server ~]$ cat restore2/inc0/foo/bar/uptime.log 
	 17:35:09 up 65 days,  6:38,  2 users,  load average: 0.00, 0.00, 0.00
	 17:43:39 up 65 days,  6:47,  2 users,  load average: 0.01, 0.01, 0.00

- - -

#split	

split即一款分割文件的小工具，可以根据设定的大小（如行数、字节数等）将一个文件等分成更小的文件。若文件大小超出文件系统支持的单文件最大值，或由于网络传输的限制，此时将大文件切分成同等大小的小文件，则可以很好的解决这些问题。

##split help

	[test@server ~]$ split --help
	Usage: split [OPTION]... [INPUT [PREFIX]]
	Output fixed-size pieces of INPUT to PREFIXaa, PREFIXab, ...; default
	size is 1000 lines, and default PREFIX is `x'.  With no INPUT, or when INPUT
	is -, read standard input.
	
	Mandatory arguments to long options are mandatory for short options too.
	  -a, --suffix-length=N   use suffixes of length N (default 2)
	  -b, --bytes=SIZE        put SIZE bytes per output file
	  -C, --line-bytes=SIZE   put at most SIZE bytes of lines per output file
	  -d, --numeric-suffixes  use numeric suffixes instead of alphabetic
	  -l, --lines=NUMBER      put NUMBER lines per output file
	      --verbose           print a diagnostic just before each
	                            output file is opened
	      --help     display this help and exit
	      --version  output version information and exit
	
	SIZE may be (or may be an integer optionally followed by) one of following:
	KB 1000, K 1024, MB 1000*1000, M 1024*1024, and so on for G, T, P, E, Z, Y.
	
	Report split bugs to bug-coreutils@gnu.org
	GNU coreutils home page: <http://www.gnu.org/software/coreutils/>
	General help using GNU software: <http://www.gnu.org/gethelp/>
	For complete documentation, run: info coreutils 'split invocation'

##使用
查看文件大小

	[root@server ~]# ll -h
	total 4.0K
	-rw-r--r-- 1 root root 1.5K Mar 12 10:19 netstat.log.bz2

按bytes分割文件

	[root@server ~]# split -d -b 1K netstat.log.bz2 netstat.log.bz2.
	[root@server ~]# ll -h
	total 12K
	-rw-r--r-- 1 root root 1.5K Mar 12 10:19 netstat.log.bz2
	-rw-r--r-- 1 root root 1.0K Mar 12 10:22 netstat.log.bz2.00
	-rw-r--r-- 1 root root  500 Mar 12 10:22 netstat.log.bz2.01

测试分割后文件的完整性

	[root@server ~]# bzip2 -v -t netstat.log.bz2.00 
	  netstat.log.bz2.00: file ends unexpectedly
	
	You can use the `bzip2recover' program to attempt to recover
	data from undamaged sections of corrupted files.
	
	[root@server ~]# bzip2 -v -t netstat.log.bz2.01 
	  netstat.log.bz2.01: bad magic number (file not created by bzip2)
	
	You can use the `bzip2recover' program to attempt to recover
	data from undamaged sections of corrupted files.
	
合并分割后的文件

	[root@server ~]# cat netstat.log.bz2.0[0-1] > netstat.log.recover.bz2

测试合并后文件的完整性

	[root@server ~]# bzip2 -v -t netstat.log.recover.bz2 
	  netstat.log.recover.bz2: ok

注意

	-a  指定后缀名的长度。根据数字或字母，可以确定分割后的最大文件数
		如果后缀为数字[0-9]，则分割后最多有 10 ** ${suffix_length};
		如果后缀为字母[a-z]，则分割后最多有 26 ** ${suffix_length};

通常在使用split分割文件前，根据原文件大小，分割后大小，估算下分割后文件数量，以此确定合适的分割分割后缀和后缀长度，否则可能出现后缀不够用的情况。

查看要分割的文件大小

	[test@server ~]$ wc netstat.log 
	  302  1918 23945 netstat.log

按行分割文件

	[test@server ~]$ split -a 2 -d -l 2 --verbose netstat.log netstat.log.
	creating file `netstat.log.00'
	... ...
	creating file `netstat.log.99'
	split: output file suffixes exhausted

该文件有302行，按2行一个文件进行分割，则会产生151(302/2)个文件。但在分割时，使用数字为后缀，长度为2，则最多能够产生 10 ** 2 = 100个文件，显然不够用。

#选型
组合：tar,bzip2,split。其中tar负责打包文件，bzip2负责压缩，split负责文件分割。

其他：rsync,inotify,sha1sum。rsync负责文件镜像，inotify负责文件实时监控，sha1sum负责文件校验。

##测试

边打包、压缩，边分割

	tar -g snapshot/snapshot.snar -cjpvf - source | split -a 3 -b 1K - backup/backup_201303121100.tar.bz2.

注：	

	tar 选项

	-c  创建新的归档文件
	-j  使用bzip2压缩归档文件
	-g  即--listed-incremental 指定增量备份
	-p  归档时保留文件权限
	-f  指定归档文件
	-   stdout
	
	split 选项

	-a  指定后缀名的长度。根据数字或字母，确定分割后的最大文件数
		如果后缀为数字[0-9]，则分割后最多有 10 ** ${suffix_length};
		如果后缀为字母[a-z]，则分割后最多有 26 ** ${suffix_length};
	-b  指定分割大小，以字节为单位
	-   stdin

	[root@server ~]# tree .
	.
	├── backup
	│   ├── backup_201303121100.tar.bz2.aaa
	│   ├── backup_201303121100.tar.bz2.aab
	│   └── backup_201303121100.tar.bz2.aac
	├── snapshot
	│   └── snapshot.snar
	└── source
	     ... ...

测试分割后的文件	

	[root@server backup]# tar -tf backup_201303121100.tar.bz2.aaa 

	bzip2: Compressed file ends unexpectedly;
		perhaps it is corrupted?  *Possible* reason follows.
	bzip2: Inappropriate ioctl for device
		Input file = (stdin), output file = (stdout)
	
	It is possible that the compressed file(s) have become corrupted.
	You can use the -tvv option to test integrity of such files.
	
	You can use the `bzip2recover' program to attempt to recover
	data from undamaged sections of corrupted files.
	
	tar: Child returned status 2
	tar: Error is not recoverable: exiting now

合并分割后的文件

	[root@server backup]# cat * > backup_201303121100.tar.bz2

查看要恢复的文件

	[root@server backup]# tar -tf backup_201303121100.tar.bz2
	source/
	source/foo/
	source/foo/bar/
	source/foo/bar/fooo/
	source/0
	source/1

	[root@server backup]# tar -tf backup_201303121100.tar.bz2 | grep 50
	source/50

解压指定的文件

	[root@server backup]# tar -xjvf backup_201303121100.tar.bz2 source/50
	source/50

查看文件

	[root@server backup]# tree source/
	source/
	└── 50
	
	0 directories, 1 file

- - -

#参考
* [鸟哥的私房菜 文件与文件系统的压缩与打包](http://vbird.dic.ksu.edu.tw/linux_basic/0240tarcompress.php)
* [rsync wikipedia](http://en.wikipedia.org/wiki/Rsync)
* [inotify wikipedia](http://en.wikipedia.org/wiki/Inotify)