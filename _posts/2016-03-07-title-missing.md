---
layout: post
title: Title missing
author: juhofriman
excerpt: Some domains do not allow any attributes to be missing or unknown, but most domains contain at least some attributes which can be unknown, missing or undefined. Be sure to pay extra attention on attributes that can be missing. Using NULL in relational databases divide approaches within programmer community. In my experience some of us absolutely detest using NULLs and some of us cope with NULLs. I belong to the latter group.
categories:
- SQL
tags:
- SQL
- domain modeling
- NULL
---

When we create business critical programs we must be able to represent values that are missing or unknown. In relational algebra no such ugly concept as "missing value" exist, but in real world scenarios we don't have all the data we need all the time. Instead in most situations data keeps popping from here and there. We ultimately need to be able to build UI's for customers which are essentially highly usable and represent missing values clearly. For example when building a customer registry is it a problem if user does not have an address? Should UI represent it accordingly then? This all comes down to persistence model and thus it's important to build model that represents missing values accurately.

During my career I have witnessed bright minded software developers being in my opinion way too strict about NULL values in databases. They do just about everything to define schema which does not allow NULLs anywhere. I'm not here to mock great minds, such as C.J. Date who has taken really strong stance against NULLs in relational databases. This has been ongoing debate in relational database community since the first implementations. I personally feel, that when it comes to professional software development, we as a developers should have reasonable amount of practical stance, but in the same time should be aware of the underlying theory.

Some domains do not allow any attributes to be missing or unknown, but most domains contain at least some attributes which can be unknown, missing or undefined. Be sure to pay extra attention on attributes that can be missing. Using NULL in relational databases divide approaches within programmer community. In my experience some of us absolutely detest using NULLs and some of us cope with NULLs. I belong to the latter group.

*Examples are tested with Postgresql 9.5.0*

## Semantics of NULL

This writing concerns only NULL values in relational databases but as a background information, we briefly introduce three well known semantics of NULL.

### 1) NULL is Falsy

In many programming languages NULL is *falsy*. You can evaluate it and it "is false".

```javascript
if(null) {
    // not executed
} else {
    // executed!
}
```

LISPs follow this semantics and most dynamically typed languages such as Ruby and Python.

### 2) Evaluation of NULL is illegal

NULL can also be considered something that can not be evaluated. For example Java takes this approach and throws a *NullPointerException* when evaluating something like mentioned. Note that you can't evaluate truth value if pointer is not type *Boolean*. Primitive type *boolean* can't be null.

```java
Boolean value = null;
if(value) {
    // Not executed, instead a NullPointerException is thrown
    // when clause is evaluated
}
```

Also note that you can evaluate if pointer is pointing to NULL, but you can't make a boolean out of NULL which is the case in *NULL is falsy* semantics.

```java
Object a = null;
if(a == null) {
    // Executed
}
```

### 3) Three-value logic

