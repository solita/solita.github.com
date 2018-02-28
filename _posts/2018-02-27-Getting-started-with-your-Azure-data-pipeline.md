---
layout: post
title: Setting up your first data pipline in Azure
author: kaarelkorvemaa
excerpt: Getting started with your Azure data pipeline
tags:
- Azure
- Data factor
- SQL Data Warehouse
- Polybase
- Azure Data Lake
- Data pipeline
- External table
---

### Polybase and Azure Data Factor
Majority of data project limbo around text files. Companies have 10s of different software that they use.  Integrating all of the can be sometimes impossible and not so business oriented. That’s why exporting text files from different systems is always easier, than building a datahub. Self-service solutions make it very easy to import text files and visualise them. This can at one point mean that an individual in an organisation has X amount of excels and csv files that take a lot of space and became a problem.  What was the file and is it up to date ?

### Azure
Storaging, analysing and loading them into Azure is a good option. Azure has several different storage related services available, choosing the right one should always be done case by case. Most convenient one is [Azure Data Lake(ADL)](https://azure.microsoft.com/en-us/solutions/data-lake/). ADL is the dream storage place for developer, data scientists and analysts, that need scalable data storage, with easy access to big data. It has all the capabiltities an enterpise needs, security, manageability, scalability, reliability and availability to serve demanding storage requierments. Data projects start with gathering these text files into ADL and then copying them into [Azure data warehouse(ADW)](https://azure.microsoft.com/en-us/services/sql-data-warehouse/?v=17.44)/[SQL server](https://azure.microsoft.com/en-us/services/sql-database/) for reporting. Finding suitable way for doing that can be challenging and time consuming.

Azure provides options like [ Azure Data Factor(ADF)](https://azure.microsoft.com/en-gb/services/data-factory/) and [PolyBase](https://docs.microsoft.com/en-us/sql/relational-databases/polybase/polybase-guide). Azure Data factor(ADF) is a data processing tool, for managing data pipelines. It is a fully managed ETL service in cloud. ADF can orchestrate data flows from on-premise and cloud sources, which makes it a very flexible and easy to use tool for moving data to and from ADL. It is not just for copying data into databases, you can schedule, manage, analyse, processes and monitor your data pipeline with it. As of most of the systems change, schemas and data models do that as well. ADF works well when nothing isn’t changed in the table side.

On average text files that are > 1 GB that need to be load into ADW/SQL server, would be suggestively done with Polybase. PolyBase is a technology that connects external/internal data with database via t-sql language.

Polybase and ADF loading time are different, for a 5 GB text file it varies from 20 -30 minutes. ADF has a “warming up time”, which means that the system needs some time to be fully available. With PolyBase you can make an insert and it will take around 3-5 minutes for the text file to be in ADW.

### Practicalities ADF & PolyBase

Both ADF and Polybase are very sensitive with the data. Key thing to make sure before you start querying data:

- Identical schemas and data types
- Most errors are symbols inside text rows
- Header is not specified
- Source file in ADL/Blob has to have permission (Read, Write, Execute)
- Reject_value for column names

For making PolyBase data pipeline you need the following: Database scope credentials, External data source, External file Format and External Table. For querying data, I suggest to insert data from external table into regular table.

### How it works in practice?

Before you can create Scope credentials you need your client_id and Token_EndPoint, which can be found from azure portal, under Azure Active Directory. After scope credentials have been created, use the same credentials name in the external data source credential phase. Location of the data source, is the place where you have the file.

Creating a file format, define the format based on the text file you are trying to insert. Here is where you can define what type of a text file you have.


```
CREATE DATABASE SCOPED CREDENTIAL <name>
WITH
IDENTITY = '<client_id>@<OAuth_2.0_Token_EndPoint>',
SECRET = '<key>'
;



CREATE EXTERNAL DATA SOURCE <datalake>
WITH (
TYPE = HADOOP,
LOCATION = 'adl://<AzureDataLake account_name>.azuredatalakestore.net,
CREDENTIAL = <name>
);


CREATE EXTERNAL FILE FORMAT TextFile
WITH (
FORMAT_TYPE = DelimitedText,
FORMAT_OPTIONS (FIELD_TERMINATOR = '|'
,STRING_DELIMITER = '' ),


);

```

After that create external table add the location in the Data Lake.

```
CREATE EXTERNAL TABLE [TABLE.NAME]
(
COLUMN INT,
COLUMN2 VARCHAR(10)
)
WITH (DATA_SOURCE = [Data Lakename ], LOCATION = N'/foldername/', FILE_FORMAT = [TextFiletype], REJECT_TYPE = VALUE, REJECT_VALUE = 1)
```

Credentials are connected to the folder inside the Data Lake, so you can't create the external table before the folder has credentials. According to Microsoft this is the best practice to insert data into ADW.



## Summary:
In case where schemas won’t change or have little changes external tables are a good way of managing regular data flows. Automating loads between ADL and ADW, Microsoft  suggest SSIS usage. There is also an open source option [Airflow](https://airflow.apache.org/), which is a platform to programmatically author, schedule and monitor workflows.


[CREATE EXTERNAL TABLE (Transact-SQL)](https://docs.microsoft.com/en-us/sql/t-sql/statements/create-external-table-transact-sql)
[Access control in Azure Data Lake Store](https://docs.microsoft.com/en-us/azure/data-lake-store/data-lake-store-access-control)


