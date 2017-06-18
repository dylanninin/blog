---
layout: post
title: Oracle ROWID
category : Oracle
tags : [Oracle, Database, DBA]
---

## Rowid Data Types

Every row stored in the database has an address. Oracle Database uses a  ROWID  data type to store the address (rowid) of every row in the database. Rowids fall into the following categories:

 * Physical rowids store the addresses of rows in heap-organized tables, table clusters, and table and index partitions.
 * Logical rowids store the addresses of rows in index-organized tables.
 * Foreign rowids are identifiers in foreign tables, such as DB2 tables accessed through a gateway. They are not standard Oracle Database rowids.

A data type called the universal rowid, or  UROWID , supports all kinds of rowids.

## Use of Rowids  

Oracle Database uses rowids internally for the construction of indexes. 

A B-tree index, which is the most common type, contains an ordered list of keys divided into ranges. Each key is associated with a rowid that points to the associated row's address for fast access. End users and application developers can also use rowids for several important functions:

 * Rowids are the fastest means of accessing particular rows.
 * Rowids provide the ability to see how a table is organized.
 * Rowids are unique identifiers for rows in a given table.

You can also create tables with columns defined using the  ROWID  data type. For example, you can define an exception table with a column of data type  ROWID  to store the rowids of rows that violate integrity constraints. Columns defined using the  ROWID data type behave like other table columns: values can be updated, and so on.

## ROWID Pseudocolumn  

Every table in an Oracle database has a pseudocolumn named ROWID . A pseudocolumn behaves like a table column, but is not actually stored in the table. You can select from pseudocolumns, but you cannot insert, update, or delete their values. A pseudocolumn is also similar to a SQL function without arguments. Functions without arguments typically return the same value for every row in the result set, whereas pseudocolumns typically return a different value for each row. Values of the  ROWID  pseudocolumn are strings representing the address of each row. These strings have the data type  ROWID . This pseudocolumn is not evident when listing the structure of a table by executing  SELECT  or  DESCRIBE , nor does the pseudocolumn consume space. However, the rowid of each row can be retrieved with a SQL query using the reserved word  ROWID  as a column name.


## Rowid Format  

Oracle Database uses a rowid to uniquely identify a row. Internally, the rowid is a structure that holds information that the database needs to access a row. A rowid is not physically stored in the database, but is inferred from the file and block on which the data is stored.

An extended rowid includes a data object number. This rowid type uses a base 64 encoding of the physical address for each row. The encoding characters are  A-Z ,  a-z , 0-9 ,  + , and  / . 

After a rowid is assigned to a row piece, the rowid can change in special circumstances. For example, if row movement is enabled, then the rowid can change because of partition key updates, Flashback Table operations, shrink table operations, and so on. If row movement is disabled, then a rowid can change if the row is exported and imported using Oracle Database utilities.


    --rowid
    ROWID	            Object	File	Block	Row
    AAAVYeAAMAAAAMcAAk	AAAVYe	AAM	    AAAAMc	AAk


    --查询RowID信息 10进制
    select dbms_rowid.rowid_object('&rowid')       data_object_id,
           dbms_rowid.rowid_relative_fno('&rowid') data_file_id,
           dbms_rowid.rowid_block_number('&rowid') data_block_id,
           dbms_rowid.rowid_row_number('&rowid')   data_num
      FROM dual;
	--output
    DATA_OBJECT_ID	DATA_FILE_ID	DATA_BLOCK_ID	DATA_NUM
    87582	        12	            796	            36

	
## The Base64 Alphabet
	
                    Table 1: The Base64 Alphabet

     Value Encoding  Value Encoding  Value Encoding  Value Encoding
         0 A            17 R            34 i            51 z
         1 B            18 S            35 j            52 0
         2 C            19 T            36 k            53 1
         3 D            20 U            37 l            54 2
         4 E            21 V            38 m            55 3
         5 F            22 W            39 n            56 4
         6 G            23 X            40 o            57 5
         7 H            24 Y            41 p            58 6
         8 I            25 Z            42 q            59 7
         9 J            26 a            43 r            60 8
        10 K            27 b            44 s            61 9
        11 L            28 c            45 t            62 +
        12 M            29 d            46 u            63 /
        13 N            30 e            47 v
        14 O            31 f            48 w         (pad) =
        15 P            32 g            49 x
        16 Q            33 h            50 y
	
## Reference

* Oracle Database Administrator's Guide
* [The Base16, Base32, and Base64 Data Encodings](http://tools.ietf.org/html/rfc4648)