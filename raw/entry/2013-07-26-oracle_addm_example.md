---
layout: post
title: Oracle ADDM Example
category : Oracle
tags : [Oracle, Database, DBA, Performance]
---

## pl/sql packages

	[oracle@oradb ~]$ ls -l /db/oracle/product/11.2.0/db_1/rdbms/admin/addm*
	-rw-r--r--. 1 oracle oinstall 4748 Jan  6  2005 /db/oracle/product/11.2.0/db_1/rdbms/admin/addmrpti.sql
	-rw-r--r--. 1 oracle oinstall 3168 Oct 16  2003 /db/oracle/product/11.2.0/db_1/rdbms/admin/addmrpt.sql
	-rw-r--r--. 1 oracle oinstall 6196 Mar  6  2007 /db/oracle/product/11.2.0/db_1/rdbms/admin/addmtmig.sql

## dbms_advisor

### statistics_level
     
    SQL> show parameter statistics_level;
     
    NAME                                 TYPE        VALUE
    ------------------------------------ ----------- ------------------------------
    statistics_level                     string      TYPICAL
     
### tables
     
    SQL> create table bigtab as select rownum as "id", a.* from dba_objects a;
     
    Table created
     
    SQL> create table smalltab as select  rownum as "id", a.* from dba_tables a;
     
    Table created
     
    SQL> declare
      2  n number;
      3  begin
      4     for n in 1 .. 100
      5     loop
      6       insert into bigtab select rownum as "id", a.* from dba_objects a;
      7       commit;
      8     end loop;
      9  end;
     10  /
     
    PL/SQL procedure successfully completed

### create first snapshot
    
    SQL> exec dbms_workload_repository.create_snapshot('TYPICAL');
     
    PL/SQL procedure successfully completed
     
### high-load operation   
  
    SQL> declare
      2  v_var number;
      3  begin
      4     for n in 1 .. 6
      5     loop
      6       select count(*) into v_var from bigtab a, smalltab b;
      7     end loop;
      8  end;
      9  /
     
    PL/SQL procedure successfully completed

    SQL> /

    PL/SQL procedure successfully completed

### create second snapshot
    
    SQL> exec dbms_workload_repository.create_snapshot('TYPICAL');
     
    PL/SQL procedure successfully completed

### create advisor task
    
get last two snap_id
    
    SQL> select * from(select * from dba_hist_snapshot order by snap_id desc)where rownum <= 2;
     
       SNAP_ID       DBID INSTANCE_NUMBER STARTUP_TIME                                                                     BEGIN_INTERVAL_TIME                                                              END_INTERVAL_TIME                                                                FLUSH_ELAPSED                                                                   SNAP_LEVEL ERROR_COUNT  SNAP_FLAG
    ---------- ---------- --------------- -------------------------------------------------------------------------------- -------------------------------------------------------------------------------- -------------------------------------------------------------------------------- ------------------------------------------------------------------------------- ---------- ----------- ----------
          4220 1193549399               1 08-JUL-13 05.34.27.000 PM                                                        26-JUL-13 01.00.41.115 PM                                                        26-JUL-13 01.40.28.363 PM                                                        +00000 00:00:00.6                                                                        1           0          1
          4219 1193549399               1 08-JUL-13 05.34.27.000 PM                                                        26-JUL-13 11.47.51.301 AM                                                        26-JUL-13 01.00.41.115 PM                                                        +00000 00:00:00.9                                                                        1           0          0
  
get dbid
  
    SQL> select dbid from v$database;
     
          DBID
    ----------
    1193549399

### create advisor task and execute
    
    SQL> declare
      2     task_name varchar2(30) := 'ADDM_01';
      3     task_desc varchar2(30) := 'ADDM Feature Test';
      4     task_id number;
      5  begin
      6     dbms_advisor.create_task('ADDM', task_id, task_name, task_desc, null);
      7     dbms_advisor.set_task_parameter(task_name, 'START_SNAPSHOT', 4219);
      8     dbms_advisor.set_task_parameter(task_name, 'END_SNAPSHOT', 4220);
      9     dbms_advisor.set_task_parameter(task_name, 'DB_ID', 1193549399);
     10     dbms_advisor.execute_task(task_name);
     11  end;
     12  /
     
    PL/SQL procedure successfully completed
    
