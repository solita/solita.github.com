---
layout: post
author: pkalliok
title: >
  Dynamic SQL in applications: how to handle dynamic WHERE clauses
excerpt: >
  The only way to make efficient SQL database queries is to include
  their SQL code in your application.  There is a very common need for
  dynamic SQL that textual SQL templates do not cover very well, or at
  all.  That is the case where we want to have a varying number of WHERE
  conditions in a database query.
tags:
- programming
- Clojure
- SQL
- security
- simplicity
- orthogonality
- Python
---

## What is so difficult about using SQL in applications?

If you're like me, you might have thought that there is something smelly
if not outright wrong in the way applications interact with SQL
databases.  The ubiquitous practice of sending practically executable
code &ndash; SQL statements &ndash; to the server means that we will
have to construct executable code programmatically in our application.
And that means that we have to be very careful to prevent security
problems in that generated code.  The reason we have SQL injections in
the first place is that there's no other way to interact with SQL
databases than to construct code on the fly.

> ```sql
> SELECT phone, email
> FROM people
> WHERE name LIKE '%$namepart%'
> ```
> Whoopsie, what happens if $namepart contains a quote character?

Of course, every modern database interface provides some facilities to
interpolate values from our application language to the generated SQL in
a safe way.  This handles the vast majority of cases where you need to
take care that your dynamically generated SQL doesn't end up being
something completely different you meant it to be.  The SQL is generated
from some kind of (textual) SQL templates, and the templating library
&ndash; often integrated with the programming language's database
interface library &ndash; takes care that the generated SQL is always
structurally sound.

> ```sql
> SELECT users.username, people.email
> FROM people, users
> WHERE users.person = people.id
>   AND people.name LIKE :namepattern
>   AND users.last_login > :lastdate
> ```
> This is what it usually looks like, with modern database interfaces.

## The problem of dynamic WHERE clauses

But, there is a very common need for dynamic SQL that textual SQL
templates do *not* cover very well, or at all.  That is the case where
we want to have a varying number of WHERE conditions in a database query
depending on whether or not the listing is constrained in some specific
way.  For instance, the user might want to list all cities in some specific
area; then, having seen there are too many to browse through, they want
to restrict the search to only big cities with more than half a million
people.  The two queries are essentially the same, except that the
latter adds a new AND condition to the WHERE clause of our generated
SQL.

> ```python
> query = """SELECT * FROM cities
> 	WHERE (lng - :x) * (lng - :x) + (lat - :y) * (lat - :y) < 100"""
> params = { "x": x, "y": y }
> if minpopulation:
>   query += " AND population > :minpop"
>   params["minpop"] = minpopulation
> ```
> One (bad) way to dynamically construct WHERE clauses (in Python).

There are a couple of solutions to this situation without inducing code
duplication between the two queries.  One of them (and sadly common) is
to construct SQL *templates* by hand, adding more AND conditions when
needed, and also updating the list of template parameters.  This is
error prone and wastes working time every time one needs to update the
query construction logic.

