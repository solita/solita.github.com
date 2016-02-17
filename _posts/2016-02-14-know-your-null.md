---
layout: post
title: Know your NULL
author: juhofriman
excerpt: I'm here to argue that NULL values belongs to relational database and are actually great abstraction. But, with great power comes great responsibility.
categories: 
- SQL
tags: 
- SQL
- NULL 
---

During my career I have witnessed real witty and bright minded software developers being way too strict about NULL values in databases. 
They do just about everything to define schema which does not allow NULLs anywhere. I call them NULL phobics.
I'm not here to mock great minds, such as C.J. Date who has taken really strong stance against NULLs in relational
databases. This has been ongoing debate in relational database community since the first relational databases. I personally feel, 
that when it comes to software development, we as a developers should have reasonable amount
of practical stance, but in the same time should be aware of the underlying theory.

When we create business critical programs we must be able to represent values that are missing or unkown. In relational
algebra no such ugly concept as "missing value" exist. But the world we describe with our programs in is vague and imperfect 
and thus shall our applications be when it comes to data. We don't have all the data we 
need all the time, but instead, in most of the situations data keeps popping from here and there.

I'm here to argue that NULL values belong to relational database and are actually great abstraction. 
But, with great power comes great responsibility.

*Examples are tested with Postgresql 9.5.0*

## Semantics of NULL

This writing concerns only NULL values in relational databases, but as a background information, we briefly introduce
three well known semantics of NULL.

### 1) NULL is Falsy

In many programming languages NULL is *falsy*. You can i.e evaluate it and it "is false".

```javascript
if(null) {
    // not executed
} else {
    // executed!
}
```

LISPs follow this semantics and most dynamically typed languages such as Ruby and Python.

### 2) Evaluation of NULL is illegal

NULL can also be considered something that can not be evaluated. For example Java takes this approach and throws 
NullPointerException when evaluating something like mentioned.

```java
if(null) {
    // Not executed, instead a NullPointerException is thrown
    // when clause is evaluated
} 
```

Note that you can evaluate if pointer is pointing to NULL, but you can't make a boolean out of NULL which is the
case in NULL is falsy semantics.

```java
Object a = null;
if(a == null) {
    // Executed
} 
```

### 3) Three-value logic

Relational databases take yet another approach on how to handle NULL values. 
They introduce something that it known as a three-value logic (trinary logic, ternary logic), which can be thought as 
an extension to well familiar boolean logic. Three-value logic takes to account the fact that value can indeed be
missing and clauses must still be evaluable. The problem is that it yields NULL as a result in some comparisions.

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

I personally try to think this pragmatically. NULLs "bubble" in a way to resulting value. But it's not suprising
that this is generally thought something that is from a painting by Salvador Dali.

![World of ternary logic](/img/sql-nulls/dali.jpg)

> **Picture 1.** Dali visioned pragmatic programmer in a world if ternary logic.

It's important to notice, that IF p and q are NOT NULLs all evaluations follow boolean logic exactly. This means that
when you are using NOT NULL columns for joining, sorting, aggregating and such everything works as expected. I can
see why this leads to conclusion that NULL should be abolished everywhere in database.

#### EXTRA: No NULL semantics! Abolish NULL!

It's possible. For example Haskell takes this approach. In Haskell program no such thing as NULL exists. 
Instead, it has the concept of *Maybe a*, which can be *Nothing* or *Just a*. In Scala you find *Option* which 
can be *Some* of *None* on top of NULL. Loads of languages follow this approach.

## How avoiding NULL is usually done

Alternatives for NULL values in databases do exist. Next we describe most well-known strategies for avoiding the need to use
NULLable columns in databases.

### Placeholder values

Most of the time, null phobics use replacement values for missing values. For instance, if we have street addresses in our
database, we can just write empty string to our database when we do not know the address. If we don't know how
many coaches we have in our train we just write -1 to our field representing couach_count. Most NULL phobics consider
this a good approach because it shadows ternary logic from queries. Yes it does in a way, but it also brings another problems. 
Consider query for finding all short trains in the system:

```SQL
SELECT * FROM trains WHERE coach_count < 5;
```

Oh yes. You need to add condition for filtering those ghost trains with coach\_count -1. And when time passes by
that -1 encodes missing value turns sort of hidden knowledge. If we tried to avoid problems originating from ternary logic,
we actually created even bigger problem! When using NULL to encode unknown coach count, query
just works straight because some great mind understood that SQL could work that way - it just simply falsifies comparision
```NULL < 5```. Doesn't it look pretty pragmatic? When querying for short trains we do not want those with unkown
coach count. When dealing with those, it is completely different issue.

