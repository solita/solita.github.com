---
layout: post
title: When to Refactor
author: orfjackal
excerpt: How to maintain the balance between adding new features and refactoring existing code? Here are some rules of thumb for choosing when to refactor and how much.
---

Refactoring is the process of improving the code's design without affecting its functionality. Is it possible to over-refactor? I don't think that code can ever be "too clean", and following the [four elements of Simple Design](http://www.jbrains.ca/permalink/the-four-elements-of-simple-design) should not result in over-engineering. But certainly there is code that needs more cleaning up than other cases, and we rarely have enough time to do all we want. That's why prioritization is needed.

When I refactor, it's usually in one of the following situations.


## After getting a test to pass

At unit scale TDD (as opposed to [system scale TDD](http://www.natpryce.com/articles/000780.html)), writing a test and making it pass takes only a few minutes (or you're working in too big steps). After getting a test to pass, it's good to take a moment to look at the code we just wrote and clean it up. Basically it comes down to removing duplication and improving names, i.e. Simple Design. This takes just a minute or two.

This is also a good time to fix any obvious design smells while they are still small. For example [Primitive Obsession](http://dev.solita.fi/2013/03/01/refactoring-primitive-obsession.html) gets the harder to fix the more widespread it is. This usually takes just a few minutes and at most an hour. Very faint design smells I would leave lying around until they *ripen* enough for me to know how to fix them - but not too long, so that they begin to rot.


## When adding a feature is hard

If the system's design does not make it easy to add a feature I'm currently working on, I would first refactor the system to make adding that feature easier. If this is the second or third instance of a similar feature <a name="note-1-ref"></a>[[1]](#note-1), I would refactor the code to follow the [Open-Closed Principle](http://blog.8thlight.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html), so that in the future adding similar features will be trivial. This might take from half an hour up to a couple of hours.

When the difficulty of adding a feature hits you right away like a ton of bricks, then it's obvious to do the refactoring first. But what if a difficulty sneaks up on you *during* implementing the feature? Trying to refactor and implement features at the same time is a road to [pain and suffering](http://c2.com/cgi/wiki?RefactoringHell). Instead, retreat to the last time that all tests passed (either revert/stash your changes or disable the new feature's one failing test), after which you can better focus on keeping the tests green while refactoring.


## When our understanding of what would be the correct design improves

When we start developing a program, we have only partial understanding of the problem being solved, but we'll do our best to make the code reflect our current understanding of the problem. As the program grows over months and years, we will learn more and inevitably there will be parts of the code that we would have designed differently, if we only had then known what we know today. This is the [original definition](https://www.youtube.com/watch?v=pqeJFYwnkjE) of the Technical Debt metaphor and the ability to pay back the debt depends on how clean the code is.

For big refactorings, it is unpractical to block adding new features while the design is being changed. So working towards a new design should be done [incrementally at the same time as developing new features](http://continuousdelivery.com/2011/05/make-large-scale-changes-incrementally-with-branch-by-abstraction/). Whenever a developer touches a class that does not yet conform to the target design, they should refactor it there and then, before implementing the feature at hand. This kind of refactoring might take many weeks or months to completion, but it is done incrementally in small steps, maybe at most a couple of hours at a time, so that the software keeps working at all times.


## When trying to understand what some piece of code does

If you need to understand some code, even if you're not going to change it, refactoring the code is one means for understanding it better. Extract methods and variables, give them better names and move things around until the code says clearly what it does. You may combine this with writing unit tests, [which likewise helps to understand the code](http://www.jbrains.ca/permalink/does-unit-testing-add-value-when-were-not-doing-tdd).

If the code has good test coverage, you might as well commit the changes you just did, in hopes of the next reader understanding the code faster <a name="note-2-ref"></a>[[2]](#note-2). But even if the code has no tests, you can do some refactoring to understand it and then throw away your changes - your understanding will remain. If you know that you're going to throw away your changes, you can even do the throwaway refactoring faster with less care. And for complex refactorings, when you're not sure about what sequence of steps would bring you safely to your goal, prodding around the code can help you to get a feel for the correct refactoring sequence.


<hr>

### Notes

<a name="note-1"></a>[[1]](#note-1-ref): If the shape of the code is developing into a direction that you've seen happen many times in the past, it's easy to know how to refactor it already when the second duplicate instance raises its head. But if you're uncertain of what the code should be like, it may be worthwhile to leave the second duplicate be and wait for the third duplicate before creating a generic solution, so that you can clearly see which parts are duplicated and which vary.

<a name="note-2"></a>[[2]](#note-2-ref): Sometimes I wonder whether a refactoring made the code better, or I just understand it better because of spending time refactoring it.

![Not sure if refactoring made code more understandable, or I just understand the code better because I spent hours in it.](/img/when-to-refactor/not-sure-if-refactoring.jpg)
