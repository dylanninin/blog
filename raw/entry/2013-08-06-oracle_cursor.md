---
layout: post
title: Oracle Cursor Introduction
category : Oracle
tags : [Oracle, Database, DBA]
---

## Cursor

Cursors are one of the most common and fundamental terms in the database terminology. 

It is one of the core database programming concepts, which forms a basic unit of execution of SQL statement.

A cursor is a pointer, which points towards a pre allocated memory location in the SGA. For transparent understanding, it is a handle or gateway adopted by Oracle to execute a SQL query. The memory location to which it points is known as Context area. Oracle associates every SELECT statement with a cursor to hold the query information in this context area.

Cursor follows a defined execution cycle to execute the SQL statement associated with it. The article describes the Oracle cursors and their usage.

There are two types of cursors: Implicit cursors and explicit cursors.

### Implicit Cursors

Oracle server processes every SQL statement in a PL/SQL block as an implicit cursor. All the DML statements (INSERT, UPDATE or DELETE) and SELECT query with INTO or BULK COLLECT clauses are candidates for implicit cursors. Whenever a SQL statement is executed, Oracle automatically allocates a memory area (known as context area) in Oracle database PGA i.e. Process Global Area. This allocated memory space is the query work area which holds the query related information.

For implicit cursor, the complete execution cycle is internally handled and maintained by the oracle server. For developers, implicit cursor appears to be an abstract concept. Only thing which is physically available and visible to them is the cursor status flags and information. Cursor attributes reveal the cursor related information and status. Following are the cursor attributes available:

* SQL%ROWCOUNT – Number of rows returned/changed in the last executed query. Applicable for SELECT as well as DML statement
* SQL%ISOPEN – Boolean TRUE if the cursor is still open, else FALSE. For implicit cursor it is FALSE only
* SQL%FOUND – Boolean TRUE, if the cursor fetch points to a record, else FALSE
* SQL%NOTFOUND – Inverse of SQL%FOUND. The flag is set as FALSE when the cursor pointer does not point to a record in the result set.

These attributes are set at the different stages of execution cycle and retained in the context area.

### Explicit Cursors

These cursors are explicitly declared in the DECLARE section of the block. They possess a specific name and a static SELECT statement attached to them. Explicit cursors are manually executed by the developers and follow complete execution cycle.

Explicit cursor information is also captured in cursor attributes, which are set during the cursor processing and reveal essential information about the cursors. These attributes, as listed below, are same as that in implicit cursors but specific to the cursors.

* CURSOR%ROWCOUNT
* CURSOR%ISOPEN
* CURSOR%FOUND
* CURSOR%NOTFOUND

## Reference

* Oracle Database Administrator's Guide