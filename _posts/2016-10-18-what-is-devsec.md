---
layout: post
title: What is DevSec
author: Rinorragi, lokori
excerpt: DevSec is a emerging trend to move developers closer to security experts, akin to DevOps. In this blog post we argue that this is necessary and how this will improve security, while simultaneously lowering the costs. We wil also cover how to do this in practice.
tags:  
- DevSec
- security
- DevOps
---

DevSec is a emerging trend to move developers closer to security experts, akin to DevOps. In this 
blog post we argue that this is necessary and how this will improve security, while simultaneously
lowering the costs (time and monetary costs). We will also cover briefly how we have been moving
to this direction in practise.

## Why?

How often have you heard that "you just can't add security afterwards" and 
"security has to be thought of all the time"? This is the main concern DevSec aims to address. Most people
realize that you can't add security afterwards, any more than you can add usability or quality after the product is "done".

DevSec is not the only solution, as there are plenty of presentations about integrating security related
work to agile development cycle. Even somewhat formalized processes, like 
[Microsoft's "Security Development Lifecycle"](https://www.microsoft.com/en-us/SDL/Discover/sdlagile.aspx). 
What's different in our opinion, is that we feel that process is not the answer. Rather, we prefer to make
developer teams capable of taking responsibility for the security. Changes in the process are a good thing,
but they are a result, not the starting point.

## What is DevSec?

Like DevOps, this is about the culture. It's about responsibility. It's about knowing the right thing and
having the power, resources and ability to do it. A somewhat mechanical implementation would be to add a
"security specialist" to development team, as you could add some "system operation specialist" and say you're now
doing DevOps. In our opinion, this approach is a minor improvement and totally misses the point about *culture*. A culture is about 
values and beliefs shared by everyone. It is not enough that a "security expert" sits with the team, if that person
is the only one concerned about security. The DevSec goal is to make every developer think about security and acknowledge 
it is necessary. Not everyone needs to be an expert, but everyone needs to understand that security is essential and important.


## What

Classic CIA triangle consists of confidentialy, integrity and availability. All of those three factors thrive towards keeping business ongoing. By losing confidentiality we will lose customers, by losing availability we can't have business and by losing integrity we can't rely on our data. To achieve security we have quite a long list of items where attacker could affect. 

* Physical security of data center and client machines
* Hardware security
* BIOS security 
* Operating system security
* Application server security
* Language and framework specific security 
* Component security
* Code 
* Data integrity

Sofware architects and developers design software architecture that affects items above. By choosing certain technologies you will limit your options in application servers and operating systems and maybe also in hosting partners. In each level we need to have some kind of security controls to be sure that our systems is not easily compromised. In the end it is the development team that knows the needed pieces to run the production environment. 

## How

I myself prefer to bind secure development lifecycle model into our project. It dictates that what kind of thinking should be done during the project. There are steps that may need some training like penetration testing. 

* Train your personnel 
* Know the policies and laws that affects your project
* Document your architecture and understand your attack surface
* Do a threat analysis and risk assesment
* Follow vulnerability feeds for your technology stack 
* Know the best practices with your technologies
* Analyze your code and configurations
* Keep on track about dependencies and their possible vulnerabilities
* Try to break your system
* Try to break other systems (with permission of course)
* Monitor your application 
* Know what is normal use and get alerts from anomalities
* Do incident & response handling
* Plan for compromise 
* Revalidate on changes

Techniques you use and the intesivity of the security depends on your application. Still you should never neglect security. Try to be better than your competitors since attackers calculate gain per effort ratio. 

## How has it worked

By embracing DevSec a lot of cool things has already happened. Our customers have been pleased when we have brought up things that have security issues. By doing security testing it is likely to find also not just security flaws but also logical inconsistencies in the software. By ordering penetration testing outside of the company you might not get all the ugly functionalities into your reports because security companies are mostly interested on security issues. We also noticed that having developers doing penetration testing also helps us to find vulnerabilities in third party components and report their vulnerabilities to them and thus helping community.  