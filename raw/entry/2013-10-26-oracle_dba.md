---
layout: post
title: Oracel DBA
category: Miscellanies
tags: [Oracle, Database, DBA, Resource]
---

DBA，即Database Administrator，数据库管理员，是负责管理和维护数据库的人。

DBA负责全面管理和维护数据库，从工作内容上讲，贯穿了一个数据库的整个服务周期，如数据库安装和创建， 网络和客户端配置，用户权限、数据库对象、存储和实例的管理与维护，日常问题的诊断和处理，系统性能监 控和调优，备份与恢复策略的定制与测试，高可用性环境的规划与实施，历史数据的切割与归档，数据库软件 的维护与升级，以及数据库的迁移等，确保数据库可用、安全和可靠。

不同公司分工明细度不同，DBA的职责也不尽相同，管理和维护数据库是DBA的必备技能，但随着发展，每个DBA 会有各自的研究方向和专长，如性能调优，备份与恢复，高可用性，内部原理等。一般来讲，DBA的定义更为宽 泛，除了数据库的全面管理和维护，DBA还需兼任SA(System Administrator)、SDE(Software Development Engineer)的部分工作；因此按面向的工作内容，DBA又可以分为运维DBA、开发DBA、应用DBA（如ERP DBA）等。

DBA的成长不易，DBA要经过入门、初级、中级、高级、资深、顶级等阶段，算起来，可能又是一个本硕博连读 的时间。只是不少人在入门阶段就会身陷泥淖左右彷徨而不得其法，导致多走弯路、耗费青春。陈吉平在《构 建Oracle高可用环境--企业级高可用数据库架构、实战与经验总结》中提到，“不管任何行业，高级的人才总是 奇缺，而低端的人总是遍地都是，永恒的金字塔结构持续了一年又一年。如果你不想做金字塔的最低层，就必 须及早自我修炼”。修炼的方法，就是多读书、多实践、多思考、多总结，逐步提升自己在管理与维护、技术与 经验、规划与设计、视野与思路等方面的水平。

知乎上有一个提问[“DBA应该具备什么样的特质？招聘DBA时应看谢什么？”](http://www.zhihu.com/question/20112937), [涛吴](http://www.zhihu.com/people/Metaphox)依重要程度依次列举了一些DBA应该具有的性格、知识特点， 可供准备走入DBA行业的人参考，也可供已是DBA的人反思和鞭策。

因上一任DBA离职和工作调整，2012-7月临时从Java开发转Oracle DBA，至今一年有余。期间，主要维护Oracle EBS 11i和R12，包括Apps和DB，以及一些IT系统的数据库，包括Oracle Database 9i, 10g, 11g以及MySQL 5.1， 需要学习大量关于Oracle Database、MySQL、主机、存储和网络等方面的知识，因时间精力有限，只是初窥门径 而已。

这一年多时间，看了一些官方文档，也看了一些个人博客，官方的英文文档依然是首先，中文圈重点推荐下 [Eygle](http://www.eygle.com/)，他是[Oracle ACE](http://www.oracle.com/technetwork/community/oracle-ace/index.html) 总监，[云和恩墨](http://www.enmotech.com/)创始人，现在专注于以数据为中心的企业服务和传道授业解惑； [Dave](http://blog.csdn.net/tianlesoftware)，熟读官方文档，原创和实践很多，是学习Oracle的益友；更 多Oracle牛人，可以参考[中国Oracle用户组](http://www.acoug.org/)。

##Roadmap to Oracle DBA

阅读官方文档和同行博客是熟悉其产品和技术的最有效的不二法门，以下是个人收集整理的一些资料，大部 分都可以在[Oracle Database Documentation Library](http://www.oracle.com/pls/db112/homepage) 和[Oracle Blogs](https://blogs.oracle.com/)中找到。

* roadmap

	* [Maclean：学习Oracle Database的自由之翼](http://www.askmaclean.com/archives/linked-to-oracle-world.html)
	* [Tom: the road map to 10g documentation](http://dylanninin.com/assets/images/2013/tom.jpg)
	* [High Level Vision of DSI](http://dylanninin.com/assets/images/2013/dsi.jpg)

* fundamentals (SQL, PL/SQL, `SQL*Plus`, PL/SQL Developer)

	* Oracle SQL教程
	* Oracle SQL & PL/SQL 教程
	* `SQL*Plus` Quick Reference
	* PL/SQL Language Reference
	* PL/SQL Developer 8.0 User’s Guide 

* administration

	* 2 Day DBA
	* 2 Day + Security Guide
	* Concepts
	* Administrator's Guide
	* Net Services Administrator's Guide
	* Error Messages

* tuning & diagnostics

	* 2 Day + Performance Tuning Guide
	* Performance Tuning Guide
	* Cost Based Oracle Fundamentals

* high availability

	* High Availability Best Practices
	* The White Paper: Oracle Database 11g Release 2 High Availability 
	* Data Guard Concepts and Administration
	* Backup and Recovery User's Guide
	* Real Application Clusters Administration and Deployment Guide
   
* development

	* 2 Day + Java Developer's Guide
	* Java Developer's Guide
	* JDBC Developer's Guide
   
* book

	* [陈吉平：构建Oracle高可用环境--企业级高可用数据库架构、实战与经验总结](http://www.douban.com/subject/2531036/)
	* [Oracle DBA手记1：数据库诊断案例与性能优化实践](http://www.douban.com/subject/4209919/)
	* [Oracle DBA手记2：数据库诊断案例与内部恢复实践](http://book.douban.com/subject/5362865/)
	* [Oracle DBA手记3：数据库性能优化与内部原理解析](http://book.douban.com/subject/6849408/)
	* [Fenng维护的豆列：Oracle优秀图书](http://www.douban.com/doulist/10940/)

* blog

	* [Oracle DB/EM Support](https://blogs.oracle.com/db/)
	* [Oracle Optimizer](https://blogs.oracle.com/optimizer/)
	* [Dave](http://blog.csdn.net/tianlesoftware)
	* [Eygle](http://www.eygle.com/)

* reference
    
	* [Tahiti Documentation](http://tahiti.oracle.com/)
	* [Oracle Metalink](https://support.oracle.com)
