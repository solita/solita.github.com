---
layout: post
title: A case for formal computer science
author: lokori
excerpt: To write great programs, one needs to know the theory of programming. Hacking is the fun part, but mastery requires more.
tags: 
- NP
- Turing
- Graph
- Algorithm
- Computer science
---

### Practical programming over theory of programming? ###

Universities provide courses on algorithms, data structures, different kinds of formal methods, 
graph algorithms and theory of computation. The curriculum is pretty much the same everywhere
and yet in everyday work one is rarely required to implement a [red-black tree](http://en.wikipedia.org/wiki/Red%E2%80%93black_tree) or provide formal proof that [merge sort](http://en.wikipedia.org/wiki/Merge_sort) performs in O(n lg n) time.

Students wonder why study these things at all, since their future employers will have
zero interest in them. Knowledge of node.js and Java will get you hired, while knowledge of
the [Turing Machine](http://en.wikipedia.org/wiki/Turing_machine) will not. Knowledge, understanding and new discoveries are the goals 
of universities, but I will provide some practical arguments and reasons here.

### Why it matters ###

1. 
Serious study of this dry and heavyweight stuff will develop your analytical skills. If you
want to be good at analyzing and solving logical problems, there is no shortcut. Flipping 
through a proof is not the same as actually understanding it.

2. 
You will learn the vocabulary and background necessary for writing and reading formal 
specifications. Mathematical notations are very powerful, exact and global. While english
may be global nowadays, it's neither accurate nor compact. 

3. 
These things cannot be picked up "on demand". Some people will find it easier, but understanding 
[what P=NP means and why it matters](http://en.wikipedia.org/wiki/P_versus_NP_problem) will take time even for very smart people.

4. 
These things do not change or become obsolete very often. Languages and frameworks come and go, 
but the [Church-Turing thesis](http://en.wikipedia.org/wiki/Church%E2%80%93Turing_thesis) and [the halting problem](http://en.wikipedia.org/wiki/Halting_problem) have been around for decades. These are, in a 
sense, core knowledge for a serious programmer and will remain with you (and your CV) for the 
rest of your career.

5. 
The more you know about the theoretical side of things, the easier it gets to find a correct solution and
to exclude implausible solutions. How much better is it to recognize that the customer's problem
is NP-hard than to try a brute force attack on it? Infinitely.

6. 
In a similar fashion, this thread [about regex matching](http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags) is both funny and sad. What good is that Perl regex magic if you do not know [what regular languages are and how they are limited](http://en.wikipedia.org/wiki/Chomsky_hierarchy)? Not much. 

7. 
If you have implemented a compiler for a serious language, picking up today's 
hot language becomes a non-issue. (Learning a new programming paradigm may still be an issue).

8. 
You actually need this stuff per se. I'm working on a large enterprisey Java project at the moment. 
We have encountered problems which are naturally solved with [graph algorithms](http://www.cs.berkeley.edu/~kamil/teaching/sp03/041403.pdf) 
like depth-first search, breadth-first search, topological distance and cycle detection. 
Graph algorithms are in fact very handy solutions for a wide variety of real world problems. They are 
not particularly difficult to understand or implement, but you have to know about them.

### A short test ###

Your customer wants a solution to this problem. They have thousands of vehicles, pickup locations and warehouses.

> A number of goods need to be moved from certain pickup locations to their delivery locations. The goal is to find optimal routes for a fleet of vehicles to visit the pickup and drop-off locations.

Is it immediately obvious to you how to approach this problem? Can you explain your approach to the customer who knows nothing about programming or NP?


### Aiming for a career as a programmer? ###

Assuming you have not graduated yet, this is a good day to reconsider which courses to take. There are three
reasons to start today:

1. 
You will never have the time to study these subjects after you graduate and work full-time in the private sector. Ask anyone.
It is difficult and time consuming and your employer or customers won't pay for it.

2. 
Since this stuff never goes out of fashion, you get the most benefit by learning it now.

3. 
If you want to have a serious career as a *programmer*, sooner or later you will run into these things. 
Want to work with great programmers -- perhaps even in a technical lead role -- but not willing to study 
the theoretical aspects of programming? Forget it, [Yegge will not be amused](http://steve-yegge.blogspot.fi/2008/03/get-that-job-at-google.html).

#### Do or do not -- there is no try ####

To put it bluntly, either you do it or you never become a [Great Programmer](http://www.drdobbs.com/architecture-and-design/what-makes-great-programmers-different/240001472). Your choice. There are many positions and projects where writing the code is not in the center. Not everyone wants to have a "career" anyway, which is also fine.

Theory is not enough. Here's [some practical advice on the matter](http://norvig.com/21-days.html).

### Jobs for passionate programmers ###

As an added bonus, you can mention that [compiler crafting course](http://www.cs.tut.fi/kurssit/OHJ-4500/) in your CV. Maybe Foobar Ltd. considers it ridiculous to mention a course assignment, but that's OK. You should apply for a job here and forget about that other company. We will take you seriously. We deliver elegant solutions to difficult problems and to do that we need people who

<ol style="list-style: lower-alpha;">
 <li> want to learn as much as possible about programming</li>
 <li>have a deep insight into the field beoynd today's buzzwords</li>
 <li>want to write great code and can actually deliver solutions to difficult problems</li>
 <li>will listen to customers' and users' needs and solve the trivial parts too</li>
 <li>aim to improve the standard of work and customer satisfaction</li>
</ol>

The "useless" theoretical stuff and that compiler course neatly demonstrate points a,b and c. 
I intentionally mentioned points d and e because we get paid for results. Great code has value 
only if it helps our customers.

