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

## Learning and sharing knowledge

This might be little surprising for someones, but reducing bugs or code quality are not the most important reasons to do code reviews. It is sharing the knowledge. Code reviews are meant to share the knowledge about code base and also programming in general.

"Oh, I didn’t know it can also be done this way. I will use it next time!". This is something I've said many times when I've reviewed code.

With code reviews at least two persons know something about the code and it reduces the bus factor.

## Better code quality

> Code review remains the number one thing a company can do to improve code quality. - [State of Software Quality | Code Review 2021, Presented by SmartBear](https://smartbear.com/state-of-software-quality/code-review/)

Code quality is really important thing, and without code reviews, we know it will decrease. My ordered list why code reviews improve code quality:

1. You don't dare to write bad code when you know someone else will review it,
1. The reviewer will notify you if there is a code he/she doesn’t understand, and you will fix it and
1. There will be fewer bugs because some of the bugs will be found and fixed already in code review.

(I personally think that unit tests are number one thing that improves code quality. It was #2 in SmartBear's questionnaire. Not far behind code reviews.)

## Increased collaboration

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

## Make impact and do the code review soon

*Only done work has real value (€$£)*. All cards in agile board that are not yet done don't have any value yet. They will have value when they are done (and deployed to the production).

"In review" is close to be done. It will soon create value, sooner than cards in todo or in progress columns. The more right you go in agile board, the sooner it will have real value. Thus *things on right are more important than things on left*. Help your co’worker to finish his/her task and create value by reviewing the code as soon as possible.

# Shift-left code reviews - how to review sooner?

> I recommend that you do your initial code walkthrough much earlier. Instead of waiting for the completion of a feature, make it a practice to present and discuss each implementation at one-third completion. (Adam Tornhill, Software Design X-Rays)

There is a problem when we review "completed" code. When the code comes to review, it is too late or much more difficult to make significant changes to it. All of us have heard "we are busy, we can fix it later." And by experience we know that "later" comes never.

Example - Urgent and Big Code Review Just Before The Deadline:

- Manager: "This must be accepted/merged in an hour. Our code ships then."
- Reviewer: "This is horrible code; I can’t let it pass the review!"
- Then the manager forces reviewer to accept it and promises that this was the last time reviewer must accept this kind of code.

This shouldn't happen but we know it happens now and then.
It is the situation that Tornhill describes: it is too late to change the code.

## Fix = Review Unfinished Code

What if that code was already reviewed when it wasn't ready yet? If it was reviewed when it was only 70% done? A reviewer could've mentioned about problems earlier and a programmer would've fixed them in time.

My suggestion is to review code before it is 100% ready, and receive feedback earlier. Ie. "shift-left" code review a bit in agile board.

For example with GitHub you can create [draft pull requests](https://github.blog/2019-02-14-introducing-draft-pull-requests/). "Draft" is a good sign for a reviewer not to look at tiny details but to look for a big picture. And when you publish the code review (ie. remove "draft" from it), it requires also less time to review because review has already reviewed most of it.

# Tips

TODO