### display task report
    
    SQL> set long 1000000 pagesize 0 longchunksize 1000
    SQL> column get_clob for a80
    SQL> select dbms_advisor.get_task_report('ADDM_01', 'TEXT', 'All') from dual;
     
    DBMS_ADVISOR.GET_TASK_REPORT('
    --------------------------------------------------------------------------------
              ADDM Report for Task 'ADDM_01'
              ------------------------------
     
    Analysis Period
    ---------------
    AWR snapshot range from 4219 to 4220.
    Time period starts at 26-JUL-13 01.00.41 PM
    Time period ends at 26-JUL-13 01.40.28 PM
     
    Analysis Target
    ---------------
    Database 'DBTEST' with DB ID 1193549399.
    Database version 11.2.0.1.0.
    Analysis was requested for all instances, but ADDM analyzed instance DBTEST,
    numbered 1 and hosted at oradb.egolife.com.
    See the "Additional Information" section for more information on the requested
    instances.
     
    Activity During the Analysis Period
    -----------------------------------
    Total database time was 2303 seconds.
    The average number of active sessions was .96.
    ADDM analyzed 1 of the requested 1 instances.
     
    Summary of Findings
    -------------------
       Description            Active Sessions      Recommendations
                              Percent of Activity
       ---------------------  -------------------  ---------------
    1  Top SQL Statements     .96 | 100            1
    2  "User I/O" wait Class  .02 | 2.35           0
     
     
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     
     
              Findings and Recommendations
              ----------------------------
     
    Finding 1: Top SQL Statements
    Impact is .96 active sessions, 100% of total activity.
    ------------------------------------------------------
    SQL statements consuming significant database time were found. These
    statements offer a good opportunity for performance improvement.
     
       Recommendation 1: SQL Tuning
       Estimated benefit is .96 active sessions, 100% of total activity.
       -----------------------------------------------------------------
       Action
          Run SQL Tuning Advisor on the SELECT statement with SQL_ID
          "4mfwm7psk02pc".
          Related Object
             SQL statement with SQL_ID 4mfwm7psk02pc.
             SELECT COUNT(*) FROM BIGTAB A, SMALLTAB B
       Rationale
          The SQL spent 100% of its database time on CPU, I/O and Cluster waits.
          This part of database time may be improved by the SQL Tuning Advisor.
       Rationale
          Database time for this SQL was divided as follows: 100% for SQL
          execution, 0% for parsing, 0% for PL/SQL execution and 0% for Java
          execution.
       Rationale
          SQL statement with SQL_ID "4mfwm7psk02pc" was executed 2 times and had
          an average elapsed time of 1150 seconds.
       Rationale
          Top level calls to execute the PL/SQL statement with SQL_ID
          "b8zqgfq0kz0hv" are responsible for 100% of the database time spent on
          the SELECT statement with SQL_ID "4mfwm7psk02pc".
          Related Object
             SQL statement with SQL_ID b8zqgfq0kz0hv.
             declare
             v_var number;
             begin
             for n in 1 .. 6
             loop
             select count(*) into v_var from bigtab a, smalltab b;
             end loop;
             end;
     
     
    Finding 2: "User I/O" wait Class
    Impact is .02 active sessions, 2.35% of total activity.
    -------------------------------------------------------
    Wait class "User I/O" was consuming significant database time.
    The throughput of the I/O subsystem was not significantly lower than expected.
    The Oracle instance memory (SGA and PGA) was adequately sized.
     
       No recommendations are available.
     
     
     
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     
              Additional Information
              ----------------------
     
    Miscellaneous Information
    -------------------------
    Wait class "Application" was not consuming significant database time.
    Wait class "Commit" was not consuming significant database time.
    Wait class "Concurrency" was not consuming significant database time.
    Wait class "Configuration" was not consuming significant database time.
    CPU was not a bottleneck for the instance.
    Wait class "Network" was not consuming significant database time.
    Session connect and disconnect calls were not consuming significant database
    time.
    Hard parsing of SQL statements was not consuming significant database time.
     
    The database's maintenance windows were active during 100% of the analysis
    period.

## Alternative

script path

    [oracle@oradb ~]$ pwd
    /home/oracle
    [oracle@oradb ~]$ ls -l /db/oracle/product/11.2.0/db_1/rdbms/admin/addm*
    -rw-r--r--. 1 oracle oinstall 4748 Jan  6  2005 /db/oracle/product/11.2.0/db_1/rdbms/admin/addmrpti.sql
    -rw-r--r--. 1 oracle oinstall 3168 Oct 16  2003 /db/oracle/product/11.2.0/db_1/rdbms/admin/addmrpt.sql
    -rw-r--r--. 1 oracle oinstall 6196 Mar  6  2007 /db/oracle/product/11.2.0/db_1/rdbms/admin/addmtmig.sql
    
execute addmrpt
    
    [oracle@oradb ~]$ sqlplus  dev/dev

    `SQL*Plus`: Release 11.2.0.1.0 Production on Fri Jul 26 14:07:16 2013

    Copyright (c) 1982, 2009, Oracle.  All rights reserved.


    Connected to:
    Oracle Database 11g Enterprise Edition Release 11.2.0.1.0 - 64bit Production
    With the Partitioning, OLAP, Data Mining and Real Application Testing options

    SQL> @?/rdbms/admin/addmrpt

    Current Instance
    ~~~~~~~~~~~~~~~~

       DB Id    DB Name	 Inst Num Instance
    ----------- ------------ -------- ------------
     1193549399 DBTEST		1 DBTEST


    Instances in this Workload Repository schema
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

       DB Id     Inst Num DB Name	   Instance	 Host
    ------------ -------- ------------ --------- ------------------
      1193549399	    1 DBTEST	   DBTEST	 oradbbak.egolife.com
    * 1193549399	    1 DBTEST	   DBTEST	 oradb.egolife.com

    Using 1193549399 for database Id
    Using	       1 for instance number


    Specify the number of days of snapshots to choose from
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Entering the number of days (n) will result in the most recent
    (n) days of snapshots being listed.  Pressing <return> without
    specifying a number lists all completed snapshots.



    Listing the last 3 days of Completed Snapshots

                                Snap
    Instance     DB Name	    Snap Id    Snap Started    Level
    ------------ ------------ --------- ------------------ -----
    DBTEST	     DBTEST	       4158 24 Jul 2013 00:00	   1
                       4159 24 Jul 2013 01:00	   1
                       4160 24 Jul 2013 02:00	   1
                       4161 24 Jul 2013 03:00	   1
                       4162 24 Jul 2013 04:00	   1
                       4163 24 Jul 2013 05:00	   1
                       4164 24 Jul 2013 06:00	   1
                       4165 24 Jul 2013 07:00	   1
                       4166 24 Jul 2013 08:00	   1
                       4167 24 Jul 2013 09:00	   1
                       4168 24 Jul 2013 10:00	   1
                       4169 24 Jul 2013 11:00	   1
                       4170 24 Jul 2013 12:00	   1
                       4171 24 Jul 2013 13:00	   1
                       4172 24 Jul 2013 14:00	   1
                       4173 24 Jul 2013 15:00	   1
                       4174 24 Jul 2013 16:00	   1
                       4175 24 Jul 2013 17:00	   1
                       4176 24 Jul 2013 18:00	   1
                       4177 24 Jul 2013 19:00	   1
                       4178 24 Jul 2013 20:00	   1
                       4179 24 Jul 2013 21:00	   1
                       4180 24 Jul 2013 22:00	   1
                       4181 24 Jul 2013 23:00	   1
                       4182 25 Jul 2013 00:00	   1
                       4183 25 Jul 2013 01:00	   1
                       4184 25 Jul 2013 02:00	   1
                       4185 25 Jul 2013 03:00	   1
                       4186 25 Jul 2013 04:00	   1
                       4187 25 Jul 2013 05:00	   1
                       4188 25 Jul 2013 06:00	   1
                       4189 25 Jul 2013 07:00	   1
                       4190 25 Jul 2013 08:00	   1
                       4191 25 Jul 2013 09:00	   1
                       4192 25 Jul 2013 10:00	   1
                       4193 25 Jul 2013 11:00	   1
                       4194 25 Jul 2013 12:00	   1
                       4195 25 Jul 2013 13:00	   1
                       4196 25 Jul 2013 14:00	   1
                       4197 25 Jul 2013 15:00	   1
                       4198 25 Jul 2013 16:00	   1
                       4199 25 Jul 2013 17:00	   1
                       4200 25 Jul 2013 18:00	   1
                       4201 25 Jul 2013 19:00	   1
                       4202 25 Jul 2013 20:00	   1
                       4203 25 Jul 2013 21:00	   1
                       4204 25 Jul 2013 22:00	   1
                       4205 25 Jul 2013 23:00	   1
                       4206 26 Jul 2013 00:00	   1
                       4207 26 Jul 2013 01:00	   1
                       4208 26 Jul 2013 02:00	   1
                       4209 26 Jul 2013 03:00	   1
                       4210 26 Jul 2013 04:00	   1
                       4211 26 Jul 2013 05:00	   1
                       4212 26 Jul 2013 06:00	   1
                       4213 26 Jul 2013 07:00	   1

                                Snap
    Instance     DB Name	    Snap Id    Snap Started    Level
    ------------ ------------ --------- ------------------ -----
    DBTEST	     DBTEST	       4214 26 Jul 2013 08:00	   1
                       4215 26 Jul 2013 09:00	   1
                       4216 26 Jul 2013 10:00	   1
                       4217 26 Jul 2013 11:00	   1
                       4218 26 Jul 2013 11:47	   1
                       4219 26 Jul 2013 13:00	   1
                       4220 26 Jul 2013 13:40	   1



    Specify the Begin and End Snapshot Ids
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Enter value for begin_snap: 4217
    Begin Snapshot Id specified: 4217

    Enter value for end_snap: 4220
    End   Snapshot Id specified: 4220



    Specify the Report Name
    ~~~~~~~~~~~~~~~~~~~~~~~
    The default report file name is addmrpt_1_4217_4220.txt.  To use this name,
    press <return> to continue, otherwise enter an alternative.

    Enter value for report_name: 

    Using the report name addmrpt_1_4217_4220.txt


    Running the ADDM analysis on the specified pair of snapshots ...


    Generating the ADDM report for this analysis ...


          ADDM Report for Task 'TASK_4690'
          --------------------------------

    Analysis Period
    ---------------
    AWR snapshot range from 4217 to 4220.
    Time period starts at 26-JUL-13 11.00.36 AM
    Time period ends at 26-JUL-13 01.40.28 PM

    Analysis Target
    ---------------
    Database 'DBTEST' with DB ID 1193549399.
    Database version 11.2.0.1.0.
    ADDM performed an analysis of instance DBTEST, numbered 1 and hosted at
    oradb.egolife.com.

    Activity During the Analysis Period
    -----------------------------------
    Total database time was 6692 seconds.
    The average number of active sessions was .7.

    Summary of Findings
    -------------------
       Description		  Active Sessions      Recommendations
                  Percent of Activity
       ---------------------  -------------------  ---------------
    1  Top SQL Statements	  .51 | 72.49	       1
    2  "User I/O" wait Class  .02 | 2.41	       0


    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


          Findings and Recommendations
          ----------------------------

    Finding 1: Top SQL Statements
    Impact is .51 active sessions, 72.49% of total activity.
    --------------------------------------------------------
    SQL statements consuming significant database time were found. These
    statements offer a good opportunity for performance improvement.

       Recommendation 1: SQL Tuning
       Estimated benefit is .51 active sessions, 72.49% of total activity.
       -------------------------------------------------------------------
       Action
          Run SQL Tuning Advisor on the SELECT statement with SQL_ID
          "4mfwm7psk02pc".
          Related Object
         SQL statement with SQL_ID 4mfwm7psk02pc.
         SELECT COUNT(*) FROM BIGTAB A, SMALLTAB B
       Rationale
          The SQL spent 100% of its database time on CPU, I/O and Cluster waits.
          This part of database time may be improved by the SQL Tuning Advisor.
       Rationale
          Database time for this SQL was divided as follows: 100% for SQL
          execution, 0% for parsing, 0% for PL/SQL execution and 0% for Java
          execution.
       Rationale
          SQL statement with SQL_ID "4mfwm7psk02pc" was executed 4 times and had
          an average elapsed time of 1652 seconds.
       Rationale
          Top level calls to execute the PL/SQL statement with SQL_ID
          "b8zqgfq0kz0hv" are responsible for 100% of the database time spent on
          the SELECT statement with SQL_ID "4mfwm7psk02pc".
          Related Object
         SQL statement with SQL_ID b8zqgfq0kz0hv.
         declare
         v_var number;
         begin
         for n in 1 .. 6
         loop
         select count(*) into v_var from bigtab a, smalltab b;
         end loop;
         end;


    Finding 2: "User I/O" wait Class
    Impact is .02 active sessions, 2.41% of total activity.
    -------------------------------------------------------
    Wait class "User I/O" was consuming significant database time.
    The throughput of the I/O subsystem was not significantly lower than expected.
    The Oracle instance memory (SGA and PGA) was adequately sized.

       No recommendations are available.



    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

          Additional Information
          ----------------------

    Miscellaneous Information
    -------------------------
    Wait class "Application" was not consuming significant database time.
    Wait class "Commit" was not consuming significant database time.
    Wait class "Concurrency" was not consuming significant database time.
    Wait class "Configuration" was not consuming significant database time.
    CPU was not a bottleneck for the instance.
    Wait class "Network" was not consuming significant database time.
    Session connect and disconnect calls were not consuming significant database
    time.
    Hard parsing of SQL statements was not consuming significant database time.

    The database's maintenance windows were active during 100% of the analysis
    period.


    End of Report
    Report written to addmrpt_1_4217_4220.txt
	
## Reference

* Oracle Database Performance Tuning Guide