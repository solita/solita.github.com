---
layout: post
title: Elasticsearch as read only database
author: villephamalainen
excerpt: >
  Elasticsearch is a powerful, open-source search and analytics engine. It was initially released in 2010 and has since been adopted widely. Solita has a long history of using Elasticsearch and has found good use cases for it. One of them is using Elasticsearch as a read only database on top of traditional SQL database. This architecture has the benefit of modeling full domain relations to the SQL database and getting the lightning-fast searches from Elasticsearch where needed.
tags:
  - Software Architecture
  - Software development
  - Elasticsearch
  - SQL Server
  - Microsoft
  - DOTNET
  - C#
---

**Elasticsearch is a powerful, open-source search and analytics engine. It was initially released in 2010 and has since been adopted widely <sup>[1]</sup>. Solita has a long history of using Elasticsearch and has found good use cases for it. One of them is using Elasticsearch as a read only database on top of traditional SQL database. This architecture has the benefit of modeling full domain relations to the SQL database and getting the lightning-fast searches from Elasticsearch where needed.**

I was personally introduced to Elasticsearch three years ago when I started working at Solita. My first and only project in Solita so far heavily relies on Elasticsearch. When I started in the project, I did not understand why it was used and what the tradeoffs were. Since then, I have learned a lot about Elasticsearch. In this post I would like to explain some of the tradeoffs and put some actual numbers on them as well. But first, I would like to briefly explain the technologies I'm talking about.

## What is Elasticsearch

Elasticsearch is a distributed search and analytics engine built on top of Apache Lucene. It is designed for speed and scalability, making it ideal for handling large volumes of data in near real-time. Elasticsearch is part of the Elastic Stack, which includes tools like Kibana for visualization, Logstash for data processing, and Beats for data shipping.

Key Features of Elasticsearch:
-	Full-Text Search: Optimized for fast and relevant full-text searches.
-	Scalability: Horizontally scalable with support for data sharding and replication.
-	Real-Time Analytics: Capable of performing complex queries and aggregations in near real-time.
-	Versatility: Supports a wide range of use cases, including log and event data analysis, application monitoring, and security analytics

Elasticsearch is open sourced under the AGPL license.

In this post I will be talking about Elasticsearch only and the other components of Elastic Stack are out of scope. <sup>[2], [3]</sup>

## What is SQL Server

SQL Server is a relational database management system (RDBMS) developed by Microsoft. It uses Transact-SQL (T-SQL) to manage and query data. SQL Server is known for its robustness, security, and comprehensive support for transaction processing, business intelligence, and analytics.

Key Features of SQL Server:
-	Relational Database: Structured storage with support for complex queries and transactions.
-	Security: Advanced security features like Transparent Data Encryption and Always Encrypted.
-	Integration Services: Tools for data integration, transformation, and analysis.
-	High Availability: Features like Always On Availability Groups for high availability and disaster recovery

In this post I will be focusing only in a small part on SQL Server usage. There is more to it than what this post brings up. <sup>[4]</sup>

## Comparing differences in Elasticsearch and SQL Server

**Data Model**<br>
Elasticsearch: Uses a schema-free JSON document model, which allows for flexible and dynamic data structures.<br>
SQL Server: Uses a structured, tabular data model with predefined schemas, making it ideal for relational data.

**Scalability**<br>
Elasticsearch: Designed for horizontal scalability, allowing it to handle large datasets by distributing data across multiple nodes.<br>
SQL Server: Supports both vertical and horizontal scaling, but horizontal scaling can be more complex to implement.

**Performance**<br>
Elasticsearch: Excels in full-text search and real-time analytics, making it suitable for applications requiring quick search capabilities.<br>
SQL Server: Optimized for transaction processing and complex queries on structured data, providing robust performance for OLTP workloads.

**Use Cases**<br>
Elasticsearch: Best suited for log and event data analysis, real-time application monitoring, and security analytics.<br>
SQL Server: Ideal for transaction processing, business intelligence, data warehousing, and enterprise applications. <sup>[5], [6]</sup>

## Architecture

Now that we have covered the basics let’s get back to my use case.
In many applications it is typical to use just one SQL database for everything. This is a very simple setup, and it works well in many cases, especially with small applications. When the application userbase gets a little bigger or the application uses search heavily this setup might start to slow down. In these cases, it might be a good time to start thinking about different approaches.

The approach we have used is using Elasticsearch as a read only database. This means that data is always first written to the SQL database and after that synchronized to Elasticsearch. You can then choose where to use Elasticsearch and where SQL database for reading. Elasticsearch is typically used for complex queries or ones that are used the most often. When Elasticsearch is used on top of SQL database it provides performance improvements and the ability to have different abstractions to the underlying data. You can for example optimize the data structure for the use case in Elasticsearch.

[![Figure 1: Simplified version of the architecture](/img/2025-elasticsearch-as-read-only-database/read-only-architecture.png)](/img/2025-elasticsearch-as-read-only-database/read-only-architecture.png)<br>
*Figure 1: Simplified version of the architecture*

