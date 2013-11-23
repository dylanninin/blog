---
layout: post
title: Oracle ERP DBA
category: Miscellanies
tags: [Oracle, DBA, EBS, Resource]
---

Oracle EBS全称Oracle E-Business Suite，是有名的[ERP](http://en.wikipedia.org/wiki/Enterprise_resource_planning) 产品之一，其他的还有SAP ERP，用友ERP等，具体参见[List of ERP software packages](http://en.wikipedia.org/wiki/List_of_ERP_software_packages) 。

从2012-7月至今，做了一年有余的ERP DBA，主要负责管理和维护Oracle E-Business 11i和R12，服务全 公司，用于生产制造、销售管理等。其中11i基于IBM Power5，OS为AIX 5.3；R12基于x86，OS为Oracle Linux 6。

最近半年，在Oracle Advanced Customer Support的Team带领下，完成了11i到R12的升级项目，主要包 括硬件平台的迁移(主机从Power5到x86，存储从DS4700到V7000)，部署架构的调整(应用、数据库分离， 单节点到多节点，数据库实施RAC + ASM)，应用、数据库、客制化程序的升级等。

经过一年的折腾，可以说入门了，积累不多，但体会不少，以下仅针对ERP DBA吐吐槽，不同人体会可能 不一样：

* ERP DBA也是一个SDE，是Someone Do Everything，也是Miscellaneous Transaction；
* Oracle EBS坑太多，软件臃肿，文档泛滥，Reference Cross Reference，而且还是个大内存杀手；
* Oracle 有个藏经阁叫Metalink，皓首穷经始成绝技，但人生苦短时不我待，容易练成小无相功；
* Oracle ACS Team经验丰富，但多是重复性的、支持性的工作，远远望去，不免无聊乏味，也不免骑虎难下；

当然，即使这么多坑坑槽槽，也可以从中学到很多，比如耐下心来看英文Guide和Note，熟悉行业的业务流程， 理解复杂系统的技术架构；其中也有犯过很多错误，走过很多弯路，所谓“犯完这些错误，再牛逼起来”是也。 只是Oracle ERP DBA入行需慎重再慎重。

##ERP DBA

以下引用朱龙春在[《Oracle E-Business Suite: ERP DBA实践指南》]((http://book.douban.com/subject/10795733/)) 中的话，介绍ERP DBA：

ERP 在中国的应用与推广已有近20 年，而Oracle 电子商务套件（E-Business Suite）作 为世界上最有 名的ERP 产品之一，在中国也已经有了十几年的发展历程，并且已经广泛应用于各个行业和领域，在国内市 场上占有很大份额。
	
随着ERP 的发展，市场上对于能担任重要角色的ERP DBA 有着大量的需求。ERP DBA 与一般意义上的DBA和 其他技术人员是有区别的：ERP DBA 需要有更多的综合知识，不仅 要精通ERP 产品和数据库技术，还要掌 握操作系统、网络、存储设备及程序开发等相关知识，甚至对模块功能也需要有一定的了解。可见，ERP DBA人才是需要有较长实践的持续积累的。 	

然而，像Oracle 电子商务套件这样重要的ERP 产品，由于是西方人研发的，相关的文档基本上都是英文的， 至今也没有一本写给ERP DBA 看的中文书籍，这也就进一步抬高了进入ERP 领域的门槛，让很多爱好者无从 下手或望而却步。
	
本书是国内第一本适用于ERP DBA 的中文书籍，全书从介绍如何架构一个大型ERP 系统开始，并配以ERP系 统管理员的基础知识，最后以概述如何优化和维护一个大型ERP 系统结尾。漫漫人生路，笔者总结自己十几 年的ERP 从业经历，越发感悟到：“越是最基础的东西，往往就是最精髓的”，所谓的“高级技术”只不过是基 础知识的衍生而已。当然，技能是ERP DBA 存在的价值，但思路可以决定一个人的未来，所以本书推翻了初 稿中大量的所谓的“高级技术”内容，以“最基础的知识”为引子，力求使读者不仅能掌握基础知识，更能拓宽 思路，从而一步一步走向架构师的职业发展道路。“授人以鱼，不如授人以渔”，这是笔者一贯秉承的理念， 也是始终贯穿于本书的指导思想，希望本书能够降低广大技术爱好者的学习难度，并使更多的技术爱好者走 进ERP 顾问行业，促进中国ERP 事业的进一步发展。

##Roadmap to Oracle ERP DBA

Oracle ERP的相关文档基本上都是英文的，但因为缺少中文文档而望而却步：What a shame it is!

阅读官方文档和同行博客是熟悉其产品和技术的最有效的不二法门，以下是个人收集整理的一些资料，大部 分都可以在[Oracle R12.1 Documentation Library](http://docs.oracle.com/cd/B53825_08/current/html/docset.html) 和[Oracle Blogs](https://blogs.oracle.com/)中找到，其他请自行Google。

* technology	

	* R12 Technology Stack Roadmap
	* R12 Technology Essentials
	* Oracle Application Installation Guide:Using Rapid Install
	* Oracle Applications Concepts
	* Oracle Applications Multiple Organizations Implementation Guide

* administration	

	* Oracle Applications System Administrator's Guide - Configuration
	* Oracle Applications System Administrator's Guide - Maintenance
	* Oracle Applications System Administrator's Guide - Security
	* Oracle Web Applications Desktop Intergrator Implementation and Administrator's Guide

* tuning & diagnostics

	* Tuning All Layers of EBS
	* Oracle EBS Diagnostics User's Guide

* guide

	* Oracle Applications User's Guide
	* Oracle Applications Developer's Guide
	* Oracle Application Framework Personalization Guide
	* Oracle Applications Flexfields Guide
	* Oracle Workflow Administrator's Guide
	* Oracle Workflow User's Guide
	* Oracle Application User Interface Standards for Forms-Based Products

* book
    
	* [Oracle E-Business Suite: ERP DBA实践指南](http://book.douban.com/subject/10795733/)

* blog

	* [Oracle E-Business Suite Technology](https://blogs.oracle.com/stevenChan/)
	* [Oracle E-Business Suite Support Blog](https://blogs.oracle.com/ebs/)
	* [Apps DBA & Architect Knowledge Warehouse](https://blogs.oracle.com/longchun/)
	* [Paul Tian on CSDN](http://blog.csdn.net/pan_tian)
	* [OracleSeeker](http://oracleseeker.com/)

* reference

	* [Oracle R12.1 Documentation Library](http://docs.oracle.com/cd/B53825_08/current/html/docset.html)
	* [Oracle Metalink](https://support.oracle.com)
	* [Oracle eTRM Technical Reference](http://etrm.oracle.com/pls/etrm/etrm_search.search)