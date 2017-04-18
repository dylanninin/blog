---
layout: post
title: Python with Oracle Database
category : Python
tags : [Python, Libs, Database]
---

最近刚开始学习Python，学习了下基本语法，确实很灵活，不得不让只会写Java代码的人眼前一亮。

因工作中与Oracle数据打交道比较多，所以最先想到的就是如何用Python操作Oracle数据库，比如基本的数据库连接，增删改查操作，存储过程、函数调用，事务处理等，方便以后做一些测试、管理工作的迁移。在Java开发中，访问Oracle数据库可以采用JDBC，Oracle官方提供实现JDBC规范的ojdbc驱动；在Python开发中，找到了实现Python DB API V2.0规范的cx_Oracle模块，还有基于Tuxedo事务规范的tux_oracle。tux_oracle即基于tuxmodule和cx_Oracle。

## cx_Oracle学习计划

cx_Oracle 是Python版的Oracle Database操作扩展模块

1) 实现Python database API 2.0 规范

   curosr.nextset()、time data type尚未实现(Oracle Database不支持)

2) 增加一些Oracle Database扩展

3) 使用前提：安装Oracle客户端(服务端)，或者Instant Client

*  windows: Oracle Instant Client  +  cx_Oracle 5.1.2
* unix: cx_Oracle.pyd/cx_Oracle.so

4) 实现原理：OCI --> C --> Python

5) 开发者：doc -> sample -> test -> source code -> apps dev

6) 事务处理：tux_oracle

7) 总结：意见，建议

## 参考

* [Python: Python DB API 2](http://www.python.org/dev/peps/pep-0249/)
* [Sourceforge: cx_Oracle](http://sourceforge.net/projects/cx-oracle/)
* [Sourceforge: tux_oracle](http://sourceforge.net/projects/cx-oracle/)