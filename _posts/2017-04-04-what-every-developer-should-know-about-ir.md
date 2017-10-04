---
layout: post
title: What every developer should know about Information Retrieval
author: juhofriman
excerpt: Effective and intuitive search functionalities are crucial part of nearly every system. This blog post tries to introduce reader some of the science behind information retrieval (IR) as it is vastly studied since the sixties, yet the field is not too well known within the developer community.
tags:
- Information Retrieval
- Elasticsearch
- Postgresql
- Natural language processing
---

Effective and intuitive search functionalities are a crucial part of nearly every system, but my gut feeling is that the search functionalities are usually implemented in an ad hoc manner - just creating something that returns results to user and lets the user to tinker with search and just try to cope with it. This blog post tries to introduce reader some of the science behind information retrieval (IR) as it is vastly studied since the sixties, yet the field is not too well known within the developer community. A suggested reading list is collected at the end.

Information retrieval is an area where has happened a lot during the last couple of years and search algorithms (matching algorithms to be exact) are well kept business critical secrets. Focus is put to neural networks, machine learning and stuff like that, but this blog post follows much more traditional approaches. First we take a look at *naive approach*, then *boolean model* is examined and after that *vector space model* is introduced.

**I promise you, with well crafted and thought retrieval system your users will love you.**

Firstly, we define some essential concepts which will help us to understand the IR-models.

**Collection:** Collection of documents. Documents can be, but are not limited to, textual documents, html pages, rows in database, entries in document database and such. A library (like a real analog library, with real books and stuff - remember those?) has a collection.
**Document:** A single entry of information in collection. A document can be a html-page, a textual snippet, an entity from database or pretty much anything that can be reduced down into *terms*.
**Query:** An expression in which user tries to describe information need. Note that in information retrieval, query is usually considered pretty low level thing, and usually queries are constructred with well crafted user interfaces. The words that you write to Google are expressions of your information need, but I'm certain that Google does excessive processing when forming the executed query.
**Term:** A term is an atom of information retrieval. It usually is pretty equivalent to *word*, but not always as we’ll see later on. Both document and query contain terms.
**Result set:** A list of documents matching the query. Result set can contain all data directly or just references to documents.
**Index:** Index is a “place” or a “structure” from with we can lookup which documents satisfy our query. Books usually have indexes and yes, database indexes can effectively be seen as similar structures. They utilize b-trees and such for algorithmic efficiency, but the idea is very much the same. It is pretty easy find all mentions of “Frodo” from the Lord of the Rings, if someone has already collected all the pages “Frodo” is mentioned in, rather than browsing through all the pages and skimming for mentions.
**Relevance:** Relevance denotes the relevance of certain document against certain *information need*. A document about cats' eating habits is not relevant when I want to know about dogs' eating habits, but it is relevant when I want to know about cats.

## Naive approach

I call naive approach this super simple retrieval pattern, which will get you started, but is probably not that efficient in the end. You can just wildcard query term from both ends and match directly. In SQL you could do something like this:

```SQL
SELECT * FROM product_category WHERE category_name LIKE '%tofu%'
```

If you have a text input field with cool autocomplete, this just might be enough. Usually you execute query when query term is three or more letters long to reduce the size of result set. This is not information retrieval in the strict sense, but more of an UX improvement for drop down selects with lots of options.

This naive pattern can also be targeted to full text fields.

```SQL
SELECT * FROM blog WHERE text LIKE '%dog%' AND text LIKE '%eat%';
```

Presented SQL query can be read as: "give me every blog that contains both character sequences 'dog' and 'eat'". This might work in small collections, but clever reader like you can see problems with this implementation.

Clearly we need something better. We need an *index*.

## Boolean retrieval model

Let's take it back to the old school. When the idea of an information retrieval system was first introduced, it was built on top of the boolean logic. It was though that users could *express* their *information needs* with simple boolean logic clauses such as:

```
dog AND eats
```

Which means "give me all the documents containing both words *dog* and *eats*". In the information retrieval science literature, this is refered as an exact match model because nothing is done to query terms (dog + diet) and documents either match or do not match.

