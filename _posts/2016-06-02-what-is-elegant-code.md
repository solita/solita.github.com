---
layout: post
author: pkalliok
title: >
  What is elegant code, actually?
excerpt: >
  However, I claim that code elegance is not _just_ a question of
  personal preference.  There is a least common denominator for code
  elegance that does not depend on who is reading the code.  I'm talking
  about things that make code easier to produce, read, understand and
  maintain _irrespectible_ of the programming culture.
tags:
- brevity
- simplicity
- complexity
- maintainability
- productivity
- Python
- Lisp
---

Many of my fellow coders, both colleagues and friends, have recently discussed a lot the writing of elegant code and how important it is that your code is elegant.  Of course, this is a very welcome development of attitudes.  However, it still bugs me sometimes: what do all these people _mean_ by elegant code?

The dictionary definition of "elegant" tells us that elegant is basically the same as beautiful or tasteful, with an overtone of some kind of extra effort, or refinement, put into the outcome.  The important message here is, of course, that it is not enough for code to just _work_, that is, execute correctly.  Extra effort has to be put into making the code beautiful.  But isn't beauty in the eye of the beholder?  Is elegance just one more flamebait topic for the religious battles of programmers?

The problem is a little bit similar to the definition of "good manners".  People who were brought up in one culture (say, the Brasilian high class) may not be conscious that what they have learned as "good manners" are not universally accepted as such.  Likewise, people who learned their programming skills in one programming culture (say, the Lisp culture) may not see that their elegant code might be seen as cumbersome, impractical, incomprehensible or downright ugly by people who never learned the values of the Lisp culture.  A coder who has a multicultural background will naturally adjust their coding style to what will likely be accepted by those who will read their code.

However, I claim that code elegance is not _just_ a question of personal preference.  Good manners also include something else than just arbitrary rules that live in various cultures.  There are many ways of social conduct that are universally good: be interested and enthusiastic, talk with people, listen and understand, don't judge, and tell others you like them.  Not surprisingly, there is also a least common denominator for code elegance that does not depend on who is reading the code.  I'm talking about things that make code easier to produce, read, understand and maintain _irrespectible_ of the programming culture.

It is not to say that one should disregard cultural elegance preferences altogether, quite on the contrary: you must be aware which ways of writing code are idiomatic in your particular choice of technologies (languages, libraries, frameworks and toolchains).  But universally elegant code makes your programs better in every culture, so its principles are really important to understand.

Now, lest my definition of "elegant" be just another opinion in the air, I'll try to back this definition with at least some data (or actual research) about the effect of these code metrics on programmer productivity and code maintainability.

Here are my metrics for universal code elegance.  Remember, you cannot write elegant code by disregarding cultural elegance (say, naming conventions) altogether!  There has to be a balance.

1. Brevity, or concision.  This metric means that the code is short.  Brevity can be measured as the number of characters, tokens, or keystrokes it takes to create some particular functionality.
2. Simplicity.  This metric means that the structure of the code is "straightforward".  It has many measures such as the average length of a single definition (e.g. function, macro, or method), [cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity) per statement, [Halstead complexity measures](https://en.wikipedia.org/wiki/Halstead_complexity_measures), amount of code in cyclically dependent code units (code that stops working correctly if you take any part of it away), and graph density of almost any graph that visualises the codebase.

Code brevity is a fundamental factor in programmer productivity.  It is no coincidence that a good code refactoring practically always produces code that is shorter that what we started with.  Proponents of functional programming languages have studied programmer productivity in different languages and concluded that the same amount of code takes approximately the same time to produce, regardless of the expressivity of the language used, and also regardless of how much functionality the code has.  [This study](http://page.mi.fu-berlin.de/~prechelt/Biblio/jccpprtTR.pdf) shows that even within one language, program length correlates well with the time that it takes to produce it.

Oooh, so short code is quick to write, you say, but what about maintainability?  Well, brevity is directly related to many of Halstead measures; especially _volume_, which has been shown to correlate to number of bugs delivered and also the time it takes to read (and understand) a given piece of code.  Programmer performance also has been shown to degrade quickly when they have to jump around in the code to be able to understand it; in practice this means (weird as it may sound) that the more code you can cram on one screen, the easier it will be to read.  Of course as long as we don't override cultural values, such as proper code formatting practices.

Code brevity has a natural bound: when a given piece of code has been so factored that it basically has no duplication, there is no way to make the code shorter, than to come up with a more concise way to describe the problem.  Thus brevity is related to DRY (don't repeat yourself): it leads to code where a single change doesn't need to be implemented in many places.

Simplicity, or complexity, has been studied extensively.  Most of these studies are efforts to prove the feasibility of a given complexity metric.  They show that some given definition of complexity correlates with something undesirable (such as time it takes to update a piece of code, or likelihood that the code has bugs).  Complexity metrics can be used as hints to find code that needs refactoring, but they can also be used to assess the maintainability of some codebase as a whole.

Some studies that discuss well known complexity metrics are:

 * [Cyclomatic complexity density and software maintenance productivity](http://dx.doi.org/10.1109/32.106988)
 * [A quantitative evaluation of maintainability enhancement by refactoring](http://dx.doi.org/10.1109/ICSM.2002.1167822) studies effect of reduced coupling (interaction graph density)
 * [Measurements of software maintainability](http://www.artes.uu.se/events/gsconf02/papers/Land_Maintainability.pdf) has many more pointers
 * [Do Programming Languages Affect Productivity? A Case Study Using Data from Open Source Projects](http://dx.doi.org/10.1109/FLOSS.2007.5)

Some aspects of simplicity seem to be more tightly associated with actual productivity, readability and ease of maintenance than others.  Still, individual case studies cannot actually measure the "maintainability" of a given codebase because there are also so many culturally dependent factors involved.

But what does this all mean in practice, from the point of view of a programmer?  It means that we all should strive for code that is not repetitive, uses a small vocabulary, and is written in units that only depend in one direction.  Also, if we have two ways to write the same program, the shorter one is the more elegant one, as long as they take cultural values equally well into account.

