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
having the power, resources and ability to do it. And of course It's about hacking yourself first. A somewhat mechanical implementation would be to add a
"security specialist" to development team, as you could add some "system operation specialist" and say you're now
doing DevOps. In our opinion, this approach is a minor improvement and totally misses the point about *culture*. A culture is about 
values and beliefs shared by everyone. It is not enough that a "security expert" sits with the team, if that person
is the only one concerned about security. The DevSec goal is to make every developer think about security and acknowledge 
it is necessary. Not everyone needs to be an expert, but everyone needs to understand that security is essential and important.

## What is "security" actually?

The so called CIA triangle consists of confidentiality, integrity and availability. These are not technical concepts, they are important business concerns. Lose confidentiality, and you'll lose customers. Unavailable services do not make money and if you lose integrity, you can't rely on your data. 

![CIA](/img/devsec/cia.png)

The attackers have a number of potential routes to affect the system's CIA qualities:

* Physical security of data center and client machines
* Hardware security
* Network security
* BIOS security 
* Operating system security
* Application server security
* Language and framework specific security 
* Component security
* Code
* Data integrity

Sofware architects and developers design software architecture that affects these issues. Security should be one consideration when operating systems and technology is chosen for a software system. The development team usually doesn't need to worry about BIOS security or physical security of the data center, but many security controls are at their responsibility.

## Security conscious developers

As we said, DevSec calls for developers to become conscious about security. We recommend a secure development lifecycle model as a starting point for practical everyday work. It dictates what needs to be dealt with, but the team decides what is the proper thing to do in their particular context. If you are a wildling and do not like processes you can also try "hack yourself first" motto as your starting point. Here's an example list of actions and decisions to make:

* Train your personnel.
* Know the policies and laws that affect your project.
* Document your architecture and understand your attack surface.
* Do a threat analysis and risk assesment.
* Follow vulnerability feeds for your technology stack.
* Keep on track about dependencies and their possible vulnerabilities.
* Know the best practices with your technologies.
* Analyze your code and configurations.
* Do inhouse penetration testing, try to break your system.
* Monitor your application.
* Automate alerts for anomalies in the usage patterns.
* Do incident & response handling.
* Prepare and plan for compromise.
* Revalidate on changes.

It's important to understand that cybercriminals estimate payoff/risk and payoff/effort before they seriously attack a system. If your system is difficult to crack, it won't get attacked unless there's a very big payoff. The criminals take the easy money, always.  Hackers and hacktivists might have other motivations, but here's a rough model for calculating "criminal value" of a system:

**expected value = (effort / direct payoff) / risk factor** 

Threat analysis will give insight into payoff and risk factors and you can tune the security practices accordingly. As a software designer, you can't do much about the direct payoff usually, but you can directly affect the effort and to some extent the risk factor faced by a would-be attacker. 

![Seagull](/img/devsec/seagull.jpg)

## What about automatization?

Trying to script and automatize things is deep in the nature of the developer. Some of the security related testing can also be automatized. We have already our continuous integration pipelines in place so we can easily add few more testing steps into that pipeline. When automating you should remember that not all of the security testing products are meant to be automatized. It is not a replacement for manual testing but it can still support you in a long run. Atleast automated test gives you advantage to follow how your products security changes on each build and to get alerts from delta values. 

Here are few things we have been trying to automatize:

* Static code analysis
* Web application penetration testing
* Attack surface analysis
* Virus scanning
* Known vulnerability analysis 
* Performance testing
* Monitoring setup

Succesfulness depends a lot about the solution itself and the technological stack that you are using. It is common to get a lot of noise from automatical testing and you need to cherry pick critical information and delta values from the test results. 

By automatizing some things and by adding few important things from secure development lifecycle process we can derive our own cyber security pipeline. 

![Seagull](/img/devsec/cyberpipeline.png)

## Our experiences

We have embraced DevSec. Our customers have been pleased that have been able to discuss and bring up relevant security issues. While doing security testing we often find logical flaws in the software, not just security issues. In our experience, third party penetration testers are expert hackers obsessed with "pwning" the system, and may disregard non-security related bugs. Or they might miss the implications of logical bugs as they have a superfluos understanding of the system context.

Training, threat analysis, tools etc. cost money, but this should not become a problem. A discussion with stakeholders is necessary as ultimately these costs have to be covered by the customers. It may be necessary to explain to people why a threat analysis or penetration test is beneficial, but as news about cyber attacks are common everyone kind of understands that security is important. In our opinion DevSec is a very cost-effective and rational way to improve security in the coming years.

