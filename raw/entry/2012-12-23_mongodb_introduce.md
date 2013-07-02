#Introduction
MongoDB wasn't designed in a lab. We built MongoDB from our own experiences building large scale, high availability, robust systems. We didn't start from scratch, we really tried to figure out what was broken, and tackle that. So the way I think about MongoDB is that if you take MySql, and change the data model from relational to document based, you get a lot of great features: embedded docs for speed, manageability, agile development with schema-less databases, easier horizontal scalability because joins aren't as important. There are lots of things that work great in relational databases: indexes, dynamic queries and updates to name a few, and we haven't changed much there. For example, the way you design your indexes in MongoDB should be exactly the way you do it in MySql or Oracle, you just have the option of indexing an embedded field.

-- Eliot Horowitz, 10gen CTO and Co-founder

#Why MongoDB?

* Document-oriented
 	* Documents (objects) map nicely to programming language data types
 	* Embedded documents and arrays reduce need for joins
 	* Dynamically-typed (schemaless) for easy schema evolution
 	* No joins and no multi-document transactions for high performance and easy scalability

* High performance
 	* No joins and embedding makes reads and writes fast
 	* Indexes including indexing of keys from embedded documents and arrays
 	* Optional streaming writes (no acknowledgements)
* High availability
 	* Replicated servers with automatic master failover
* Easy scalability
 	* Automatic sharding (auto-partitioning of data across servers)
 	* Reads and writes are distributed over shards
 	* No joins or multi-document transactions make distributed queries easy and fast
 	* Eventually-consistent reads can be distributed over replicated servers
* Rich query language

#Large MongoDB deployment

1. One or more shards, each shard holds a portion of the total data (managed automatically). Reads and writes are automatically routed to the appropriate shard(s). Each shard is backed by a replica set - which just holds the data for that shard.

	A replica set is one or more servers, each holding copies of the same data. At any given time one is primary and the rest are secondaries. If the primary goes down one of the secondaries takes over automatically as primary. All writes and consistent reads go to the primary, and all eventually consistent reads are distributed amongst all the secondaries.

2. Multiple config servers, each one holds a copy of the meta data indicating which data lives on which shard.

3. One or more routers, each one acts as a server for one or more clients. Clients issue queries/updates to a router and the router routes them to the appropriate shard while consulting the config servers.

4. One or more clients, each one is (part of) the user's application and issues commands to a router via the mongo client library (driver) for its language.

	mongod is the server program (data or config). mongos is the router program.

	![mongodb](http://www.mongodb.org/download/attachments/2097393/sharding.PNG)

#Small deployment (no partitioning)
1. One replica set (automatic failover), or one server with zero or more slaves (no automatic failover).

2. One or more clients issuing commands to the replica set as a whole or the single master (the driver will manage which server in the replica set to send to).

#Mongo data model

* A Mongo system (see deployment above) holds a set of databases
* A database holds a set of collections
* A collection holds a set of documents
* A document is a set of fields
* A field is a key-value pair
* A key is a name (string)
* A value is a
	* basic type like string, integer, float, timestamp, binary, etc.,
	* a document, or
	* an array of values

#Mongo query language

To retrieve certain documents from a db collection, you supply a query document containing the fields the desired documents should match. For example, `{name: {first: 'John', last: 'Doe'}}` will match all documents in the collection with name of John Doe. Likewise,` {name.last: 'Doe'}` will match all documents with last name of Doe. Also, `{name.last: /^D/}` will match all documents with last name starting with 'D' (regular expression match).

Queries will also match inside embedded arrays. For example, `{keywords: 'storage'}` will match all documents with 'storage' in its keywords array. Likewise, `{keywords: {$in: ['storage', 'DBMS']}}` will match all documents with 'storage' or 'DBMS' in its keywords array.

If you have lots of documents in a collection and you want to make a query fast then build an index for that query. For example, `ensureIndex({name.last: 1})` or `ensureIndex({keywords: 1})`. Note, indexes occupy space and slow down updates a bit, so use them only when the tradeoff is worth it.

#See also:
* [source](http://www.mongodb.org/display/DOCS/Introduction)
* [Philosophy](http://www.mongodb.org/display/DOCS/Philosophy)

#Reference
* [Mongodb Reference](http://docs.mongodb.org/manual/reference/)
* [SQL to MongoDB Mapping Chart](http://docs.mongodb.org/manual/reference/sql-comparison/)
* [10gen](http://www.10gen.com/)
* [courses of 10gen](https://education.10gen.com/courses)
* [PyMongo](http://api.mongodb.org/python/current/)