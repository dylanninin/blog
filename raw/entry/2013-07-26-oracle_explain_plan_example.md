---
layout: post
title: Oracle Explain Plan Example
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

unlock hr

	SQL> alter user hr account unlock;
	 
	User altered
	 
	SQL> alter user hr identified by hr;
	 
	User altered

## example 1

	SQL> explain plan for
	  2  select e.employee_id, j.job_title,e.salary,d.department_name
	  3  from employees e, jobs j, departments d
	  4  where e.employee_id < 103
	  5  and e.job_id  = j.job_id
	  6  and e.department_id = d.department_id
	  7  /
	 
	Explained
	 
display plan
	 
	SQL> select * from table(dbms_xplan.display);
	 
	PLAN_TABLE_OUTPUT
	--------------------------------------------------------------------------------
	Plan hash value: 2963623819
	--------------------------------------------------------------------------------
	| Id  | Operation                       | Name          | Rows  | Bytes | Cost (
	--------------------------------------------------------------------------------
	|   0 | SELECT STATEMENT                |               |     3 |   189 |     8
	|   1 |  NESTED LOOPS                   |               |       |       |
	|   2 |   NESTED LOOPS                  |               |     3 |   189 |     8
	|   3 |    MERGE JOIN                   |               |     3 |   141 |     5
	|   4 |     TABLE ACCESS BY INDEX ROWID | JOBS          |    19 |   513 |     2
	|   5 |      INDEX FULL SCAN            | JOB_ID_PK     |    19 |       |     1
	|*  6 |     SORT JOIN                   |               |     3 |    60 |     3
	|   7 |      TABLE ACCESS BY INDEX ROWID| EMPLOYEES     |     3 |    60 |     2
	|*  8 |       INDEX RANGE SCAN          | EMP_EMP_ID_PK |     3 |       |     1
	|*  9 |    INDEX UNIQUE SCAN            | DEPT_ID_PK    |     1 |       |     0
	|  10 |   TABLE ACCESS BY INDEX ROWID   | DEPARTMENTS   |     1 |    16 |     1
	--------------------------------------------------------------------------------
	Predicate Information (identified by operation id):
	---------------------------------------------------
	 
	PLAN_TABLE_OUTPUT
	--------------------------------------------------------------------------------
	   6 - access("E"."JOB_ID"="J"."JOB_ID")
		   filter("E"."JOB_ID"="J"."JOB_ID")
	   8 - access("E"."EMPLOYEE_ID"<103)
	   9 - access("E"."DEPARTMENT_ID"="D"."DEPARTMENT_ID")
	 
	25 rows selected


## example 2
	
sql
						   
	 SQL> explain plan
	  2  set statement_id = 'exp_1' for
	  3  select phone_number
	  4  from employees
	  5  where phone_number like '650%'
	  6  /
	 
	Explained
	 
display plan
	 
	SQL> select plan_table_output
	  2  from table(dbms_xplan.display(null,'exp_1','All'))
	  3  /
	 
	PLAN_TABLE_OUTPUT
	--------------------------------------------------------------------------------
	Plan hash value: 1445457117
	-------------------------------------------------------------------------------
	| Id  | Operation         | Name      | Rows  | Bytes | Cost (%CPU)| Time     |
	-------------------------------------------------------------------------------
	|   0 | SELECT STATEMENT  |           |     1 |    15 |     3   (0)| 00:00:01 |
	|*  1 |  TABLE ACCESS FULL| EMPLOYEES |     1 |    15 |     3   (0)| 00:00:01 |
	-------------------------------------------------------------------------------
	Query Block Name / Object Alias (identified by operation id):
	-------------------------------------------------------------
	   1 - SEL$1 / EMPLOYEES@SEL$1
	Predicate Information (identified by operation id):
	---------------------------------------------------
	   1 - filter("PHONE_NUMBER" LIKE '650%')
	Column Projection Information (identified by operation id):
	 
	PLAN_TABLE_OUTPUT
	--------------------------------------------------------------------------------
	-----------------------------------------------------------
	   1 - "PHONE_NUMBER"[VARCHAR2,20]
	 
	23 rows selected
	 
	SQL> 

## Reference

* Oracle Database Performance Guide