To execute this against a *collection*, we need an *index*.

When having documents:

| id    |  doc                  |
|-------|-----------------------|
| 1     | A dog eats dog food   |
| 2     | A cat eats mice.      |

We can construct an *index* such as

| term    |  found at  |
|---------|------------|
| a       | 1,2        |
| dog     | 1          |
| eats    | 1,2        |
| dog     | 1          |
| food    | 1          |
| cat     | 2          |
| mice    | 2          |

Our query matches to document 1 but not document 2, because even though "eats" is found in both documents "dog" exists only in document 1. Note that you could implement this *index* by yourself to database, but you're probably better of by using something from the box. Most DBMS:s have full text indexing capabilities out of the box, or you can use something like Elasticsearch, Lucene or SOLR. In this example, we wrote "a" to our index as well, but it is usually beneficial to include a list of stop words which are excluded from *index* and *queries*.

If we had a bigger *collection*, could it be, that there exists relevant documents which do not talk about dogs with the word "dog", but refer to the same animal as "hound" or "mongrel" or "pooch" or even "stray"? With boolean model we can craft a query combining synonyms within OR-facets such as:

```
(dog OR hound OR mongrel OR pooch OR stray)
AND
(diet OR nourishment OR nutrition OR sustenance)
```

Could some of the documents contain same words only in plural form?

```
(dog OR dogs OR hound OR hounds OR mongrel OR mongrels
  OR pooch OR pooches OR stray)
AND
(diet OR nourishment OR nutrition OR sustenance)
```

Or we might even utilize wildcard operator:

```
(dog* OR hound* OR mongrel* OR pooch* OR stray*)
AND
(diet* OR nourishment* OR nutrition* OR sustenance*)
```

We begin to see, that we should be really good with words or even have a dictionary with us when we craft our queries. Making queries like this, is a job for a professional information retrieval specialist. Building those OR-facets seems a horrible task and practically no system is anymore implemented like this. Yet, some of the largest and dominant systems still use boolean model as a main interface - it's fair to say, that these types of systems are meant for expert usage.

There has been loads of systems that use synonym dictionaries to add synonyms automatically to queries, so user so user doesn't have to think the synonyms at all. This is called *query expansion*, which is a very important technique when helping user with the queries. The problem is that you need a really good synonym dataset to make something like this automatically. This is usually really beneficial in large collections that deal with wide range of subjects - such as news collections - and is not that beneficial in smaller rather heavily specialised collections where users usually know the terms documents contain. Query expansion is not limited to the boolean model, but usable in various other retrieval models as well, which we'll take a peek next.

## Vector space model

Vector space model is nowadays the most predominant retrieval model. I try not to get too mathematical, but in vector space model index is defined as a vector space as the name suggests. Now, this might seem like a total **gibberish**, but one can think vector space as documents being vectors in space in which terms are dimensions (yes, there really are quite a lot of dimensions...) and the weight of the terms is "the juice" how far these vectors reach. Because vector calculus contains some very intriguing methods for calculating similarities we take advantage of that, and actually calculate the weighted similarity between query and a document and order the result set with that. This is called *partial matching*, because the documents that do not contain all the terms in query can easily be included to the result set. Interested reader is suggested to revise through suggested reading below, as we will not address the mathematical basis more here.

It's important to notice that in a pure vector space model, documents and queries are effectively equivalent, and hence "give me more like this document" -functionality should be trivial to implement.

### TW = TF * IDF

TW = TF * IDF is the e = mc^2 of the information retrieval, in which:

**TW**: *term weight in document*
**TF**: *term frequency* - How many times term exists in document
**IDF**: *inverse document frequency* - inverse number of how many times term exists in collection

Most retrieval models choose the assumption that *if a term is common in a the document but rare in collection, it's really good to distinguish documents from each other within that collection*. So, if a document mentions lots of "dog", it really must be about dogs. It's especially important if "dog" is quite rare term in the whole collection. Please note, that this assumption might as well be wrong within collection, but it still is one of the best assumptions we can make when dealing with texts in natural language. Think of it this way: would it make any sense to query with term "dog" to a collection of texts abouts dogs?

