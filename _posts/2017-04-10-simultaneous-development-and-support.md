---
layout: post
title: Simultaneous Development and Support
author: jarnovayrynen
excerpt: How our team improved simultaneous new development and end user support
tags:
- software development process
- iterative development
- support
---

After a major production release a software team may become overwhelmed with customer feedback. Investigating defect reports, communication with end users and related bug fixing may hinder development of new features for a long time if not handled properly. This article presents how we tackled this issue in Solita’s Harja project.



Our team develops a large software project, called Harja, for the Finnish Transport Agency. [Harja is open source, developed with full-stack Clojure and can be found in GitHub](https://github.com/finnishtransportagency/harja). Our team size has varied between 3 to 7 software developers, a UX designer and a project manager.

After almost two years of development, we made the first major release of Harja in October 2016. Harja is used by three major user groups: the Finnish Transport Agency, the local transportation officials and the road maintenance contractors. Harja helps officials to monitor that the contractors do their work as agreed in the contracts.

With the first release Harja replaced two older software products that had been used for years. The end users were forced to quickly adopt a new software tool that was supposed to help them to do their work even better.

As always, changing to a new tool caused some resistance. Harja provides a feedback channel which enables end users to send us feedback, feature requests and bug reports via email. This feedback email box was a terrific idea – we found a way to hear instantly how our software fulfilled (or didn’t!) the needs of our users.

We had encouraged our users to give lots of feedback and suggestions for improvements. When the feedback started flowing in, we were happy. Many of the requests provided us new information how the system should work. However, soon it became clear that the amount of feedback was getting very high – too high. With our way of working at that time, we were not able to keep up the pace in new feature development that our customer also wanted. We were not smart enough yet how to multitask with new feature development and provide end user support.

After the first release, our initial process with the feedback relied almost solely on project manager. The project manager was supposed to deal with all the feedback emails in order to enable software folks to focus on further development work. Should she need technical assistance, she would ping a developer. Due to other responsibilities our project manager had and the large number of feedback, this process didn’t really work but unread feedback issues started piling up on our project manager’s desk. 

We needed to change the process quickly so we decided to engage the whole team with the feedback handling to eliminate one person becoming a bottle neck. We started to go through the feedback list by the whole team at the end of the daily meeting. This way we got visibility to what’s going on, and were able to assign issues that needed fixing directly to developers.

This helped us, and after a few weeks we had cleared up the whole feedback issue list. It almost seemed we were on top of the feedback problem. But after some more weeks we learnt we had solved the problem by adding way too much working hours to feedback handling. This made new development suffer. Besides, many of the issues turned out trivial, they were either not problems at all, misunderstandings of the end user or otherwise did not require technical expertise to resolve. Going through the list with the whole team cost time and made developers feel they were not able to code new stuff fast enough. With so many people involved, handling the feedback was inefficient and rather chaotic than well-organized. In one of our regular retrospective meetings many team members wanted to do something about it. It was time to rethink the whole process once more. We set some goals how a better feedback handling process should look like:

*	User feedback is very valuable so users deserve to be responded without long delays
*	Fix any “easy fixes” rapidly
*	Team members must be better protected against constant interruptions
*	Project manager must get help from developers rapidly when she needs it
*	All the feedback must not be handled by the whole team (too much waste)

Through intense discussions, we gradually developed a better process how to handle the feedback. We decided to assign every day a different developer to help project manager handle the feedback. We named this role ‘the goat’ – don’t ask me why. So the goat was now a circulating role in the development team to help project manager with the feedback.

![Goat](/img/simultaneous-development-and-support/goat.png)


## How ‘goat’ works

Imagine there are 20 emails in feedback inbox from yesterday. Project manager goes them through and she is able to tackle 14 of these issues independently. 6 of the issues are too technical so that project manager can’t decide what our team should do with them. She marks those issues with "goat" label in JIRA. Goat is responsible for all the goat issues. Then the goat looks into those issues from technical point of view and decides whether they are bugs that can be fixed in our team or need e.g. communication to external stakeholders that use our APIs. The main advantages of having a goat for the team are:

*	Everyone is the goat only once a week so there is little burden to new development work. Developers get to write more code, ie. do the work what they love the most
*	Everyone gets to be the goat regularly, so everyone has an up-to-date understanding what kind of issues our end users are facing
*	The goat token is passed on in our daily meetings. Thanks to physical token, project manager always knows who she can poke when she needs technical support

Adopting the goat process has been a great success in our team. Our daily meetings are started by the current goat who gives an update what he/she has achieved as a goat. Then the goat is passed to the next one. Feedback issues get processed so that majority of the team can write new code uninterrupted. The project manager also has a colleague to sort out the feedback. If your team needs to excel in both new development and maintenance, we can wholeheartedly recommend you the goat. Feel free to invent your own name and token for the process, though!

PS. If you'd like to read more about Harja's development process, check also [10 Things that Make Development Process Awesome](http://dev.solita.fi/2016/07/04/10-things-that-make-development-process-awesome.html) - a great posting by my colleague.
