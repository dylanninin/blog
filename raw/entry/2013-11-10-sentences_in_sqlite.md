---
layout: post
title: Sentences in SQLite 3
category : Miscellanies
tags : [SQLite, Rails]
---

拖同学和朋友帮忙，最近看Rails，第一份教材自然是[Agile Web Development with Rails 4](http://book.douban.com/subject/24718727/)。

其中谈到SQLite 3是Rails的默认数据库，使用SQLite省去了安装和创建数据库、创建账户、分配权限等步骤，可以使开发人员的精力集中在项目开发上；等到部署和投入使用时，再根据应用和业务特点选择合适的数据库产品，此时SQLite就不一定适合了。

比起SQLite这类嵌入式数据库，常见的CS架构的数据库产品的安装、配置、使用、维护等一般是非常耗时的，此时可能需要一个专职的DBA来支撑，安装数据库软件、创建数据库、创建用户、分配权限等看似很简单，但看看[OS Preparation for Oracle Database](http://dylanninin.com/blog/2013/07/19/os_preparation_for_oracle.html)、 [Manually Creating Oracle Database On Linux](http://dylanninin.com/blog/2012/10/01/manually_creating_oradb_on_linux.html)、[Users, Roles, Privileges in Oracle Database](http://dylanninin.com/blog/2013/03/07/user_roles_privileges.html)就知道这些步骤有多么复杂了。 对于适合Rails开发的Mac、Ubuntu本本来说，运行Oracle这类数据库实在太暴殄天物，估计没人干这事儿吧！此时选择SQLite是多么的合适，不需要单独运行的数据库，也不需要额外的网络配置。Rails选择SQLite作为默认的数据库可以说是它宣称"Agile"的一个有力例证。 

旧习难改，忍不住去看了下SQLite的介绍，设计哲学，SQL教程，日常使用以及开发教程，不得不说，[The Definitive Guide to SQLite](http://book.douban.com/subject/5392299/)是一本好书，概念阐述得清晰到位，配图也很经典，让人真正体会到什么是一图胜万言。

比如这张讲`SELECT`语句处理过程的：

![SELECT](http://dylanninin.com/assets/images/2013/sqlite_sql_select.png)

当然，书中文笔也是很优美、很流畅的，所以看到一图胜万言时，也不要忘记认细读。这不，我就顺手摘抄了其中的一些好句子，与大家共赏。

##The Definitive Guide to SQLite 

The Definitive Guide to SQLite 

* The eXperT’s Voice ® in open source. Take control of this compact and powerful tool to embed sophisticated SQL databases within your applications.

The API is both well documented and intuitive.

* As a programming library, SQLite’s API is one of the simplest and easiest to use. The API is both well documented and intuitive.It is designed to help you customize SQLite in many ways, such as implementing your own custom SQL functions in C. The open source community also has a created a vast number of language and library interfaces with which to use SQLite. There are extensions for Perl, Python, Ruby, Tcl/Tk, Java, PHP, Visual Basic, ODBC, Delphi, C#, VB .NET, Smalltalk, Ada, Objective C, Eiffel, Rexx, Lisp, Scheme, Lua, Pike, Objective Camel, Qt, WxWindows, REALBASIC, and others. You can find an exhaustive list on the SQLite wiki: www.sqlite.org/cvstrac/wiki?p=SqliteWrappers. 

For their particular application, Informix was somewhat overkill. For an experienced database administrator (DBA) at the time, it could take almost an entire day to install or upgrade. To the uninitiated application programmer, it might take forever.

* SQLite was conceived on a battleship...well, sort of. SQLite’s author, D. Richard Hipp, was working for General Dynamics on a program for the U.S. Navy developing software for use on board guided missile destroyers. The program originally ran on Hewlett-Packard Unix (HP-UX) and used an Informix database as the back end. For their particular application, Informix was somewhat overkill. For an experienced database administrator (DBA) at the time, it could take almost an entire day to install or upgrade. To the uninitiated application programmer, it might take forever. What was really needed was a self-contained database that was easy to use and that could travel with the program and run anywhere regardless of what other software was or wasn’t installed on the system. 

SQLite contains just enough features to fit in a single programmer’s brain, and like its library, it requires as small a footprint in the gray matter as it does in RAM.

* From its initial conception, SQLite has been designed so that it can be incorporated and used without the need of a DBA. Configuring and administering SQLite is as simple as it gets. SQLite contains just enough features to fit in a single programmer’s brain, and like its library, it requires as small a footprint in the gray matter as it does in RAM.

It is not that SQLite is incapable of working over a network file system because of anything in its implementation. Rather, SQLite is at the mercy of the underlying file system and wire protocol, and those technologies are not always perfect. 

* Although SQLite databases can be shared over network file systems, the latency associated with such file systems can cause performance to suffer. Worse, bugs in network file system implementations can also make opening and modifying remote files—SQLite or otherwise—error prone. If the file system’s locking does not work properly, two clients may be allowed to simultaneously modify the same database file, which will almost certainly result in database corruption. It is not that SQLite is incapable of working over a network file system because of anything in its implementation. Rather, SQLite is at the mercy of the underlying file system and wire protocol, and those technologies are not always perfect. For instance, many versions of NFS have a flawed fcntl() implementation, meaning that locking does not behave as intended. Newer NFS versions, such are Solaris NFS v4, work just fine and reliably implement the requisite locking mechanisms needed by SQLite. However, the SQLite developers have neither the time nor the resources to certify that any given network file system works flawlessly in all cases.  

These limitations are in line with its intended purpose.

* So, there are situations where SQLite is not as fast as larger databases. But many if not all of these conditions are to be expected. SQLite is an embedded database designed for small to medium-sized applications. These limitations are in line with its intended purpose. Many new users make the mistake of assuming that they can use SQLite as a drop-in replacement for larger relational databases. Sometimes you can; sometimes you can’t. It all depends on what you are trying to do. 

In short, what SQLite can’t do is a direct result of what it can.

* Again, most of these limitations are intentional, resulting from SQLite’s design. Supporting high write concurrency, for example, brings with it great deal of complexity, and this runs counter to SQLite’s simplicity in design. Similarly, being an embedded database, SQLite intentionally does not support networking. This should come as no surprise. In short, what SQLite can’t do is a direct result of what it can. It was designed to operate as a modular, simple, compact, and easy-to-use embedded relational database whose code base is within the reach of the programmers using it. And in many respects, it can do what many other databases cannot, such as run in embedded environments where actual power consumption is a limiting factor. 

No matter how good you think your chosen backup approach is, remember you are only as good as your last successful restore. Test your restore procedure if you need to rely on it—otherwise, you’ll be remembered for one failed restore, regardless of how many successful backups you took. 

##SQLite in Rails Application

###Development

For this application, we’ll use the open source SQLite database (which you’ll need if you’re following along with the code). We’re using SQLite version 3 here.

SQLite 3 is the default database for Rails development and was installed along with Rails (in Chapter 1, Installing Rails, on page 3). With SQLite 3 there are no steps required to create a database, and there are no special user accounts or passwords to deal with. So, now you get to experience one of the benefits of going with the flow (or, convention over configuration, as Rails folks say...ad nauseam).

If it’s important to you to use a database server other than SQLite 3, the commands you’ll need to create the database and grant permissions will be different. You will find some helpful hints in the Getting Started Rails Guide.

###Deployment and Production

The SQLite website is refreshingly honest when it comes to describing what this database is good at and what is not good at. In particular, SQLite is not recommended for high-volume, high-concurrency websites with large datasets. And, of course, we want our website to be such a website . 

##Reference

* [Agile Web Development with Rails 4](http://book.douban.com/subject/24718727/)
* [The Definitive Guide to SQLite](http://book.douban.com/subject/5392299/) 
* [SQLite Introduction](http://dylanninin.com/blog/2012/12/19/sqlite.html)
* [为什么会有这么多中的数据库](http://www.aqee.net/what-databases-fix/)
* [What Databases Fix](http://cargocultcoder.blogspot.se/2012/12/what-databases-fix.html)