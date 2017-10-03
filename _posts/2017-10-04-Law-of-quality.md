---
layout: post
title: The Law of Three for Software Quality
author: lokori
excerpt: There is a simple rule-of-thumb for software quality which seems to remain true over the years: 
If the system properly handles dates, characters and money, it has good quality. 
Short of scientific evidence, empirical arguments are provided. Try and see how your system measures up against this law.
tags:
- quality
- bugs
- encoding
- SQL
- Java
---

## The Law of Three

This is the law. 

### If the system properly handles dates, characters and money, it has good quality.

I have been talking about it every now and then for quite some time. It seems to hold true in the world of professional software development where I work as years pass by. Most of the real world systems handle characters and dates in some fashion, even if money is not involved and even getting these two right is a major challenge.

This post examines the difficulties of these three aspects through some examples to shed some light into why it's actually quite difficult. I believe I have never seen a software system of non-trivial size which got all these right.

## Dates

Date and time are something familiar to us, but the devil is in the details. [The Long, Painful History of Time](http://naggum.no/lugm-time.html) gives a good account of the intricacies of date and time.

Provided you understand this historical context and time zones, this is only half of the victory. Let's consider Java and a standard JDBC interface to a relation database, say PostgreSQL. 

Originally Java had two Date classes: java.util.Date and java.sql.Date. Despite Java core developers being smart, it
turned out that java.util.Date had issues. A decade later Java time API was rewritten in [JSR 310](https://community.oracle.com/docs/DOC-983209). And then [JodaTime](http://www.joda.org/joda-time/) came to rescue poor Java. Now the confused developer has deprecated (and broken) legacy classes laying around, some newer ones to choose from and headache follows.

Okay, but surely the situation is better in SQL databases? We'll define our table like this:
```
CREATE TABLE dadas
  (
    le_time TIMESTAMPT NOT NULL
  ) ;
```

Ops, we just failed. According to [PostgreSQL documentation](https://www.postgresql.org/docs/9.1/static/datatype-datetime.html) this leaves out timezone, which means effectively system default. It is inadvisable to assume that system default in the database server is the same as in the application server, unless you somehow explicitly control it.

```
The SQL standard requires that writing just timestamp be equivalent to timestamp without time zone, and PostgreSQL honors that behavior. (Releases prior to 7.3 treated it as timestamp with time zone.)
```

Even if you have everything under control in the backend, what about the UI? Enter Javascript and let the mortals trebmle.

```
new Date(2012,12,12)
Sat Jan 12 2013 00:00:00 GMT+0200 (EET)
new Date(2012,0,1)
Sun Jan 01 2012 00:00:00 GMT+0200 (EET)
new Date(2012,-1,1)
Thu Dec 01 2011 00:00:00 GMT+0200 (EET)
```

Javascript is kind enough to allow data slip without warnings or exceptions like that. You get dates, just maybe a bit different dates from what you expected. And what might be the timezone should you do something like that? You can't rely on the user's browser to have any specific timezone set even if you can control the backend server. 

Good luck getting all these layers to work perfectly in all situations.

## The characters

Unless you are a veteran with a lot of scars, this [old article about encoding](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/) from Joel Spolsky should give you something to think about.

As with dates, it doesn't end here. With Java your source code and strings at least have some defined encodings and characters sets. Python developers are not so fortunate, see this: [Unicode in Python](https://docs.python.org/2/howto/unicode.html). 

Again, remember to check your relational database for surprises. On particularly interesting one is the order of letters in a SQL statement:

```
select * from winners order by name;
```

As article on [Alphabetical Order](https://en.wikipedia.org/wiki/Alphabetical_order) in Wikipedia informs us, order of letters in the alphabet depends on the country. And even has been changed in some countries quite recently. This may result in a bit surprising orderings as some characters can even have equal standing in the order. And do you actually know what ordering your database server is using now?

Characters also need to be escaped, encoded and re-enconded multiple times as they travel with [URL encoding](https://www.w3schools.com/TagS/ref_urlencode.asp), [HTML encoding](https://www.w3schools.com/html/html_charset.asp) and many other forms of encoding. It is anything but easy to have everything working perfectly in a complex modern software system.

## Show me the money

Money may actually be the easiest of the three. Perhaps the two most difficult things to remember are:
1. Be careful with rounding and precision. 1/3 is an infinite number, even with some sort of "big decimal".
2. If you convert from one currency to another all sort of issues arise. Where did you get your currency rate from? 

My advice is to create an abstraction or wrapper for handling money. Instead of having a ```float amount``` (gasp, the horror) or ```BigDecimal amount``` it would be better to have ```Money amount``` with *Money* handling the roundings somehow. 

Eventually you will have to round money to some precision. Then all sort of funny issues may come up, like the sum of invoice rows (rounded) may not actually equal the total monetary amount stated in the invoice.

## Does it matter?

It doesn't, until it matters. It depends on the context if some mistake with encoding of characters presents a marginal non-issue, a serious security flaw or embarrasing UI glitch. Similarly, improper handling of date and time may not be pose any risk from the business perspective.

However, it does matter that the programmers are aware of these things and intricacies which may be significant. How could they otherwise judge if something is important or not? Consider also that in most cases, the correct program takes no more time to write, provided you know know what you are doing. Researching and learning takes time and usually occurs after some problem has caused real measurable consequences, like a flow of bug reports from the end users. Locked accounts. Missing payments. That's how I learnt what little I know about these things.