On the other hand, this setup is not without its downsides. Having two databases is much more complex than just using one. Synchronizing data between the two requires development effort and is a potential source of bugs. It is done with custom code as there is no out-of-the-box solution for it. In addition, synchronization takes a little bit of time, so the data is not instantly available in Elasticsearch after writing to SQL database. Additionally, the development is much harder when you need to learn how to use two different databases.

In my project we are using Elasticsearch quite extensively. It has been a great learning experience for me and I’m very impressed by how performant it is. Fetching data from Elasticsearch is very fast. But I have also noticed that it does slow down development quite a bit. This is why I have been wondering multiple times whether it is worth using it in this project. Or even on some specific feature I have been designing. I have seen some of the results in the project, but I also wanted to get some actual comparison numbers. So, I made a test setup for comparing Elasticsearch against SQL Server. This setup should simulate the situation if we would use Elasticsearch or just SQL Server for a feature.

## Test setup

I created a new ASP .NET Core 8 project with connections to local SQL Server and Elasticsearch (using docker). The code can be found [here](https://github.com/solita/sqlserver-vs-elasticsearch). The project contains a very simple test entity with just 3 properties which are written and read from the database. All the read tests were done with 100k entities in the database. Write tests were done to empty database.
The tests were done with bombardier <sup>[7]</sup>. Read tests were made with 5 simultaneous connections and 100 requests. Write tests were made with 1 simultaneous connection and 5 requests. All tests were made with a powerful modern laptop.

Tests included:
-	Read one entity
-	Search with string
-	Read 10k entities
-	Write 10k entities

## Test results

The results are divided into three different figures. In Figure 1 an average latency is seen for each test with standard deviation. In Figure 2 an average request per second is seen for each test with standard deviation. In Figure 3 CPU percentage usage is seen for one write test. Memory usage is not shown because it was static and very similar for both databases.

[![Figure 2: Latency comparison (milliseconds). Lower is better.](/img/2025-elasticsearch-as-read-only-database/elasticsearch-vs-sqlserver-latency.png)](/img/2025-elasticsearch-as-read-only-database/elasticsearch-vs-sqlserver-latency.png)<br>
*Figure 2: Latency comparison (milliseconds). Lower is better.*

As seen from Figure 2 the most difference was seen in search test. Elasticsearch performed close to 40 times faster than SQL Server. Reading difference was closer but still almost twice as fast with Elasticsearch. Writing was quite close, more on that later.

[![Figure 3: Requests per second comparison. Higher is better.](/img/2025-elasticsearch-as-read-only-database/elasticsearch-vs-sqlserver-requests.png)](/img/2025-elasticsearch-as-read-only-database/elasticsearch-vs-sqlserver-requests.png)<br>
*Figure 3: Requests per second comparison. Higher is better.*

Requests per second follow the same pattern as latency and Elasticsearch performed better in each of the tests.

[![Figure 4: Write CPU comparison.](/img/2025-elasticsearch-as-read-only-database/elasticsearch-vs-sqlserver-cpu.png)](/img/2025-elasticsearch-as-read-only-database/elasticsearch-vs-sqlserver-cpu.png)<br>
*Figure 4: Write CPU comparison.*

As seen from the CPU comparison Elasticsearch uses multiple cores when writing and SQL server does not. Writing speed might be more even with a single core instance.

## Conclusion

As can be seen from the results, Elasticsearch performed better in all of the tests. I am not surprised by this but the amount of the difference in search speed did surprise me a bit. Applying the architecture we have really has its benefits. You should also realize that when the architecture performs better it might translate into lower costs of hardware or cloud components. I think I can also see this in my project since the required cloud resources for each component are very small.

Applying architecture with Elasticsearch as read only database does wonders for performance in some areas. But it does have its drawbacks as well. The databases need to be kept in synchronization with each other. There is also the cost of development time and complexity of this type of architecture.

Last, I would like to offer some use cases where we have found Elasticsearch to be worth it. Obviously if you need to search from large amounts of data, Elasticsearch is really good. One use case we stumbled into is real time dashboards. It might be quite taxing for SQL database to offer this, and caching is a bit problematic if the data changes frequently. But Elasticsearch seems to be a very good solution for that.

## References

[[1]] https://db-engines.com/en/ranking/search+engine

[[2]] https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html

[[3]] https://www.elastic.co/enterprise-search

[[4]] https://learn.microsoft.com/en-us/sql/sql-server/what-is-sql-server?view=sql-server-ver16

[[5]] https://airbyte.com/data-engineering-resources/elasticsearch-vs-sql-server

[[6]] https://www.influxdata.com/comparison/elasticsearch-vs-sqlserver/

[[7]] https://github.com/codesenberg/bombardier

[1]: https://db-engines.com/en/ranking/search+engine
[2]: https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro-what-is-es.html
[3]: https://www.elastic.co/enterprise-search
[4]: https://learn.microsoft.com/en-us/sql/sql-server/what-is-sql-server?view=sql-server-ver16
[5]: https://airbyte.com/data-engineering-resources/elasticsearch-vs-sql-server
[6]: https://www.influxdata.com/comparison/elasticsearch-vs-sqlserver/
[7]: https://github.com/codesenberg/bombardier
