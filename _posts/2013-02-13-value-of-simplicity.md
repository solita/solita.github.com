---
layout: post
title: Value of Simplicity
author: lokori
excerpt: Seize the day and simplify your design. Finding a simple solution to a complex problem is one of the ultimate achievements. In this post I try to convince you and briefly touch the foundations on which one can build a simple solution. 
tags: Simplicity, software architecture, software design, normal form
---

There is value on a simple solution, but most software systems are way too complex. 
It need not be this way, especially in these days of high computing power, but first we must
recognize the value of simplicity.

You need not take my word on the importance of simplicity. It's value has been recognized already:

 Albert Einstein:
>"If you can't explain it to a six year old, you don't understand it yourself." 

Leonardo Da Vinci:
>"Simplicity is the ultimate sophistication." 

Antoine de Saint-Exupery:
>Perfection (in design) is achieved not when there is nothing more to add, but rather when there is nothing more to take away 


### A brief history

When I started programmming seriously about twenty years ago, most software systems were 
relatively small (aside from huge mainframe systems which were invisible) stand-alone applications. 
Concurrency was a non-issue back then and most of my effort was spent on making things efficient
in terms of CPU and memory (time and space for the theorists). 

Much has changed - a modern CPU is now multithreaded and extremely powerful, internet is everywhere 
and the applications are now integrated to other systems in almost real-time. The problem and 
solution domains have become so complex that no single person can completely master everything.

The way we approach programming has not changed to balance this. The languages have more abstractions and 
there are wonderful libraries. There's the agile movement and all that, but none of these really
adresses the *design* part of *software* design. 


### Taming the complexity of the problem domain

A rich and complex problem domain leads to complex (data) model that is hard to understand unless
you do something about it. 

According the traditional teachings of the relational database posse leaders, one should aim for 
[normalization](http://en.wikipedia.org/wiki/Database_normalization) above all else. This is what they
say:
>A standard piece of database design guidance is that the designer should create a fully normalized design; selective denormalization can subsequently be performed for performance reasons.

Horse hockey. A normal form database design is just a tradeoff that maximizes correctness and minimizes space disregarding almost everything else. Not
mentioning other worthy goals such as making the database user's work (the programmer) easy is absurd. A fully normalized database with 500+ tables 
takes considerable effort to understand, design or use. Been there, done that, not going there again.

Regardless of normal form, there is the important realization that "All models are wrong. some are useful". While George Box
was not talking about data models, this is sound advice everywhere. There are always rare marginal cases that
would be hopelessly messy to handle. Just cut them out of the algorithms or approximate them - that's what 
(software) *design* is about.


### Mastering the solution domain ###

The solution domain is where we usually live as developers. It is our territory where we should be in control
and any complexity is therefore unavoidable and a necessary evil. But is this actually true? 

#### What language 

The battle about which language is "best" seems everlasting, though the argued languages change. 
As a programmer I think [Paul Graham's BLUP paradox](http://www.paulgraham.com/avg.html) is spot on 
and we are certainly not using the best tools available.

But as an architect, I have to balance the technical merits over the practical issues.
Perhaps a Java solution is inferior, in a theoretical sense, to some Haskell code or 
Scala turbocharged with some macro magic, but what would it mean to choose the "better"?

Development of a Haskell based solution would not be easy unless the whole team consists of 
some very peculiar people. Mortals will not find it easy to understand Haskell or Scala macros. 
Even if they do, are they able to take advantage of everything the language has to offer? 

I'm not saying we should stick with what we have, but languages do not write software. People do.

#### Composability and modularity are your best friends

Always aim for modular pieces with a single clear responsibility. This applies to all levels 
- a method, a class, a module, a software system. I could say more, but others have already
written a lot about this.

[Software creativity 2.0](http://www.amazon.com/Software-Creativity-2-0-Robert-Glass/dp/0977213315), chapter 11.2. Creativity And Software Design: The Missing Link
>Great designers have a strong predilection for simplicity.
>Great designers have no fear of complexity.

[Clean Code](http://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882):
>"Software systems are unique compared to physical systems. Their architectures can grow incrementally, *IF* we maintain
>the proper separation of concerns."

If my memory serves me correct, this was written in 1991 in [Crafting a Compiler with C](http://www.amazon.com/Crafting-Compiler-Charles-N-Fischer/dp/0805321667):
>"Indeed, it is becoming increasingly clear, that for modern programs correctness rather than 
>speed is the paramount concern."

C.A.R Hoare:
>There are two ways of constructing a software design: One way is to make it so simple that there are obviously no deficiencies, and the other way is to make it so complicated that there are no obvious deficiencies. The first method is far more difficult.

Niklaus Wirth has said many things :

>Increasingly, people seem to misinterpret complexity as sophistication, which is baffling --- the incomprehensible should cause suspicion rather than admiration. 

>The belief that complex systems require armies of designers and programmers is wrong. A system that is not understood in its entirety, or at least to a significant degree of detail by a single individual, should probably not be built. 

>A primary cause of complexity is that software vendors uncritically adopt almost any feature that users want. 
   

### Tempting the dark side is

Even if you do everything to keep things simple, there are other stakeholders. Here are three
essential lessons how people can create a complex mess inadvertently:

* It is probably best to avoid [architectural astronauts](http://www.joelonsoftware.com/articles/fog0000000018.html). 

* It is good to question oneself occasionally. When in doubt, [remember the gloves](http://thedailywtf.com/Articles/The_Complicator_0x27_s_Gloves.aspx).

* While [Knuth](http://en.wikipedia.org/wiki/Donald_Knuth) is certainly one of the Great Old Ones, even a demigod may make misguided design decisions:
[Knuth versus Unix shell](http://www.leancrew.com/all-this/2011/12/more-shell-less-egg/)

### There is the Light side too

Rich Hickey has been thinking about these issues a lot and given birth to [Clojure](http://clojure.org/) and [Datomic](http://www.datomic.com/).
Here are some of his thoughts related to the topic of this blog post:
[Rich Hickey on simple](http://www.slideshare.net/evandrix/simple-made-easy)

Unix is, despite it's shortcomings, a good example of modularity. Exposing sockets as files,
providing pipes to glue things together etc. provides an extremely powerful platform to build
upon.

At the system integration level, ESB, SOA, REST etc. are all aiming at the same goal. 
Is it better to have twenty software systems integrated together or just one? I will take the former 
structure any day, but some people prefer the latter. For example, our capital is currently planning a purchase of 
[EPIC system](http://thedailywtf.com/Articles/A_Case_of_the_MUMPS.aspx) for medicare. Budgeted at something like 300 million euros, one of the goals is to replace many 
smaller and specific systems with a big monolithic system.
[One Apotti to Rule Them All](http://www.hel.fi/hki/apotti/fi/Apotti-hanke/English)

Good luck with EPIC or any huge (closed source) monolith when the requirements change, as they inevitably will. 
