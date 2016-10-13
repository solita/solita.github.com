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

Security is not just knowing the OWASP TOP 10 lits and trying to avoid implementing any of them. Security as a word covers quite a long list of items. 

* Physical security of data center and client machines
* Hardware security
* BIOS security 
* Operating system security
* Application server security
* Language and framework specific security 
* Component security
* Code 
* Monitoring
* Incident & response 
* and more 

Who takes the responsibility of the whole stack? The whole solution security. 

## How

I myself prefer to bind secure development lifecycle model into our project. It dictates that what kind of thinking should be done during the project. There are steps that may need some training like penetration testing. 

## How has it worked

By embracing DevSec a lot of cool things has already happened. Our customers have been pleased when we have brought up things that have security issues. By doing security testing it is likely to find also not just security flaws but also logical inconsistencies in the software. By ordering penetration testing outside of the company you might not get all the ugly functionalities into your reports because security companies are mostly interested on security issues.