---
layout: post
title: Back to business
author: riikkanen
excerpt: TODO
categories: 
- normipäivä
- programming
---

##From a mother to a software developer

Clock alarms at 6.15 am. Today I'm lucky and also the children have slept so long. Today is working day, one of my three working days per week. On other days I take care of my three children at home, which is a convenient arrangement for the time being and enabled by my employee, Solita.

After waking up, eating porridge, feeding porridge for my 1,5 years old daughter, making braids for my 6 years old daughter and saying bye-byes also to my 4 years old son and my dear husband, I take my bicycle and pedal to work. Cycling is a wonderful way to switch the context in my head from home matters to work issues. When I arrive to our office, I take my bag and change clothes, like Superman in a phone booth, turning from a mother to a software developer. 

This is my 12th working day after quite a long break, a little over 1,5 years maternity leave. Before that I had been working in KIRRE project since 2010. In KIRRE I worked as a software developer and had my hands on both in back end and front end. KIRRE project was dealing with registry of legal confirmations to real properties. 

##Jump to the moving train

After working a long time in the same project, it seemed to be reasonable to change the project, from real properties to a completely different world, railways. LIIKE project has been started in 2008 in co-operation with Liikennevirasto. LIIKE projects deals with managing the capacity of railways and supervising and controlling the actual traffic. The project contains maintenance and support, but also further development.

It's always a challenge to familiarize oneself with a new business branch, ecspecially when the project has already been active for a long time and the business logic is full of little but still essential details. A huge amount of information is just waiting to be digested.

LIIKE project consists of several applications developed using various technologies. The back end is implemented using Java. In the front end there are both web and desktop applications. 

##A story of one Jira-ticket

Our backlog of tasks to be implemented is stored in Jira. One can pick a task from the backlog and start implementing the task. As I'm a novice in the project the project manager has picked suitable tasks for me. Not too fierce in the beginning. Today I started with a task about showing an icon and tooltip in the user interface when there is something worth of noticing when a train assembly is inspected, e.g. the train is longer than it should.

We use IntelliJ IDEA as development environment. I've cloned the project codes from remote repository to my local repository using Git. IntelliJ IDEA feels quite familiar after using Eclipse but I'm just hoping that they had similar keyboard shortcuts. I still try to open types with Ctrl + Shift + T and so on. Git is also a new acquintance to me. I still feel a little bit clumsy with all the branches but I like the idea to be able to make commits just in my own repository.

The task in hand needs to be done in Reaali application which has user interface implemented using Java Swing. I have not used Swing since 2005 but there is some correspondence to Apache Wicket which was used in the previous project. However, when using Swing, html-tags need to be used only when formatting tool tip texts. 

I go through the code and find the right place to make changes. Lucky for me, the data needed for the tool tip is already fetched to the model. I don't have to touch the back end at all. Only thing left to me is to write logic for showing the icon and tool tip when there is something fishy in the train setup. I notice that there is also a similar table in another dialog, so I decide to make the change also there. Hence, I use a little bit more time and effort to write some common TableAdapters and CellRenderers to be used in both tables. I tidy up the code I wrote, test and review it by myself. 

When I'm happy with the change, I make a commit to my own repository. I've been making the changes into a separate branch which is dedicated for this Jira issue only. After commit I push my branch containing the change to remote repository. I move the Jira issue for waiting for internal testing. I also create a code review because the change was a little bit more complicated than I first thought and link the review in the issue. I also need to remember to update the Reaali user manual which is maintained in Confluence.

The task will be waiting for some of my project-mates to review the change. If reviewer does not find any problems, the branch containing the change can be merged to our master branch. After pushing the changes to the master, automated continuous integrations jobs, which are run on Jenkins, will take care of running all the tests also for the changed code.

##Afterwords

The comeback to the working world has been exciting and a little bit unnerving. The last 1,5 years have gone by without even thinking of Java (what?!?! there is already Java 8, my certificate is on Java 5), version control, coding or anything related to technology or software development. No, I have not had any time to make ambitious projects in my spare-time (what is that?!?) such as many of my colleagues seem to be doing. However, after these 12 days I've been glad to notice that I've not forgotten everything. I'm not a lost case at all. Also, getting familiar with the new project has started fine, thanks to helpful workmates.

The long experience in software business has not disappeared during the maternity leave, even though it sometimes felt like it. And after all, the work of software developer is learning of new things, ways and technologies anyway. I also notice that working as "project manager" at home has given me more perspective and ability to take care of tasks at hand even in shifty environment. 

I appreciate the ability to combine maternity and work in such a fluent way, already third time for me. I think otherwise I would have been even longer at home taking care of children. In my opinion, the longer the break is, the harder it is to come back to business. Hence, I think that the shortened work week is a win-win situation for both employee and employer. 

Besides of everything, I enjoy adult lunch and coffee company a lot. <3







