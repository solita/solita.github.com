---
layout: post
title: About languages
author: lokori
excerpt: Form follows function in great design. Interestingly we can and should now eliminate barriers between form and function. The Clojure train is accelerating!
tags: Clojure, Lisp, Datomic, Prolog
---
<p></p>

## What's this about and what it's not about

I offer a brief peek at recent and older developments on programming languages and how they relate to some topics outside 
the field of computer programming. And building on that somewhat unconventional base I'll explain why Clojure is totally
awesome.

That's all. No fight over paradigms and languages here.


## The secret of great design
  
In 1896 [Form follows function](http://en.wikipedia.org/wiki/Form_follows_function) becomes a law.
     
Lois Sullivan stated about everything: 
>"that form ever follows function. This is the law."

It really is that simple! There is of course much to say about how this can be achieved, but that's another post.

## A short and somewhat biased history lesson
     
### 1929 People think about the concept of [linguistic relativity](http://en.wikipedia.org/wiki/Linguistic_relativity)
     
A cunning linguist named Sapir states that natural language constrains and shapes our thought processes. 
Later this is refined and known as [Sapir-Whorf hypothesis](http://plato.stanford.edu/entries/relativism/supplement2.html). 
		
### 1960 A new "programming language" for so called "computers" is born
      
The world does not notice because most people have never seen any computers, but
John McCarthy defines [Lisp](http://en.wikipedia.org/wiki/Lisp_(programming_language\)) anyway. For fun and profit.
      
In it's core it is small, elegant and extremely powerful. AI researchers go wild,
people doing practical things yawn. Neither camp understands.
      
Most striking perhaps is the design where form and function are interconvertible. This is based on 
so called [Lisp macros](http://stackoverflow.com/questions/267862/what-makes-lisp-macros-so-special) and REPL
which neatly addresses Sapir-Whorf hypothesis by making the language fully extensible and unconstrained.


### 1972 programmers find logic

[Mycroft Holmes](http://en.wikipedia.org/wiki/Mycroft_Holmes) is very excited. He finally gets to resign from 
his human computer post since [Prolog](http://en.wikipedia.org/wiki/Prolog) takes his place with it's fact-based data storage and logic programming.
      
### 1998 Java Architect denounces Java, praises Lisp

In a great talk titled [Growing a Language](http://cs.au.dk/~hosc/local/HOSC-12-3-pp221-236.pdf) Guy Steele,
one of the main architects behind Java, admits that Lisp got it right when they made the language
extensible with the macros. He states it in no uncertain terms:

>"I should not design a small language, and I should not design a
large one. I need to design a language that can grow. I need to plan ways in which it might
grow—but I need, too, to leave some choices so that other persons can make those choices
at a later time"


### 2000's known programmers admit using Lisp 

In 2003 [Paul Graham comes out of the closet](http://www.paulgraham.com/avg.html) and talks openly about his addiction to Lisp.

In 2006 Steve Yegge talks about his experiences and why [Java was not enough](http://steve-yegge.blogspot.fi/2006/03/execution-in-kingdom-of-nouns.html)
in the end though the first samples were free.

### 2007 Lisp is revived from the graveyard

Secretly Rich Hickey has listened to all this. After reading a remarkable collection of 
[extraordinarily fine literature](http://www.amazon.com/Clojure-Bookshelf/lm/R3LG3ZBZS4GCTH) he has created a new 
form of Lisp.

The time is now ripe. The voice of Rich Hickey booms: 
>"repent now thou Java programmers, I give thee a [practical Lisp](http://clojure.org/) thou and all thy kin can use."
	  
Nobody listens.
	  
### 2010 (let \[Datomic\] (loose :on :the :world)
      
Rich Hickey's hammer and anvil are steaming hot. With some friends he forges a new database which combines
Prolog's fact based view of data with a practical implementation and powerful query language. 
Putting time and revision history in is a nice plus.

Nobody understands [Datomic](http://www.datomic.com/) but the bang of the hammer is now heard far away.

### 2013 Public sightings of Clojure programmers

Clojure programmers are proven to exist outside controlled environments. Even here at [Tampere](http://www.clojutre.org) we
have witnessed this and our capital [Helsinki follows suit](http://reaktordevday.fi/2013/#speakers).

## There is a great disturbance in the Force

What we now have therefore is a practical JVM stack where *data*, *form* and *function* are all interconvertible
and expressible in the same very powerful, yet elegant language. There is no "impedance mismatch" in this stack.

I stand in awe.

## The "functional train" is leaving the platform

Last week we got a greenish light to go ahead with Clojure in our project. This is not the first Clojure project for 
Solita, but first real world Clojure project for me. I have been sitting on the metaphorical "functional train" for some
years already. Patience is a virtue and now we are finally moving! 

I look forward to enjoyable, speedy and luxurious ride on this train.  

