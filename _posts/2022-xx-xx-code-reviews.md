---
layout: post
title: Code Reviews
author: lassiautio
excerpt: >
  TODO
tags:
 - code review
---

Code reviews are something we all have been involved, and what we do continuously in our projects. We might have contradictory feelings about them. Often they feel like just bureaucracy that is required by a manager. Sometimes we want someone to give us feedback on our code. When we see poor code, we might think that we should've reviewed the code better. In this blog post I will explain why code reviews are important, even more important than programming itself. I will also give motivation to do code reviews now, not after few days. Some practical tips will be also given to make reviewing easier.

# Reasons to do code reviews

**Learning and sharing knowledge**

This might be little surprising for someones, but reducing bugs or code quality are not the most important reasons to do code reviews. It is sharing the knowledge. Code reviews are meant to share the knowledge about code base and also programming in general.

"Oh, I didn’t know it can also be done this way. I will use it next time!". This is something I've said many times when I've reviewed code.

With code reviews at least two persons know something about the code and it reduces the bus factor.

**Better code quality**

> Code review remains the number one thing a company can do to improve code quality. - [State of Software Quality | Code Review 2021, Presented by SmartBear](https://smartbear.com/state-of-software-quality/code-review/)

Code quality is really important thing, and without code reviews, we know it will decrease. My ordered list why code reviews improve code quality:

1. You don't dare to write bad code when you know someone else will review it,
1. The reviewer will notify you if there is a code he/she doesn’t understand, and you will fix it and
1. There will be fewer bugs because some of the bugs will be found and fixed already in code review.

(I personally think that unit tests are number one thing that improves code quality. It was #2 in SmartBear's questionnaire. Not far behind code reviews.)

**Increased collaboration**

Code reviews force us to communicate with others about the code. Common problem is how to ask for a feedback. Reviews give us a nice organized way to get and give feedback and communicate.

# Code reviews are more important than programming itself

"I am busy with my new feature." Classic reason to postpone code review, sometimes with many days! But, truth is that code reviews are more important than your current feature that you are programming. I will show why.

Below is a simple agile board. Which feature has the highest value?

![Simple agile board](/img/code-reviews/simple-agile-board.png)

Drum rolls... Feature C!

**Feature C has highest value because it is done**. It is a feature that users can use. Feature B might be important, but before it is done, it has no value. Feature A is just an idea so far, and doesn't have any value yet.

Now lets add an in review column to our agile board, and feature D to it. Which feature has the highest value after C?

![Agile board with in review column](/img/code-reviews/in-review-agile-board.png)

Drum rolls... Feature D!

Why? How about feature B that I'm now programming? It is a super important feature. I will review D after I've done B.

Reason is simple: the feature D is **closest to be done** and thus has highest value after feature C.

**Make impact and do the code review soon.**

Only done work has real value (€$£). All cards in agile board that are not yet done don't have any value yet. They will have value when they are done (and deployed to the production).

"In review" is close to be done. It will soon create value, sooner than cards in todo or in progress columns. The more right you go in agile board, the sooner it will have real value. Thus things on right are more important than things on left. Help your co’worker to finish his/her task and create value by reviewing the code as soon as possible.

# Shift-left code reviews

TODO

# Tips

TODO