TF * IDF weight can be calculated in most simple form for term T in document D belonging to collection C as: T occurrences in D * (1 / T occurrences in C). Usually frequencies are further normalized logarithmically, as we probably want to raise weight of those documents with one or two mentions and diminish the juice on those documents which just repeat the same term over and over, but let's keep things simple.

| id    |  doc                                                                  |
|-------|-----------------------------------------------------------------------|
| 1     | A dog eats canned dog food. A dog does not eat chocolate.             |
| 2     | Cats eat mice.                                                        |
| 3     | Cats are usually cute. Dogs too.                                      |

TF for couple of terms in documents.

| term  | TF in documents                            | TF in collection        |
|-------|----------------------------------------------------------------------|
| dog   | **1:** 3 **2:** 0 **3:** 1 **4:** 0        | 4                       |
| cat   | **1:** 0 **2:** 1 **3:** 1 **4:** 0        | 3                       |

By the formula we can calculate that weight for "dog" is 0.75 `= 3 * (1 / 4)` for document 1 and 0.25 `= 1 * (1 / 4)` for document 2. From this we reason that document 1 is more relevant than documents 2 for term "dog" and thus should be raised higher in resultset. Note that weight is not necessarily used to reason if the document is found at all but to order the resultset.

Matching algorithms is a vast subject, of which entire books are written, so it can't be thoroughly addressed here. Suggested further reading can be found at the end of this post.

## Vector space vs. boolean model

These models are usually kept clearly separate in research and literature. Most of the real life information retrieval systems are actually hybrid of these using ideas from various sources. For instance predominant Elasticsearch is a hybrid of boolean model and vector space model interpretation. It uses boolean model for matching documents, but utilizes vector space influenced sorting algorithm to sort result set. Postgres has a really good full text search support and to my understanding it utilizes vector space model pretty cleanly.

Google utilized originally really simple TF * IDF vector space model system with "page rank" added. The page rank added more weight to pages which are broadly linked from the other pages and similarly diminished weight of the pages that were seldom linked. For now, we don't know basically anything how Google actually works.

Other models of information retrieval include probabilistic model(s), latent semantic indexing, the binary independence retrieval, best-match retrieval and so on.

# Natural language processing

*Terms* are the atoms of full text information retrieval, and they are called *terms* instead of *words* because usually all kinds of preprocessing is done before they are written to index and query is executed against index. *Terms* come out of *text* with the processes of *tokenisation* (splitting separate words) and *analysation* (processing word to indexed form).

When the boolean retrieval model was discussed, we already encountered problems with words as they inflect. In boolean model, we addressed to that with OR-facets or using wild cards, but that can be really hard to lazy users who have used to Google.

There must be something better, right?

We mentioned *query expansion* already and next we take a look at *stop word lists* and *stemming*.

## Stop word list

Usually we just drop words that are not that meaningful in information retrieval context. Stop words in English usually consist of words such as: *a, an, the, none, some, he, she, it, his, her* and so on. When we tokenise raw text, the first thing to do is just drop these and do not add them to index at all. Similarly, when query is processed, the same exact stop word list should be used to filter query as well. It's nice, if user writes query `can I find me a little dog` which effectively queries for `find little dog`.

These words are really common and do not usually give much information about the context of the text. They are just noise, because we have an assumption that term frequencies tell us about the context and content of the texts. It's completely another thing if we try to do something like *question answering*, which the process of finding answers to queries presented in natural language from a collection of texts in natural language. That is really hard in English, but it's almost impossible in Finnish!

## Stemming

Stemming is an elemental technique in information retrieval as it is computationally and result wise performant. Stemming means trying to *algoritmically* match different inflects of word to the same *lexeme* (run, runs, runned all have same lexeme *run*). The lexeme stemming produces is not always lexically correct, but it does not matter as long as we get the same lexeme for different inflects. When we create index, we tokenise the raw text, apply stemmer to the terms and write them to the index.

Postgres has a nice interface to the most well known open source stemmer called Snowball stemmer. Snowball is available in Elasticsearch as well and it even contains an algorithm for Finnish language.

