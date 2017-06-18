---
layout: post
title: Java Resource
category: Miscellanies
tags: [Java, Resource]
---

大学期间主要学的编程语言是Java，做课程设计、毕业项目都是基于Java的；其他语言或多或少接触过（如C、C++、C#、VB），也写过一些小程序或小项目，但学得不深。

毕业后工作的一年时间内，除去培训，剩下大半年的时间都是在使用Java开发Web应用，使用的还是大学学到的一些技术和框架，不过引入了Flex、Ext JS等前端框架。

之后因工作调整，从小白开始逐步转向Oracle DBA，学习大量的主机、存储、网络、数据库等方面的知识，偶尔也打打杂，不直接参与项目，到现在已经又是一年的光阴了。

在做DBA这一年中，利用业余时间学习了Python，可以动手快速、简洁的实现一些自动化脚本、偶然想法、项目原型或者真正投入使用，很喜欢[The Zen of Python](http://www.python.org/dev/peps/pep-0020/)，也很喜欢“人 生苦短，我用Python”的格言。

最近几个月还学习了Ruby，十分喜欢Ruby、Ruby On Rails中随处可见的DSL，也开始折腾Github和Jekyll。

今天有同学问起Java学习的一些推荐资料，乘此机会正好整理一份，方便以后参考，以下是自己看过和值得推荐的一些资料清单。

## 基础
	
主要熟悉Java语言历史、特点、基础语法以及常用标准库，推荐官方的参考Java SE5.0/6.0 [Java Specifications](http://docs.oracle.com/javase/specs/)， 另外，台湾人[良葛格](http://openhome.cc/Gossip/)从事Java教育经验丰富，他的Java Essence和Java上下教程写得浅显易懂，很适合Java初学者，看起来不费力，入门快。

[《Thinking in Java 4th》](http://pervasive2.morselli.unimo.it/~nicola/courses/IngegneriaDelSoftware/java/ThinkingInJava.pdf)很经典，可以作参考书，从Java的基础语法到高级特性（面向对象概念、容器、多线程等）都有涉及，但讲述详实，比较厚，不适合快速入门。

网上有针对Python程序员的Java教程，对比了概念、语法，可供Python程序员快速浏览和熟悉之用，详见[Welcome to Java for Python Programmers](http://interactivepython.org/runestone/static/java4python/index.html)。

编码规范：参考[Java Code Conversion](http://www.oracle.com/technetwork/java/codeconv-138413.html)。
    
## 进阶

在了解Java语言基础之后，接下来可以熟悉下Java的网络和数据库编程，一般的Java项目都离不开这两项。

网络编程：参考[《Java Network Programming》](http://www.mdp.ac.id/materi/2012-2013-1/TI425/111061/TI425-111061-908-1.pdf)。

数据库：参考[《Java Database Programming with JDBC》](http://eduunix.ccut.edu.cn/index2/pdf/O'Reilly%20-%20Java%20Database%20Programming%20with%20JDBC.pdf)，[MongoDB Getting Started with Java Drive](http://docs.mongodb.org/ecosystem/tutorial/getting-started-with-java-driver/)。

## 高级

技术点：参考《Java核心技术》[卷1](http://www.china-pub.com/208978)，[卷2](http://www.china-pub.com/508881)，[Volume 1](http://www.amazon.com/Core-Java-I-Fundamentals-8th-Sun/dp/0132354764/ref=sr_11_1?ie=UTF8&qid=1215592737&sr=11-1)，[Volume 2](http://www.amazon.com/Core-Java-Vol-Advanced-Features/dp/0132354799/ref=sr_1_1?ie=UTF8&s=books&qid=1227751671&sr=1-1)，介绍了Java技术的方方面面，阐述精确到位，叙述深入浅出，并包含大量示例，可作参考书。

并发编程：参考[《Java Concurrency in Practice》](http://cs.famaf.unc.edu.ar/~nicolasw/Docencia/PCeJ/jcip.pdf)，熟悉Java的并发模型和机制，有助于设计和编写并发性能良好的程序。

经验规则：参考[《Effective Java》](http://uet.vnu.edu.vn/~chauttm/e-books/java/Effective.Java.2nd.Edition.May.2008.3000th.Release.pdf),熟悉常见问题的解决方案，有助于编写高效、健壮、清晰的代码。

Java解惑：参考[《Java Puzzles》](http://www.javapuzzlers.com/)，熟悉Java或其类库的陷阱和缺陷而导致的bug，可以帮助了解实现细节。

设计模式：参考[《Head First Design Patterns》](http://isa.unomaha.edu/wp-content/uploads/2012/08/Design-Patterns.pdf)、[JDK里的设计模式](http://coolshell.cn/articles/3320.html)，Java编程更偏向设计和架构，因此必须熟悉常用的设计模式，并灵活运用于实际项目中。

JVM：参考[《The JVM Specification》](http://docs.oracle.com/javase/specs/jvms/se5.0/html/VMSpecTOC.doc.html)，Java虚拟机的规范和细节，对深入编译器和字节码有兴趣的可以参考。

## Web开发

主要介绍Java在Web开发方面的基础技术和框架。

#### 1.前端

HTML/CSS/JS：这些是基础，BS架构的应用离不开

#### 2.基础

JSP/Servlet：参考良葛格的[Servlet/JSP Gossip](http://openhome.cc/Gossip/ServletJSP/)，Java服务端编程基础，必须掌握。

XML：参考 [Java XML Tutorial](http://www.mkyong.com/tutorials/java-xml-tutorials/)，[《XML开发技术教程》](http://book.douban.com/subject/3246748/)，配套的[PPT](https://drive.google.com/folderview?id=0B_BiAoqYvwURRVJsSWRHcEx1MzA&usp=sharing&tid=0B_BiAoqYvwURUnVISmVDX3hZTGc)，编辑配置文件、自动化脚本、WebService等都离不开XML，必须掌握。

Web Container：参考[《How Tomcat Works》](http://files.cnblogs.com/wasp520/tomcat/HowTomcatWorks.pdf)，熟悉Java Web容器的原理以及实现细节，源代码很适合阅读。
        
#### 3.一些框架

大学时做过一些Web项目基本都是SSH框架，对中小型企业已经够用，其他的暂未接触。

前端框架: [Struts2+](http://struts.apache.org/development/2.x/)，参考[2010-3-10_Struts2_讲义_IBM](https://drive.google.com/folderview?id=0B_BiAoqYvwURTDBrR0kyZ0hKcDQ&usp=sharing&tid=0B_BiAoqYvwURUnVISmVDX3hZTGc)。
    
数据库ORM框架：[Hibernate3+](http://www.hibernate.org/)，参考[2012-9-12_Hibernate.ppt](https://docs.google.com/file/d/0B_BiAoqYvwURcFZ3LWRzdXlDQm8/edit?usp=drive_web)。

全能框架：[Spring2.5+](http://spring.io/)，参考[2012-9-12_Spring.ppt](https://docs.google.com/file/d/0B_BiAoqYvwURcWxzdGRtTE9FRkE/edit?usp=drive_web&pli=1)。

## 工具

IDE: [Vim](http://www.vim.org/)，[Eclipse](http://www.eclipse.org/)，[MyEclipse](http://www.myeclipseide.com/)，Java开发并不难，主要在于设计，写代码方面更多的是在使用IDE（如自动补全、生成代码等），推荐使用MyEclipse，参考[MyEclipse10优化](http://www.cnblogs.com/batys/archive/2012/02/23/2364832.html)。

反编译：[JAD](http://varaneckas.com/jad/)，[jadeclipse(Eclipse插件)](http://sourceforge.net/projects/jadclipse/)，反编译.class文件，查看源代码。

自动化工具：[Ant](http://ant.apache.org/)，[Maven](http://maven.apache.org/)，用于项目的自动化编译、测试、打包、部署等。

## 其他

UML：设计核心、参考手册, [UML相关工具一览](http://www.umlchina.com/tools/newindex1.htm)。从不同维度和层次对项目进行建模（分析和设计），有助于熟悉项目的整体架构。

我用得比较多的是[StarUML](staruml.sourceforge.net/‎)，现在也有很多Web版的UML工具，推荐[LucidChart](https://www.lucidchart.com/)，Google Docs现在也支持LucidChart。

## 参考
	
* [Welcome to Java for Python Programmers](http://interactivepython.org/runestone/static/java4python/index.html)
* [Java Specifications](http://docs.oracle.com/javase/specs/)
* 良葛格 [Java Essence](http://openhome.cc/Gossip/JavaEssence/)
* 良葛格 [Java 上](http://openhome.cc/Gossip/JavaGossip-V1/)
* 良葛格 [Java 下](http://openhome.cc/Gossip/JavaGossip-V2/)
* 良葛格 [Servlet/JSP Gossip](http://openhome.cc/Gossip/ServletJSP/)
* [Java Code Conversion](http://www.oracle.com/technetwork/java/codeconv-138413.html)
* [《Thinking in Java 4th》](http://pervasive2.morselli.unimo.it/~nicola/courses/IngegneriaDelSoftware/java/ThinkingInJava.pdf)
* [《Java Network Programming》](http://www.mdp.ac.id/materi/2012-2013-1/TI425/111061/TI425-111061-908-1.pdf)
* [《Java Database Programming with JDBC》](http://eduunix.ccut.edu.cn/index2/pdf/O'Reilly%20-%20Java%20Database%20Programming%20with%20JDBC.pdf)
* [MongoDB Getting Started with Java Drive](http://docs.mongodb.org/ecosystem/tutorial/getting-started-with-java-driver/)
* 《Java核心技术》[卷1](http://www.china-pub.com/208978)，[卷2](http://www.china-pub.com/508881)，[Volume 1](http://www.amazon.com/Core-Java-I-Fundamentals-8th-Sun/dp/0132354764/ref=sr_11_1?ie=UTF8&qid=1215592737&sr=11-1),[Volume 2](http://www.amazon.com/Core-Java-Vol-Advanced-Features/dp/0132354799/ref=sr_1_1?ie=UTF8&s=books&qid=1227751671&sr=1-1)
* [《Java Concurrency in Practice》](http://cs.famaf.unc.edu.ar/~nicolasw/Docencia/PCeJ/jcip.pdf)
* [《The JVM Specification》](http://docs.oracle.com/javase/specs/jvms/se5.0/html/VMSpecTOC.doc.html)
* [Java XML Tutorial](http://www.mkyong.com/tutorials/java-xml-tutorials/)
* [《XML开发技术教程》](http://book.douban.com/subject/3246748/)
* [《How Tomcat Works》](http://files.cnblogs.com/wasp520/tomcat/HowTomcatWorks.pdf)
* [《Head First Design Patterns》](http://isa.unomaha.edu/wp-content/uploads/2012/08/Design-Patterns.pdf)
* [JDK里的设计模式](http://coolshell.cn/articles/3320.html)
* [Lisp的永恒之道](http://coolshell.cn/articles/7526.html)
* [Java SE5 API](http://docs.oracle.com/javase/1.5.0/docs/api/), [Java SE6 API](http://docs.oracle.com/javase/6/docs/api/)
* [Apache Tomcat 6](http://tomcat.apache.org/tomcat-6.0-doc/index.html)
* [UML](http://www.uml.org/)
* [陈皓 Java数据Top10](http://coolshell.cn/articles/14.html)
* [MyEclipse10优化](http://www.cnblogs.com/batys/archive/2012/02/23/2364832.html)
* [Google Drive](https://drive.google.com/folderview?id=0B_BiAoqYvwURUnVISmVDX3hZTGc&usp=sharing)