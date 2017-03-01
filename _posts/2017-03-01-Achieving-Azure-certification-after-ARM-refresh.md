---
layout: post
title: Achieving Azure certification after ARM refresh
author: Rinorragi
date: 2017-03-01 15:45:00 +0200
excerpt: Tips how to achieve Azure certifications
categories: 
- Episerver
tags: 
- Episerver 
- DOTNET 
- DevOps
- Azure
---
I started developing on Azure when the current "old portal" did not yet exist. Back then Azure resources were managed with Silverlight portal. After being around in Azure for years I decided to give a shot for the certifications while I can still earn both MCSE and MCSD with the same trouble. MCSD is expiring at the end of march 2017. Here are some observations from the certification journey. 

## Overall feeling about the exams

They reflected real life quite well. I was actually surprised that there were only few questions that got me angry. The upsetting ones were either confusing or asked about numbers that I don't feel like wanting to memorize. If you are not familiar with the Microsoft exams, then you should know how they are structured. There are four things that you will find in every question. 

* Business problem (enterprise x is developing y to achieve business goal z)
* Goal statement (you need to solve issue x)
* One or more correct answers 
* DISTRACTERS (stuff that are not related to problem scenario but rings bells in your head as they are familiar)

Try to extract the essence of the question out and then eliminate the distractors. Some of the distractors were so bad that I was still wondering about them 10 questions after. 

Were the questions easy? No. Having years of experience from three generation of Azure portals I just barely passed the first one. Second one went through with a bit better score and the third one with the highest score. I took them in an order that I thought was most familiar to me: development, architecture, infrastructure. What does this tell? They overlap a lot so each round was easier because of more studying on a same subject.

How to mentally prepare yourself to the quetions? Ask yourself questions like "There is a problem with x, where would I find logs?", "How do i scale this?" or "How do i secure the connection?". If you can answer those, then you will most likely be successful in eliminating the distractors out of the scenery. Even if the options you are left are nearly the same you have still atleast improved your odds!

## About the certificates and the ARM refresh 

![Tools](/img/azure-certification/mcsd_pyramid.png)

This is how the old pyramid looked like. And the new one is actually with the exact same format. The lowest tier is the technology specialist tier which you get if you pass a certain kind of exam. The middle tier is solution associate tier which you will get by passing two exams. The highest tier is solution expert tier, which you will get after passing one test and having the solution associate already. 

Before studying any further notice that when redesigning the tiers they actually changed the contents of the few relevant exams. Before paying for any training material make sure that the ARM refresh is mentioned. For example books that were preparing for 70-532, 70-533 and 70-534 tests have not been updated. In my experience, you can pretty safely forget the "old portal" and focus on the newer one.

