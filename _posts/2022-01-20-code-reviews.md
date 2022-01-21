---
layout: post
title: Code reviews are more important than programming - and other tips and motivations for code reviews
author: lassiautio
excerpt: >
  Why should we do code reviews? What makes code reviews even more important than programming? Why and how to shift-left code reviews?
  This blog post will give answers to these questions and go deeper into the world of code reviews.
  In the end, there will be also some tips on why code reviews should be small, and why you shouldn't comment too much on code reviews.
tags:
 - code review
---

Code reviews are something we all have been involved in, and what we do continuously in our projects. We might have mixed feelings about them. Often they feel like just bureaucracy that is required by a manager. Sometimes we want someone to give us feedback on our code. When we see poor code, we might think that we should've reviewed the code better.

In this blog post, I will explain why code reviews are important, even more important than programming itself. I will also give the motivation to do code reviews now, not after a few days. Some practical tips will be also given to make reviewing easier.

This is a blog post version from my presentation that I had at [DevDay 2021](https://dev.solita.fi/2021/12/13/devday-of-solita.html).

# Reasons to do code reviews

## Learning and sharing knowledge

This might be a little surprising for someone, but code quality or reducing bugs are not the most important reasons to do code reviews. It is sharing the knowledge. Code reviews are meant to share knowledge about the code base and also programming in general.

"Oh, I didn't know it can also be done this way. I will use it next time!" This is something I've thought many times when I've reviewed code.

With code reviews, at least two persons know something about the code and it reduces the bus factor.

## Better code quality

> Code review remains the number one thing a company can do to improve code quality. - [State of Software Quality, Code Review 2021, Presented by SmartBear](https://smartbear.com/state-of-software-quality/code-review/)

Code quality is a really important thing, and without code reviews, we know it will decrease. My ordered list of why code reviews improve code quality:

1. You don't dare to write bad code when you know someone else will review it,
1. The reviewer will notify you if there is a code he/she doesn't understand, and you will fix it and
1. There will be fewer bugs because some of the bugs will be found and fixed already in code review.

(I think that unit tests are the number one thing that improves code quality. It was #2 in SmartBear's questionnaire. Not far behind code reviews.)

## Increased collaboration

Code reviews force us to communicate with others about the code. A common problem is how to ask for feedback. Reviews give us a nice organized way to get and give feedback and communicate.

# Code reviews are more important than programming itself

"I am busy with my new feature." Classic reason to postpone code review, sometimes with many days! But, truth is that code reviews are more important than your current feature that you are programming. I will show why.

Below is a simple agile board. Which feature has the highest value?

![Simple agile board](/img/code-reviews/simple-agile-board.png)

Drum rolls... Feature C!

**Feature C has the highest value because it is done**. It is a feature that users can use. Feature B might be important, but before it is done, it has no value. Feature A is just an idea so far and doesn't have any value yet.

Now let's add an in-review column to our agile board and feature D to it. Which feature has the highest value after C?

![Agile board with in review column](/img/code-reviews/in-review-agile-board.png)

Drum rolls... Feature D!

Why? How about feature B which I'm now programming? It is a super important feature. I will review D after I've done B.

The reason is simple: feature D is **closest to be done** and thus has the highest value after feature C.

## Make an impact and do the code review soon

*Only done work has real value (€$£)*. All cards in an agile board that are not yet done, don't have any value yet. They will have value when they are done (and deployed to the production).

In-review is close to being done. It will create value sooner than cards in todo or in-progress columns. The more right you go in an agile board, the sooner it will have real value. Thus *things on right are more important than things on left*. Help your co-worker to finish his/her task and create value by reviewing the code as soon as possible.

# Shift-left code reviews - how to review sooner?

> I recommend that you do your initial code walkthrough much earlier. Instead of waiting for the completion of a feature, make it a practice to present and discuss each implementation at one-third completion. (Adam Tornhill, in his book [Software Design X-Rays](https://pragprog.com/titles/atevol/software-design-x-rays/))

There is a problem when we review the "completed" code. When the code comes to review, it is too late or much more difficult to make significant changes to it. All of us have heard "we are busy, we can fix it later." And by experience, we know that "later" never comes.

Example - Urgent and Big Code Review Just Before The Deadline:

- Manager: "This must be accepted/merged in an hour. Our code ships then."
- Reviewer: "This is horrible code; I can't let it pass the review!"
- Then the manager forces reviewer to accept it and promises that this was the last time reviewer must accept this kind of code.

This shouldn't happen but we know it happens now and then.
It is the situation that Tornhill described: it is too late to change the code.

## Fix = Review unfinished code

What if that code was already reviewed when it wasn't ready yet? If it was reviewed when it was only 70% done? A reviewer could've mentioned about problems earlier and a programmer would've fixed them in time.

My suggestion is to review the code before it is 100% ready and receive feedback earlier. Ie. "shift-left" code review a bit in an agile board.

For example, with GitHub, you can create [draft pull requests](https://github.blog/2019-02-14-introducing-draft-pull-requests/). "Draft" is a good sign for a reviewer not to look at tiny details but to look for a big picture. And when you publish the code review (ie. remove "draft" from it), it requires also less time to review because the reviewer has already reviewed most of it.

# Tips for authors

## Keep it short

How many of us have faced this?

![10 lines of code = 10 issues. 500 lines of code = "looks fine."](/img/code-reviews/10-lines-vs-500-lines-code-review.png)

Reasons why long code reviews are bad:
1. They are difficult to understand,
1. The reviewer doesn't really do the code review.

When the code review is longer, the reviewer will find fewer errors.
Think also about the reviewer and make it easier to review by keeping it short. He/she will make you a service by reading your code and giving feedback. Rarely reviewers are happy when they are requested to review a code. Make his/her job easier. You will also receive better feedback.

Split the task if it grows too large to have shorter code reviews.

Lassi's rule of thumb: max 10 files per code review.

## Pre-review your code

My simple advice is to review your code before pushing it to code review.
I always find something to fix when I pre-review my code.

This also saves time from the reviewer, and he/she can find something new to improve: not those obvious ones you fixed in this phase.

# Tips for reviewers

## Do the review on breaks

* "I don't have time to review."
* "I am in the flow now and don't want to break it."
 
 These are common problems, or excuses, with code reviews. But that is not true. We have many natural breaks during the day when we could review a code. Review at those times and you don't have to break your flow.

* Very first in the morning,
* When you have finished another task before switching to a new task,
* After meeting, lunch or coffee break before starting or continuing another task or
* As the last task before leaving.

Also, remember the importance of the code review. It is more important than programming itself. Thus it should have high priority. I don't say you have to stop your coding immediately when there is a code review waiting for you. But to not postpone review many hours, and do it within few hours from the request.

As I said earlier, help your co-worker to finish his/her task and create value by reviewing the code as soon as possible. When you request someone to review the code, you want it to be reviewed soon. So, do to others what you want them to do to you.

## What should I review?

A common problem for new developers or if you are not familiar with the codebase. My tip is to **review what is important for you**. That is something you are good at, and you can teach it to others.

"I am not an expert on this, how can I review it?"
If you don't understand it, then learn at least something from it. Or ask stupid questions from the author.

Keep an eye on the things that static code analyzers can't do. One of the best is namings. Namings are important, but static code analyzers don't know if some variable name is good or not. Design and architecture are also something human is better to analyze than static code analyzers.

![Code review: hierarchy of needs](/img/code-reviews/hierachy-of-needs.png)

Image: http://blakesmith.me/2015/02/09/code-review-essentials-for-software-teams.html

## Don't comment too much

This tip is especially for me.
When you comment much, there is a risk that most of the comments will be ignored.
If you write only a few comments, those comments are more powerful, because they will be certainly read.

Lassi's rule of thumb: write max 10 comments per code review.

"What if there are more than 10 issues?" – comment 10 most critical ones.
Short code reviews help with this, so again, keep them short.

Notice: if there are more than 10 bugs, then you should comment on all of those (or even have a meeting).

# Conclusion

Hopefully, I've told clearly the importance of code reviews, and after reading this you value them more. If I had to take the three most important things from this blog post, those would be:

* Code reviews are more important than programming itself,
* Keep it short (Lassi's rule of thumb: max 10 files) and
* Don't comment too much (Lassi's rule of thumb: max 10 comments).