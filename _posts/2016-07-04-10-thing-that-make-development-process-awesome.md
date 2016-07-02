---
layout: post
title: 10 Things That Make Development Process Awesome
author: jarzka
excerpt: What takes software dewvelopment from being merely enjoyable to awesome?
tags:
- software development processes
- testing
- culture
---

Software development is enjoyable, but there are many little things that can make the difference between it being enjoyable and awesome. Many of these are related to the working methods used in the project. At Solita, project teams are relatively free to make their own choices regarding software development methods they use. In this article, I want to share some of the methods we have used in [Harja](https://github.com/finnishtransportagency/harja) project. Some of these might seem obvious, but having been in software projects were none of these things were applied I can appreciate their presence. So here goes!

## 1. Build statuses available

As a member of a software development team I want to make sure that changes I make into the codebase are buildable - at least in the main branch that all other developers use. Tracking build statuses is thus important and they should be visible to concerned developers. We keep a TV screen at our office near the development team showing not only the current built statuses, but also sprint progress and the number of found bugs. Some of us have also installed a [Mac app](http://ccmenu.org/) that shows build statuses in the menu bar.

Tracking nightly and production builds is nice but would it be cool to also track feature branches too? Since Harja is an open source project hosted on GitHub we are able to use [Travis CI](https://travis-ci.org/). Travis helps us to monitor the current build status for all pull requests. This way we can see if the stuff we are about to merge into our main branch is compilable and has passed all tests. Awesome!

## 2. Well defined task handling

Like in many software projects, [Jira](https://www.atlassian.com/software/jira) has been our platform of choice for handling user stories and managing sprint progress. While it's not perfect (one still cannot add a task to the current sprint from the task's own page?) it has made the development process easy to track. The ease, however, requires that everyone understands what a certain process column means and what people are expected to do in different situations. To ensure that we spent some time defining our own process columns:

1. **In definition**. The task needs to be defined and described in a way that allows anyone in the team to start implementing it.
2. **Ready for implementation**. Anyone can take the task and start working with it.
3. **In progress**. The assigned person is actively working with the task. There can be no unassigned tasks in this column.
4. **In testing**. Anyone can pick an unassigned task and start testing it. If the task is assigned to someone, it means that the person is either testing it or fixing found problems.
5. **In code review**. Anyone can pick the task and review the code (usually the code is reviewed by the person testing it)
6. **Done**. The task is tested, reviewed and merged. In other words: it's done.

We also take a look at the board in daily scrum meetings and check if some tasks are in wrong columns or being blocked. For example, if there are many unassigned tasks in the testing column, they are discussed and assigned to a willing person.

## 3. Resolving problems by using database dumps

Sometimes we have faced problems that only occur in our piloting server. We can still view logging data and errors that might have caused the problem, but the tools for finding the reasons for these problems are much better on our development machines (breakpoints, debug logs etc.). To make it easier to resolve these kind of issues we have built a script which downloads the whole database dump from the piloting server and mounts it into our own local development machine.

Not only does this method make it possible to use the piloting server's data in our local environment to debug it, but it is also helpful when implementing new features. The amount of our own testing data is relatively small, and does not necessarily contain all the possible cases that can be found from the piloting server's data, so it is valuable to test new features with real piloting data.  

## 4. Tools that we love

The difference between using software development tools already provided by the project or company and tools that you prefer to use the way you want can make a big difference in enjoyability of work; working with tools that you find logical or useful makes writing code much more efficient. Naturally, some projects may require certain tools to be used but generally people at Solita are free to use the software development tools of their choice.

## 5. Everything is tested by a fellow developer

Excepting the correction of spelling errors, every change in our codebase is tested by a fellow developer. When a new feature is implemented or a bug is fixed, it is deployed into a testing server, which is largely equivalent to our piloting server. In addition to deploying a task to the testing server, we create a pull request, move the task into the testing column and write a short introduction on what is implemented or fixed and how it should be tested. This allows anyone in our team to quickly pick a testable task and test it. This makes testing easier and more time-efficient, since there is no need to locally checkout the feature branch and wait for it to be built.

## 6. Testing day

While I am a big fan of automated unit tests I also believe that not everything can be tested automatically - or at least it would require an unreasonable amount of time and effort. This is why we still need manual testing, but unfortunately it has sometimes proved difficult in our project. It's not that we don't test all new features we implement, but in addition to that we have wanted to allocate time for separate testing sessions, during which every project member spends some time testing complete user workflows (alone or in pairs). This did not work well, however, as the pre-allocated time slot was skipped many times simply because people did not have time to participate. Furthermore, some of us also felt not being productive enough by simply testing the system. Changing the pre-allocated time slot multiple times did not seem to solve the problem so we decided to allocate a whole day for the testing session.

Wait, a whole day? Doesn't this just mean even more time "wasted" in testing? This time, the testing day was allocated well in advance and the day was spent completely out of office in a quiet place - no meetings, no context switching, just focusing on testing the system. The testing day turned out to be a success. Everyone felt the day was valuable and we were able to find many potential problems.

## 7. Quick usability tests

Usability testing sessions are sometimes criticized for being expensive. But useful usability tests do not always require a dozen users and a [fully featured usability testing laboratory](http://www.interface-analysis.website/images/AV_room.jpg). Simple and low-cost usability tests can simply mean asking a fellow developer to spend a few minutes testing when a new feature is being implemented. Is he able to complete a simple user task without comprehensive introductions? Does the user interface behave as he expects?

This method can be used to quickly spot potential problems that can be fixed while the feature is still being implemented and changes are easy to make. Sure, the fellow developer's view is probably not the same as end-users', but I bet that using this method we have already fixed potential problems that end-users would have spotted in any case.

## 8. Open bug list

In our project the current up-to-date bug list is open to our development team and our customer. Every morning after the regular Scrum meeting we open the bug list, view the latest bugs, prioritize them and quickly discuss potential fixes. Usually we also check if the oldest bugs are still relevant. Many times we have closed old issues that have already been fixed during other tasks. By doing this we have been able to keep the bug list fresh and make sure that everyone has an understanding of the current bug situation. Furthermore, we also encourage people putting potential bugs in the bug list rather than just ignoring them completely.

## 9. No code ownership

In big systems like Harja there are usually multiple different places that require a special domain knowledge to work with. This can lead into a situation where a single developer becomes responsible of certain parts the system. This is not in itself a bad thing, but can lead to problems if other developers cannot easily enter and make changes to these parts of the system. We believe that there should not be hard set rules on who is responsible of different parts of the codebase. This encourages developers to learn new things and lowers the barriers to freely explore the system.

## 10 Weekly code review sessions

Since our project is relatively big, it has become clear that none of the six developers have a complete low-level understanding of the whole system. Furthermore, code intended for re-use might not always be easy to find. To fix this problem, we aim to have a code reviewing session every Friday. In this session, which usually takes 1 to 2 hours, everyone is expected to introduce changes he has made in the codebase during the current week. This, in addition to regular daily Scrum meetings, helps to share knowledge on what others have been doing and what changes has been made. And of course, who does not enjoy sharing discussion on all things coding with one's beloved teammates.

## Conclusion

Not all of the introduced methods were in use when I entered the project. In fact, many of these are the result of retrospectives we keep after each Scrum sprint. We have made many experiments to improve these methods and tried to experiment new ones. The result is the current list, and also a lot of failed experiments that lasted only a couple of weeks.  

I am not saying that all of the introduced methods work in every project - that's one reason why projects are free to define their working methods. But what is important is to recognize the working methods used in the project and try to re-think them. Are all of them giving value, could some of them be improved or could we try something completely new? Changes should be made in small parts and working changes should be taken as a part of the development process after a successful experiment.