```
postgres=# SELECT ts_lexize('english_stem', 'dog');
 ts_lexize
-----------
 {dog}
(1 row)

postgres=# SELECT ts_lexize('english_stem', 'dogs');
 ts_lexize
-----------
 {dog}
(1 row)
```

Plural 'dogs' is reduced to lexeme 'dog' as we wanted. Finnish language is way more harder than english when it comes to inflectional forms. It's suprising that Snowball is actually pretty effective in Finnish as well. It's not perfect and it will make mistakes, but trust me - it's way better than using wild cards both side.

```
postgres=# SELECT ts_lexize('finnish_stem', 'juoksija');
 ts_lexize
-----------
 {juoksij}
(1 row)

postgres=# SELECT ts_lexize('finnish_stem', 'juoksijan');
 ts_lexize
-----------
 {juoksij}
(1 row)

postgres=# SELECT ts_lexize('finnish_stem', 'juoksijoita');
 ts_lexize
-----------
 {juoksij}
(1 row)

postgres=# SELECT ts_lexize('finnish_stem', 'juoksijat');
 ts_lexize
-----------
 {juoksij}
(1 row)
```

**Important:** *When you use stemmers, use them when writing to index, so that index contains stemmed lexemes and use same actual implementation of that stemmer to queries as well. When you use stemmer, you should not use wildcard queries! And remember that stemmers are language dependant.*

Stemming can also be done lexixally correct by using dictionary. Irregular forms (mouse, mice) are usually problematic for algorithmic stemmers, and this can be avoided with a dictionary if one is available. Unfortunaly, we usually do not have a good dictionary available.

You can also use query expansion with stemming, but remember to stem your synonyms as well. If you do not have a good synonym data, maybe you can create a UI for your users, by which they can add and remove synonyms to the system? You can also use query expansion for handling inflects in stemming, with adding more inflectional forms automatically. You should start with elementary key concepts in your domain.

Usually in Finnish compound words are really hard task with information retrieval. My suggestion is that in general you should not try to solve this completely, because you just can't. Stemmers work ok with compound words to my experience, and splitting compounds requires some really good dictionary data and really good algorithms. `Mustekala` (octopus, literally 'ink fish') gets stem `mustekal` and at least to my liking, I should not find that with query terms `muste` (ink) or `kala` (fish). But some words like `kuusijuhla` (synonym for christmas, literally spruce celebration) make more sense when splitted.

## Not just algorithms

The whole idea of information retrieval research is to help user to get the most relevant documents to the top of the result list. This is raw information retrieval research, heavily rooted on computer science and mathematics. As a field of study we usually refer to *information seeking behavior* when we look more human approach to information retrieval. This is a really broad field of study, but most of it starts from assumption that user has *an information need* which causes *cognitive dissonance*, sort of a gap, which user has to get over to by finding *information*. Reader is suggested to skim Wikipedia on [information seeking behaviour](https://en.wikipedia.org/wiki/Information_seeking_behavior) as a starting point.

Even though this post talked only about full text searches, most of the systems usually benefit for having structural constraints to searches, such as "give me all the documents from department X that match to query 'dogs diet'". Naturally UX design is a really important part in crafting lovable search functionalities, and information retrieval is truly a multidisciplinary field of study.

## Suggested reading

*Exploring the similarity space*
*(J. Zobel and A. Moffat, SIGIR Forum, 1998)*

*Information Retrieval Models: Foundations and Relationships*
*Thomas Roelleke, 2013*

*A language modeling approach to information retrieval*
*(J. Ponte and W. B. Croft, SIGIR, 1998)*

*Natural language processing for information retrieval*
*(D. D. Lewis and K. Sparck Jones, CACM, 1996)*

*A probabilistic model of information retrieval: development and comparative experiments. Parts I and II*
*(K. Sparck Jones, S. Walker, and S. E. Robertson, IPM, 2000)*

*A taxonomy of web search*
*(A. Broder, SIGIR Forum, 2002)*

https://www.csee.umbc.edu/~ian/irF02/lectures/07Models-VSM.pdf
