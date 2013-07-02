#Comparison of Backup Tools

<table class="table table-striped">
	<tr>
		<td>Characteristics</td><td>mylvmbackup</td><td>mysqldump</td><td>mk-parallel-dump</td><td>mysqlhotcopy</td><td>ibbackup</td>
	</tr>
	<tr>
		<td>Blocks processing</td><td>Optional</td><td>Yes</td><td>Yes</td><td>Yes</td><td>No</td>
	</tr>
	<tr>
		<td>Logical or Raw</td><td>Raw</td><td>Logical</td><td>Logical</td><td>Raw</td><td>Raw</td>
	</tr>
	<tr>
		<td>Engines</td><td>All</td><td>All</td><td>All</td><td>MyISAM/Archive</td><td>InnoDB</td>
	</tr>
	<tr>
		<td>Speed</td><td>Very Good</td><td>Slow</td><td>Good</td><td>Very Good</td><td>Very Good</td>
	</tr>
	<tr>
		<td>Remote Backups</td><td>No</td><td>Yes</td><td>Yes</td><td>No</td><td>No</td>
	</tr>
	<tr>
		<td>Availability</td><td>Free</td><td>Free</td><td>Free</td><td>Free</td><td>Commercial</td>
	</tr>
	<tr>
		<td>License</td><td>GPL</td><td>GPL</td><td>GPL</td><td>GPL</td><td>Proprietary</td>
	</tr>
</table>

#Supplement

##Delimited file backups

To create a text file containing a table's data, you can use [`SELECT * INTO OUTFILE 'file_name' FROM tbl_name`](http://dev.mysql.com/doc/refman/5.1/en/select-into.html). The file is created on the MySQL server host, not the client host. For this statement, the output file cannot already exist because permitting files to be overwritten constitutes a security risk. See [`SELECT Syntax`](http://dev.mysql.com/doc/refman/5.1/en/select.html). This method works for any kind of data file, but saves only table data, not the table structure.

Another way to create text data files (along with files containing [`CREATE TABLE`](http://dev.mysql.com/doc/refman/5.1/en/create-table.html) statements for the backed up tables) is to use `mysqldump` with the [`--tab`](http://dev.mysql.com/doc/refman/5.1/en/mysqldump.html#option_mysqldump_tab) option. See [Section 1.4.3, “Dumping Data in Delimited-Text Format with mysqldump”](https://dev.mysql.com/doc/mysql-backup-excerpt/5.1/en/mysqldump-delimited-text.html).

To reload a delimited-text data file, use [`LOAD DATA INFILE`](http://dev.mysql.com/doc/refman/5.1/en/load-data.html) or `mysqlimport`.

backup

	mysql> select * into outfile '/db/backup/table1.txt'
		 > fields terminated by ',' optionally enclosed by '"'
		 > lines terminated by '\n'
		 > from test.table1;

recovery

	mysql> load data infile '/db/backup/table1.txt'
		 > into table test.table1
		 > fields terminated by ',' optionally enclosed by '"'
		 > lines terminated by '\n';

#Reference

* [High Performance MySQL Backup and Recovery](http://book.douban.com/subject/1495763/)
* [MySQL Backup and Recovery](https://dev.mysql.com/doc/mysql-backup-excerpt/5.1/en/index.html)
* [mysqldump command reference](https://dev.mysql.com/doc/refman/5.1/en/mysqldump.html)
* [mysqlhotcopy command reference](https://dev.mysql.com/doc/refman/5.0/en/mysqlhotcopy.html)
* [mylvmbackup](http://www.lenzg.net/mylvmbackup/)
* [mk-parallel-dump](http://www.maatkit.org/doc/mk-parallel-dump.html)
* [ibbackup command reference](https://dev.mysql.com/doc/mysql-enterprise-backup/3.5/en/options.html)