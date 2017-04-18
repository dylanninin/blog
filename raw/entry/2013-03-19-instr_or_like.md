---
layout: post
title: INSTR or Like
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

在51CTO上看到一篇文章：[在Oracle数据库中使用instr代替like实操](http://database.51cto.com/art/201005/197734.htm)，看到之后很质疑，以下是我做的简单测试，以对原文作对比验证。

## 1.创建索引前

	 SQL> select count(1) from t;
	 
	  COUNT(1)
	----------
	  11905920
	 
	Elapsed: 00:00:11.38

	SQL> select count(1) from t where instr(object_name,'A') >0;
	 
	  COUNT(1)
	----------
	   3947520
	 
	Elapsed: 00:00:10.46

	SQL> select count(1) from t where object_name like '%A%';
	 
	  COUNT(1)
	----------
	   3947520
	 
	Elapsed: 00:00:12.31

	SQL> select count(1) from t where instr(object_name,'A') = 0;
	 
	  COUNT(1)
	----------
	   7958400
	 
	Elapsed: 00:00:10.39

	SQL> select count(1) from t where object_name not like '%A%';
	 
	  COUNT(1)
	----------
	   7958400
	Elapsed: 00:00:10.94
 

从以上结果看出，没有创建索引时，instr和like效率差不多，instr效率略高一点，但也不是文中提到的相差巨大。
 
## 2.创建索引后

	SQL> create index t_i on t(object_name);
	 
	Index created.
	 
	Elapsed: 00:02:08.92

	SQL> select count(1) from t;
	 
	  COUNT(1)
	----------
	  11905920
	 
	Elapsed: 00:00:11.07

	SQL> select count(1) from t where instr(object_name,'A') >0;
	 
	  COUNT(1)
	----------
	   3947520
	 
	Elapsed: 00:00:12.04

	SQL> select count(1) from t where object_name like '%A%';
	 
	  COUNT(1)
	----------
	   3947520
	 
	Elapsed: 00:00:07.33

	SQL> select count(1) from t where instr(object_name,'A') = 0;
	 
	  COUNT(1)
	----------
	   7958400
	 
	Elapsed: 00:00:11.57

	SQL> select count(1) from t where object_name not like '%A%';
	 
	  COUNT(1)
	----------
	   7958400
	 
	Elapsed: 00:00:06.47
 

从以上测试看出，添加索引后，like比instr效率高，费时是instr的一半，可以用相差巨大来形容。

## 小结

instr,like都是Oracle已经实现的功能，严格来说instr为内部函数，like为SQL标准，效率都很高，但具体如何实现，暂且不知。但两者之间的性能差别还是要看具体的数据库环境，如表结构，数据分布，索引，数据库版本，数据库当时的负载情况。另外，效率高也是以数据库、服务器的资源消耗为代价的，在时间同数量级或用户允许的情况下，如何控制效能才是关键。

由此，也可以看出数据库性能调优应该是一门艺术，需要不断学习、实践。

## 参考

* [在Oracle数据库中使用instr代替like实操](http://database.51cto.com/art/201005/197734.htm)
* [INSTR Oracle SQL Language Reference](http://docs.oracle.com/cd/B28359_01/server.111/b28286/functions073.htm#i77598)
* [LIKE Oracle SQL Language Reference](http://docs.oracle.com/cd/B28359_01/server.111/b28286/conditions007.htm#sthref2907