Because code generation is error prone, some have solved this problem by
making a more powerful templating language.
[HoneySQL](https://github.com/jkk/honeysql), for instance, is a Clojure
library that converts templates, expressed by native data structures,
into executable SQL.  This is a working solution, but sometimes it feels
stupid to learn yet another database language &ndash; the data structure
language used to express SQL.  It might be more portable across
databases, but it also requires you to extend the template language if
you want to use some database specific features.

> ```clojure
> (-> (select :*)
>     (from :cities)
>     (merge-where (if-not (nil? namepattern)
>       [:like :name namepattern]))
>     (merge-where (if-not (nil? minpopulation)
>       [:> :population minpopulation]))
>     sql/format)
> ```
> Dynamic SQL construction in Clojure and HoneySQL.

Yet another approach to dynamic SQL generation is the ORM, or
object-relational mapper.  ORM is a technique which adorns native data
structures with the ability to be database-backed.  All changes to those
objects' state will be synced into the database, and vice versa.  ORMs
are superb for data updates, but outright horrible for complex queries.
They shift data query logic from the database side to the application
side, which makes it harder to use the database for what it excels in,
and in practice results in all kinds of performance problems.  However,
when and how to use ORMs is a very complicated question well worthy its
own blog post or several.

## Solving the dynamic WHERE clause problem in SQL

However, there is a simpler solution &ndash; so simple that it is easy
to overlook.  Usually, we can trust the SQL server to behave sensibly
when we shift the condition logic to the SQL side.  Every database I
know optimises away conditions whose truth value can be proved (such as
``3 < 5`` or, more usefully, ``NULL IS NULL``).  In practice, this means
that unwanted search parameters can be passed in a NULLs, and their
value can be checked in the SQL so that they never affect the search
when they are NULL.

> ```sql
> SELECT * FROM cities
> WHERE (lng - :x) * (lng - :x) + (lat - :y) * (lat - :y) < 100
>   AND :minpop IS NULL OR population > :minpop
> ```
> Handling the dynamic part on the SQL side.

As a sidenote, I recently found out about
[Yesql](https://github.com/krisajenkins/yesql), which very well appeals
to my &aelig;sthetic taste.  Because SQL is a domain-specific language,
I don't want to embed it in strings in another language; rather I would
like to keep it in a separate file, so that I can tell my text editor to
use SQL syntax highlighting for editing that file, and I won't need to
bother with the indentation of my host language (currently Clojure) when
I write longish SQL excerpts.  Yesql embeds query metadata in SQL
comments.  This is an actual example of a PostgreSQL query in my Yesql
query file.

```sql
-- name: db-points-near
-- Return points in order of proximity to :point, along with their tag(s).
SELECT loc.id, loc.coord, tag.name, tag.ns
FROM (SELECT id, coord, modtime, mergedto
	FROM location
	WHERE mergedto IS NULL
	ORDER BY coord <-> (:point)::point
	LIMIT (:limit)::integer
	OFFSET (:page)::integer * :limit) AS loc, location_tag l, tag
WHERE loc.id = l.location
  AND l.tag = tag.id
  AND ((:mindate)::date IS NULL OR loc.modtime > :mindate)
  AND ((:maxdate)::date IS NULL OR loc.modtime < :maxdate)
  AND ((:maxdist)::float IS NULL OR (loc.coord <-> :point) < :maxdist)
  AND ((:tagpat)::text IS NULL OR tag.name LIKE :tagpat)
  AND ((:username)::text IS NULL OR tag.ns = :username)
ORDER BY loc.coord <-> :point;
```

Neat, right?  Although I find it somewhat worrying that I have to
type-annotate parameters in almost all contexts, having the full query
logic in SQL is very pleasing and makes my application code more
straightforward.  After having the query defined thus, I only need to
construct the parameter map to pass to the query.

Further reading:
- [Common Cases when (not) to Use Dynamic
  SQL](http://www.sommarskog.se/dynamic_sql.html#Common_cases): The need
  for dynamic SQL generation arises from various reasons, some good and
  some bad.  This article, even if written for Microsoft SQL Server, has
  a lot of ideas and analysis that applies quite well to other SQL
  backends.
- [The two top performance problems caused by ORM
  tools](http://use-the-index-luke.com/blog/2013-04/the-two-top-performance-problems-caused-by-ORM-tools):
  Usually, you do not want to optimise before you can verify that
  performance problems exist (by profiling or similar techniques).
  However, ORM performance problems are especially difficult to tackle
  and sometimes require restructuring of your application.  Here are
  also two articles about ORM optimisation for
  [nHibernate](http://geekswithblogs.net/Optikal/archive/2013/03/10/152371.aspx)
  (Java) and
  [SQLAlchemy](https://pythonguy.wordpress.com/2011/08/17/sqlalchemy-tips-performance/)
  (Python).