* [MCSD certification](https://www.microsoft.com/en-us/learning/mcsd-azure-architect-certification.aspx)
* [MCSE certification](https://www.microsoft.com/en-us/learning/mcse-cloud-platform-infrastructure.aspx)

Note that there are also other routes to the same MCSE! You don't need to take any of the exams that I took. 

## No more recertification

I have always hated the recertifications. The new tier of Microsoft certificates seems to be lacking of expiration date. I love that. As a developer I get nothing out of recertification for the subject that I have already been certificated. If I have forgotten something during the 2-3 year period then I'm sure that it has not been important. Renewing the internals of the exam won't help the core of the exam mostly remains the same still. I would rather expand my view of sight by taking a new certificate. 

Hint to Episerver: you could learn from the security scene. There you can keep your qualification alive by gathering points from events. Like doing a blog post or speaking in a seminar. That would work for Episerver certifications too. This does not prevent that you could take recertification if you wish. There are much more like assessments, projects, forums, support tickets, and GitHub repositories that you could track. Nothing in this prevents from taking the certification test again. 

## Three exams, seven certificates 

At the edge of certification era change I was able to get seven different certificates with three exams. How is this possible? Well, technology specialist certification is granted from each exam. After two exams solution associate certification is granted. Finally, I was granted solution expert and solution developer certificates from passing all three exams. As a bonus, I also got MCSD App Builder by having MCSA: web applications already in my pocket. The full list is:

* Microsoft Specialist: Developing Microsoft Azure Solutions
* Microsoft Specialist: Architecting Microsoft Azure Solutions
* Microsoft Specialist: Implementing Microsoft Azure Infrastructure solutions
* Microsoft Certified Solutions Associate: Cloud Platform
* Microsoft Certified Solutions Developer: Azure Solutions Architecting
* Microsoft Certified Solutions Developer: App Builder
* Microsoft Certified Solutions Expert: Cloud Platform and Infrastructure

Expect to earn at least five certificates by targetting to MCSE. 

## 70-53x overlaps with each other

Despite which number of exams you are going to take, I strongly suggest that you check the materials of each three exam. There were lots of stuff even in Ignite cert preparation videos that would have been beneficial for me in the first place. Here are the list of similarities: 

* ARM templates
* ARM virtual machines
* ARM Networking
* Storage solutions (especially Azure Storage)
* Web apps
* Managing identities

I don't mean to say that the tests are the same. Each exam certainly has its owng angle to the subject. Expect to see code in developer exam, expect to see command-line stuff in infrastructure exam and expect to see design problems in architecture exam. Still, there are lots of questions like "Which is the best for job x in circumstances y?" and the answer would be same regardless of the exam the question was in. 

The thing is that you can learn from many of those subjects by learning the ARM templates. So make sure that you study at least this [walkthrough](https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-template-walkthrough)

## Hot topics 

Where to focus? What to learn the best? It's hard to go wrong with these:

* Azure PowerShell (try to setup environments with it directly creating the resources and with arm templates)
* ARM templates (use the automation button in portal and try to understand the json)
* Storage (I made example clients and I did not need to regret it)
* Web apps (especially the pricing tiers, scaling and monitoring) 
* Virtual machines (pricing tiers, scaling and monitoring)
* Hybrid cloud (how to connect on-premise stuff to cloud and vice versa)

## What to expect from 70-532 Developing Microsoft Azure solutions 


Case studies and code examples. You don't need to be a good programmer to pass this. You need to know the services listed in the exam and how to do design decisions with them. To be honest, I felt that this was more of a DevOps test than a developer test. There were code yes, but if you think what are the services that needs specific kind of coding to work you don't have that much to learn. Those things are:

* WebJobs
* CloudServices (role entrypoints and stuff)
* Storage clients 
* Azure Service Bus clients 

The thing is that you need to know a lot about things like DNS, HTTPS, deployments, monitoring and scaling to pass this test.  In some organizations this might not be typical for developer. The DevOps-loving Solita of course knows this all! 

* Link to the [exam](https://www.microsoft.com/en-us/learning/exam-70-532.aspx)
* Link to the preparation [video](https://channel9.msdn.com/Events/Ignite/2016/BRK3261)

## What to expect from 70-533 Implementing Microsoft Azure Infrastructure solutions 

I was not entirely sure what to expect from this one. I watched The Ignite videos and studied the docs. It was helpful. Notice that the exam materials say that you need to know how to implement Windows and Linux systems. Yes, Linux in Microsoft certification. Luckily, I had used Linux enough that I was able to answer the questions without preparing to answer to them. 

* Here are a lots of useful stuff at [IaaSOpsGuide](https://aka.ms/Azure/IaaSOpsGuide).
* You might be also interested in [tools](http://aka.ms/Azure/tools)
* Link to the [exam](https://www.microsoft.com/en-us/learning/exam-70-533.aspx)
* Link to the preparation [video](https://channel9.msdn.com/Events/Ignite/2016/BRK3262)

## What to expect from 70-534 Architecting Microsoft Azure solutions

All I can say is that try to understand purpose of every thing in this picture: 

![Tools](/img/azure-certification/mcsd_pyramid.png)

Make extra sure that you understand the purpose of different Azure connectivity options (p2p, p2s, ExpressRoute) and that you study hybrid cloud solutions. There were questions related to nearly every service I service I could think of and it was up to luck if the questions were detailed and hard or merely just about knowing the purpose of a service. 

Picture was borrowed from [channel9](https://channel9.msdn.com/Blogs/The-Game-Blog/A-Quick-overview-into-typical-Architecture-for-a-Cloud-Based-Gaming-Services)

* Link to the [exam](https://www.microsoft.com/en-us/learning/exam-70-534.aspx)
* Link to the preparation [video](https://techcommunity.microsoft.com/t5/Microsoft-Ignite-Content/BRK3264-Cert-Exam-Prep-Exam-70-534-Architecting-Azure-Solutions/td-p/9675)
* Udemy course that helped me to get the [overview](https://www.udemy.com/70534-azure/)

## How to study 

Everyone has their own way to learn. I would still mainly focus on all the materials on under the [Azure docs](https://docs.microsoft.com/en-us/azure/). Then I would definitely watch the preparation videos from Ignite 2016, all three for every certification (with 1.5x speed). And finally I would go out to the portal. I would press buttons N (for new popup) and B (for browse) and setup all the stuff that are mentioned on the exam. I would also definetly press the "automation" button that would show me the json template of the stuff I was about to create. I would also study resource groups json template after I would have set all in place.  

There are also a lot of "reading lists" available for the certifications. I checked a few but so many things have changed so recently and so many links were broken that I can't really recommend those.

Braindumps are no-no for me. But I think that there is kind of "official" practice tests available. You should learn explanations from them if you buy them. I didn't want to invest to those because I felt confident even without them. Measureup had refreshed atleast some of their tests to the ARM era. 

## Why?

Why would you want to certificate? Well, the usual list is kind of boring. Partnerships, CV, sales, test your limits etc etc. I took the exams because my company encouraged me to do this. My company also supports certifications by giving a chance to study during worktime. Of course, I also got a chance to refresh my knowledge on the areas that are not so familiar to me. 

## How was this related to Episerver?

Most of the time the customer is heavily influencing where to host Episerver. Azure is one option. DXC also runs on top of Azure. There is really no harm to understand in depth Azure as a hosting option or as an option to implement microservices-related to Episerver projects. Azure AD is also a possibility for identity federation. 

## How much effort for this all?

From 10-15 hours preparation for each test. Then, a few hours to take the actual exam. That was it for me. I got the whole thing done during February 2017. 