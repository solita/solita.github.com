---
layout: post
title: When to Refactor
author: orfjackal
excerpt: TODO
---

Refactoring is the process of improving code's design without affecting its functionality. Is it possible to over-refactor? I don't think that code can ever be "too clean" and following the [four elements of Simple Design](http://www.jbrains.ca/permalink/the-four-elements-of-simple-design) should not result in over-engineering, but certainly we can agree that some code needs more cleaning up than others and we rarely have enough time to do all we want. Prioritization is needed.

When I do refactoring, it's usually in one of the following situations.


## After getting a test to pass

At unit scale TDD (as opposed to [system scale TDD](http://www.natpryce.com/articles/000780.html)), writing a test and making it pass takes only a few minutes (or you're working in too big steps). After getting a test pass, it's good to take a moment to look at the code we just wrote and clean it up. Basically it comes down to removing duplication and improving names, i.e. Simple Design. This takes just a minute or two.

This is also a good time to fix any obvious design smells while they are still small. For example [Primitive Obsession](http://dev.solita.fi/2013/03/01/refactoring-primitive-obsession.html) gets the harder to fix the more widespread it is. This usually takes just a couple of minutes and at most an hour. Very faint design smells I would leave lying around until they ripen enough for me to know how to fix them - but not too long, so that they begin to rotten.


## Before or during implementing a new feature

If the system's design does not make it easy to add the feature I'm currently working on, I would first refactor the system into a direction where adding that feature will be easier. If this is the second or third instance* of a similar feature <a name="note-1-ref"></a>[[1]](#note-1), I would refactor the code to follow the [Open-Closed Principle](http://blog.8thlight.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html), so that in the future adding similar features will be trivial. This kind of refactoring might take from half an hour up to a couple of hours.

TODO: "during" implementing a feature


## When our understanding of what would be the correct design improves

When we start developing a program, we have only partial understanding of the problem being being solved, but we'll do our best to make the code reflect our current understanding of the problem. As the development progresses over months and years, we will learn more and invevitably there will be parts of the code that we would have designed differently if we had then known what we know today. This is the [original definition](https://www.youtube.com/watch?v=pqeJFYwnkjE) of the Technical Debt metaphor.

For big changes it's not practical to block new features for the duration of the refactoring, so working towards the new design should be done [incrementally at the same time as developing new features](http://continuousdelivery.com/2011/05/make-large-scale-changes-incrementally-with-branch-by-abstraction/). Whenever any of the developers touches a class that does not yet conform to the target design, he should refactor it there and then, before implementing the feature he is working on. This kind of refactoring might take many weeks or months to completion, but it is done incrementally in small steps, maybe at most a couple of hours at a time, so that the software keeps working at all times.


## When trying to understand what some piece of code does

TODO

https://groups.google.com/d/msg/software_craftsmanship/w–3hS1dwcA/lLXRIlfIC5kJ
http://www.jbrains.ca/permalink/does-unit-testing-add-value-when-were-not-doing-tdd


<hr>

### Notes

<a name="note-1"></a>[[1]](#note-1-ref): If the shape of the code is developing into a direction that you've seen happen many times in the past, it's easy to know how to refactor it already when the second duplicate instance raises its head. But if you're uncertain that what the code should be like, it may be worthwhile to leave the second duplicate be and wait for the third duplicate, so that you can clearly see which parts are duplicated and which vary before creating a generic solution.
