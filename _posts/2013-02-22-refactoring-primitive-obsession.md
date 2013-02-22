---
layout: post
title: Refactoring Primitive Obsession
author: orfjackal
excerpt: Enriching the domain model by fixing Primitive Obsession code smells requires careful refactoring in small steps. Here I'm presenting some tips for doing that almost fully with automated refactorings, making it much faster and safer to do.
---

[Primitive Obsession](http://www.jamesshore.com/Blog/PrimitiveObsession.html) means using a programming language's generic type instead of an application-specific domain object. Some examples are using an integer for an ID, a string for an address, a list for an address book etc.

You can see an example of refactoring Primitive Obsession in James Shore's [Let's Play TDD](http://www.jamesshore.com/Blog/Lets-Play) episodes 13-18. For a quick overview, you may watch [episode #14](http://www.jamesshore.com/Blog/Lets-Play/Episode-14.html) at 10-12 min and [episode #15](http://www.jamesshore.com/Blog/Lets-Play/Episode-15.html) at 0-3 min, to see him plugging in the TaxRate class.

The sooner the Primitive Obsession is fixed, the easier it is. In the above videos it takes just a couple of minutes to plug in the TaxRate class, but the Dollars class takes over half an hour. James does the code changes manually, without automated refactorings. For a big project with rampant Primitive Obsession it will easily take many hours, even days, to fix the problem of a missing core domain type.

Here I'm presenting some tips of using fully automated refactorings to solve Primitive Obsession. I'm using IntelliJ IDEA's Java refactorings, but the ideas should, to some extent, be applicable also to IDEs with inferior refactoring support.