Relational databases take yet another approach on how to handle NULL values. They introduce something that it known as a [three-value logic](https://en.wikipedia.org/wiki/Three-valued_logic "Wikipedia: Three-valued logic") (trinary logic, ternary logic), which can be thought as an extension to well familiar boolean logic. Three-value logic takes to account the fact that value can indeed be missing and clauses must still be evaluable. The problem is that it yields NULL as a result in some cases.

<table>
    <tr>
        <td><strong>p</strong></td>
        <td><strong>q</strong></td>
        <td><strong>p AND q</strong></td>
        <td><strong>p OR q</strong></td>
        <td><strong>NOT p</strong></td>
    </tr>

    <tr>
        <td>true</td>
        <td>true</td>
        <td>true</td>
        <td>true</td>
        <td>false</td>
    </tr>
    <tr>
        <td>true</td>
        <td>NULL</td>
        <td>NULL</td>
        <td>true</td>
        <td>false</td>
    </tr>
    <tr>
        <td>true</td>
        <td>false</td>
        <td>false</td>
        <td>true</td>
        <td>false</td>
    </tr>

    <tr>
        <td>NULL</td>
        <td>true</td>
        <td>NULL</td>
        <td>true</td>
        <td>NULL</td>
    </tr>
    <tr>
        <td>NULL</td>
        <td>NULL</td>
        <td>NULL</td>
        <td>NULL</td>
        <td>NULL</td>
    </tr>
    <tr>
        <td>NULL</td>
        <td>false</td>
        <td>false</td>
        <td>NULL</td>
        <td>NULL</td>
    </tr>

    <tr>
        <td>false</td>
        <td>true</td>
        <td>false</td>
        <td>true</td>
        <td>true</td>
    </tr>
    <tr>
        <td>false</td>
        <td>NULL</td>
        <td>false</td>
        <td>NULL</td>
        <td>true</td>
    </tr>
    <tr>
        <td>false</td>
        <td>false</td>
        <td>false</td>
        <td>false</td>
        <td>true</td>
    </tr>  
</table>

I personally try to think this pragmatically. NULLs "bubble" in a way to resulting value. But what does it mean to evaluate ```true AND null => null```? It's not suprising that this is generally thought something that is from a painting by Salvador Dali.

![World of ternary logic](/img/title-missing/dali.jpg)

> **Picture 1.** Dali visioned pragmatic programmer in a world if ternary logic.

It's important to notice, that IF p and q are NOT NULLs all evaluations follow boolean logic exactly. This means that when you are using NOT NULL columns for joining, sorting, aggregating and such everything works as expected. I can see why this leads to conclusion that NULL should be abolished everywhere in database.

### EXTRA: No NULL semantics! Abolish NULL!

It's possible. For example Haskell takes this approach. In Haskell program no such thing as NULL exists. Instead, it has the concept of *Maybe a*, which can be *Nothing* or *Just a*. In Scala you find *Option* which can be *Some* or *None* on top of NULL. Loads of languages follow this approach.

## How avoiding NULL is usually done

Alternatives for NULL values in databases do exist. Next we describe most well-known strategies for avoiding the need to use NULLable columns in databases.

### Placeholder values

Most of the time when avoiding NULL we use replacement values for missing values. For instance, if we have street addresses in our database, we can just write empty string to our database when we do not know the address. In event  we don't know how many attendees were at given event we just write -1 to attendee\_count. Then time passes on and someone queries:

```sql
SELECT * FROM events WHERE attendee_count < 5;
```

Oh yes. You need to add condition for filtering those events with attendee\_count -1. When time passes by, the value that encodes missing value turns sort of hidden knowledge. If we tried to avoid problems originating from ternary logic, we actually created even bigger problem! When using NULL to encode unknown attendee count,  query just works straight because some great mind understood that SQL could work that way - it just simply falsifies comparision ```NULL < 5```. SQL would read as: "Give me all the events which had less than five attendees". If attendee count is not known it should not be included. Event could have had less than five attendees but more as well.

This problem is even bigger with more structural data types such as dates, timestamps and coordinates. 0 milliseconds since epoch is not a missing value. It is an instant 1.1.1970 12:00:00 (UTC). One could try to indicate with separate column if value is known or not? Oh please, you must be joking? Don't so that. It's even more hidden knowledge to your schema. "But with triggers we can..!" - you say. No, don't do that.

I personally prefer using NULL for missing values and -  if needed - constructing explicit handling for missing values with **IS NULL** and **IS NOT NULL** clauses.

### Foreign key pointing to row representing unknown value

One can encode missing values as a special rows in table.

```sql
CREATE TABLE country (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50)
);

INSERT INTO country VALUES(1, 'Unknown');
INSERT INTO country VALUES(2, 'Finland');
INSERT INTO country VALUES(3, 'Sweden');

CREATE TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    id_country INTEGER NOT NULL REFERENCES country(id)
);


INSERT INTO customer VALUES(1, 'Horst', 1);
INSERT INTO customer VALUES(2, 'Heikki', 2);
INSERT INTO customer VALUES(3, 'Lisbet', 3);
-- and so on..
```

I personally feel this approach suffers ultimately from the same problem than using replacement values does. It is hidden knowledge of that one row in country table is *special*. "Unknown" is not a country. On the other hand, I agree that this can be suitable strategy in some scenarios.

What about using NULLs in foreign key columns?

```sql
CREATE TABLE country (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    id_country INTEGER REFERENCES country(id)
);

INSERT INTO country VALUES(1, 'Finland');
INSERT INTO country VALUES(2, 'Sweden');

INSERT INTO customer VALUES(1, 'Heikki', 1);
INSERT INTO customer VALUES(2, 'Mirjami', 1);
INSERT INTO customer VALUES(3, 'Minna', 1);
INSERT INTO customer VALUES(4, 'Ingrid', 2);
INSERT INTO customer VALUES(5, 'Kristian', 2);
INSERT INTO customer VALUES(6, 'Steve', NULL);
INSERT INTO customer VALUES(7, 'Horst', NULL);

SELECT country.name, COUNT(customer.id_country)
    FROM customer LEFT JOIN country
        ON id_country = country.id
    GROUP BY country.id;

  name   | count
---------+-------
         |     0
 Sweden  |     2
 Finland |     3
(3 rows)
```

Note that result is **invalid**. I would expect count in first row to be 2 because there are tow customers with NULL in id_country. This originates from SQL Specification which specifies that (most) aggregate functions should ignore NULL values. The weirdest part is that COUNT(\*) does not ignore NULLs in similar fashion and thus:

```sql
SELECT country.name, COUNT(*)
    FROM customer LEFT JOIN country
        ON id_country = country.id
    GROUP BY country.id;

  name   | count
---------+-------
         |     2
 Sweden  |     2
 Finland |     3
(3 rows)
```

This is correct in our scenario and works at least in Postgresql. Lesson learned is that be extra certain of what you are doing when using aggregate functions to fields without NOT NULL constraint. I tend to think that when you need aggregation in database you should hide NULL values in some way. This can easily be done with views designated for aggregation.

```sql
CREATE VIEW customers_with_country AS
  SELECT * FROM customer WHERE id_country IS NOT NULL;

CREATE VIEW customers_without_country AS
  SELECT * FROM customer WHERE id_country IS NULL;

SELECT country.name, COUNT(*)
  FROM customers_with_country LEFT JOIN country
      ON id_country = country.id
  GROUP BY country.id;

  name   | count
---------+-------
 Sweden  |     2
 Finland |     3
(2 rows)

SELECT COUNT(*) AS customers_without_country_count
  FROM customers_without_country;

customers_without_country_count
---------------------------------
                              2
(1 row)
```

Something that must be considered in modern web apps is that because IO is basically only thing that costs something, you just might be better of by just materializing really raw result sets of tables and transform that data into your specific form. Of course with that functional wizardy such as *reduce* and *fold*. Clarity, testability and robustness is **much** more important than fastest possible response time - don't get me wrong, fast response times are crucial as well.

### Separate tables for values that can be missing

```sql
CREATE TABLE customer (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
CREATE TABLE customer_email (
    id_customer INTEGER REFERENCES customer(id),
    email VARCHAR(100) NOT NULL
);

INSERT INTO customer VALUES(1, 'Horst');
INSERT INTO customer VALUES(2, 'Jean-Luc');

INSERT INTO customer_email VALUES(1, 'horst@aol.com');

SELECT * FROM customer LEFT JOIN customer_email ON id = id_customer;

 id |   name   | id_customer |     email     
----+----------+-------------+---------------
  1 | Horst    |           1 | horst@aol.com
  2 | Jean-Luc |             |
(2 rows)

```

In this case, the main point is that you don't persist NULLs but ultimately you read NULLs from result set because of the LEFT JOIN. Updating can be bit cumbersome because you need to update multiple tables when updating user. But yes, this can be good solution in some situations and of course your application has precise transaction policy.

### Sixth normal form

[Sixth normal](https://en.wikipedia.org/wiki/Sixth_normal_form "Wikipedia, sixth normal form") form is way of structuring your database without explicit NULL values while maintaining the concept of missing value. Only problem is that a database in sixth normal form is really hard to construct and even harder to query - not to mention update - with SQL.

## How should I use those NULLs then?

Think of it this way. When you build world class software pay attention to things that exist always in your domain, but be sure to pay even more attention to things that can be **non-existent**. In your domain are loads of concepts which can be unknown, undefined or what ever they're called in your domain. Take some time to define what it actually means that value is missing.

If you have a table which contains column for consumed meal, take some time to think can this be NULL? If it can what does it mean? Does it mean that no meal was consumed or that we do not know if user have eaten anything today. "Sausages" is pretty obvious value, but you can get "Nothing" as an input from user. Of course, this has implications to UX-design and such. This is not simply a persistence layer problem but an integral definition of the whole application and no universal truths exist in this matter.

It wouldn't hurt to document in your schema what those NULLs mean in your context.

```sql
CREATE TABLE customer (
    id UUID PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,

    -- NULL means address is unknown
    -- Empty string means customer does not have an address
    address VARCHAR(100),

    -- NULL means email address in unknown
    -- Empty string is not accepted (program must validate input)  
    email VARCHAR(100)
);
```

Write your code with huge respect to this definition. Test your code automagically and make sure it represents and handles values in database with the same exact semantics. **Be extra sure** that **everyone** in your team share understanding how your missing data is represented in database! On top of programmers, PO:s and corresponding personnel should be aware of this semantics.

With *views* you can take a look to your data with those gnarly NULLs shadowed from queries. When you know, your view does not include NULLs you can use aggregation functions without any special attention. Think of it as a solving problem "what does it mean to count sum of collection of values which can contain unknown value".

Different DBMS's behave differently. Know your DBMS. Tinker around with it and test how it handles NULLs and equalities. Don't expect to know Postgres because you have worked with Oracle and vice versa. In Oracle ```'' = NULL``` is true. In MySQL ```' ' = ''``` is true. In Postgres ```' ' = ''``` is false and the list goes on.

## Real world scenario: Twitter and Instagram accounts for user

Just couple of weeks back we had requirement of storing users optional Instagram and Twitter accounts into our database. We started with schema:

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    -- ...
    -- ... other fields
    -- ...
    instagram_account VARCHAR(255),
    twitter_account VARCHAR(255)
);
```

We could have placed NOT NULL constraint to fields and use '' as a default value. Instead we took an approach where '' is an illegal value (it's clear that '' is illegal user name in Instagram and Twitter as well) and NULL represents the fact that 1) user does not have an account OR 2) user does not want to store account here. Because we were working with Scala we constructed approach where our data access layer reads SQL NULLs to Scala None:

```scala
case class
  User(id: Integer,
       /* Fields omitted */
       instagram: Option[String],
       twitter: Option[String])

User(1, ..., Some("instagram_monster"), None)      
```
Then we defined that application must translate empty string from form to None in case class, so user can erase account simply by clearing current value from form. Another possibility would have bee to store '' as missing account, but the we would have had to check if account does not equal to empty string and then fetch data from public API:s. I preferred NULL <-> None approach over '' <-> None, but i acknowledge one can disagree.

## Postscript

Take a minute and think how SQL syntax would look like if they hadn't chose string "NULL" to represent missing values in
clauses. I consider "NOT NULL" weird constraint as well. I would prefer that everything is "NOT NULL" by default and
field can be given extra allowance if needed.

```sql
-- NOT ACTUAL SQL!!!
CREATE TABLE customer (
    id UUID PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),

    address VARCHAR(500) ALLOW_MISSING,
    email VARCHAR(500) ALLOW_MISSING,    
)

SELECT * FROM customer WHERE address IS MISSING AND email LIKE '%@solita.fi';
SELECT * FROM customer WHERE email IS DEFINED;
-- NOT ACTUAL SQL!!!
```

Looks pretty good, doesn't it?