This problem is even bigger with more structural data types, such as dates, timestamps, coordinates and such.
0 milliseconds since epoch is not missing value. It is an instant 1.1.1970 12:00:00 (UTC). Indicate with separate column
if value is known or not? Oh please, you must be joking? Don't so that. It's even more hidden knowledge 
to your schema. "But with triggers we can..!" - you say. No, don't do that.

### Foreign key pointing to row representing unkown value

One can encode missing values as a special rows in table.

```SQL
CREATE TABLE country (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50)
);

INSERT INTO country VALUES(1, 'Unkown');
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

I personally feel this approach suffers ultimately from the same problem than using replacement values does. It is hidden 
knowledge of that one row in country table is *special*. It's not a country. On the other hand, I agree that this can 
be suitable strategy in some scenarios.

What about using NULLs in foreign key columns?

```SQL
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

Note that result is **invalid**. I would expect count in first row to be 2. This originates from SQL Specification which
specifies that (most) aggregate functions should ignore NULL values. The weirdest part is that COUNT(*) does not
ignore NULLs in similar fashion and thus:

```SQL
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

This is correct in our scenario and works at least in Postgresql. Lesson learned is that be extra certain of what you 
are doing when using aggregate functions to fields without NOT NULL constraint.

It is also something that must be considered in modern web apps, that because IO is basically only thing that costs 
something, you just might be better of by just materializing really raw result sets of tables and transform that data into
your specific form. Of course with that functional wizardy such as *reduce* and *fold*. Clarity and robustness is
**much** more important than fastest possible response time - don't get me wrong, fast response times are crucial.

### Sixth normal form

Sixth normal form is way of structuring you're database without explicit NULL values maintaining the concept of 
missing value. In sixth normal form missing values are represented as references to missing values. 
Only problem is that database in sixth normal form is really hard to construct and even harder to query - 
not to mention update - with SQL.

## How should I use those NULLs then?

Think of it this way. When you build world class software pay attention to things that exist always in your domain,
but be sure to pay even more attention to things that can be **non-existent**. In your domain are loads of concepts
which can be unknown, undefined or what ever they're called in your domain. Take some time to define what it actually 
means that value is missing.

If you have a table which contains column for consumed meal, take some time to think can this be NULL? If it can
what does it mean? Does it mean that no meal was consumed or that we do not know if user have eaten anything today.
"Sausages" is pretty obvious value, but you can get "Nothing" as an input from user. Of course, this has implications
to UX-design and such. This is not simply a persistence layer problem but an integral definition of the whole application.
No universal truths exist in this matter.

It wouldn't hurt to document in your schema what those NULLs mean in your context. 

```SQL
CREATE TABLE customer (
    id UUID PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    
    -- NULL means address is unknown
    -- Empty string means customer does not have an address
    address VARCHAR(100), 

    -- NULL means email address in unkown
    -- Empty string is not accepted (program must validate input)  
    email VARHCAR(100)
)
```

Write your code with huge respect to this definition. Test your code automagically and make sure it represents and handles 
values in database with the same exact semantics. **Be extra sure** that **everyone** in your team share understanding how
your missing data is represented in database! On top of programmers, PO:s and corresponding personnel should be aware 
of this semantics.

With *views* you can take a look to your data with those gnarly NULLs shadowed from queries. In case of our train example
we could define something like:

```SQL
CREATE VIEW ghost_trains AS
    SELECT *
    FROM trains
    WHERE coach_count IS NULL;
    
CREATE VIEW trains_with_known_coach_count AS
    SELECT *
    FROM trains
    WHERE coach_count IS NOT NULL;
```

Different DBMS's behave differently. Know your DBMS. Tinker around with it and test how it handles NULLs and
equalities. Don't expect to know Postgres because you have worked with Oracle and vice versa.

## Postscript

Take a minute and think how SQL syntax would look like if they hadn't chose string "NULL" to represent missing values in
clauses. I consider "NOT NULL" weird constraint as well. I would prefer that everything is "NOT NULL" by default and
field can be given extra allowance if needed.

```SQL
-- NOT ACTUAL SQL!!!
CREATE TABLE customer (
    id UUID PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    
    address VARCHAR(500) ALLOW_MISSING,
    email VARCHAR(500) ALLOW_MISSING,    
)

SELECT * FROM customer WHERE address IS MISSING AND email LIKE '%@solita.fi';
SELECT * FROM customer WHERE email IS MISSING;
-- NOT ACTUAL SQL!!!
```

Looks pretty good, doesn't it?