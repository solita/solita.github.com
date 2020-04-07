---
layout: post
title: How to implement secure software development lifecycle
author: Rinorragi
excerpt: Sharing my experience and thoughts about secure software development lifecycle
tags:
- infosec
- software security
- devsecops
---

## What is secure software development lifecycle

Have you ever found youself wondering if the system you are implementing is secure enough? I have. Quite often actually. It is not an easy question to answer unless you are prepared. This blog post is about how to prepare yourslef for that question. The short answer is Secure Software Development Lifecycle which I will call SSDLC from this point onwards. 

You should be familiar how developing software is divided in different phases. There can be more or there can be less depending on the chosen software project management framework in use. They phases can exists in short iterations or in a one long waterfall or anything between. These phases could be for example:

![ssdlc phases](/img/ssdlc/phases.png)

What SSDLC does is to put security requirements for each of the phases. This leads you to consider security in all phases of the software project. 

## Why does secure software development lifecycle matter

It is time for mandatorial motivation! Why does this matter? Why I am reading this? Is this yet another SAFe or ITIL? 

You should think SSDLC to be more like agile development. Where agile development advocates for adaptiveness and continual improvement the SSDLC should do the same. By itself it does not mean anything unless you are able to set a useful set of tools and processes that supports your business goals. The same applies for SSDLC. Main goal is to provide a set of security oriented best practices for your existing development practices. 

So what happened to build the software and let security engineers test it afterwards? The same happened as with all the other testing too. It is much cheaper to catch mistakes early. Security problems in requirements and/or in design are pretty expensive to fix if you let them go to the production. You want to fix them early. To catch them early you need supporting routines to have a systematic approach in finding them. That is what SSDLC is all about. 

## How to implement secure software development lifecycle

Start small and make it evolve over time. Treat the improvements in SSDLC like you would treat any other process improvements or quality assurance tasks. Make them as a visible for in your agile boards and make a supporting document that clearly tells what you are after for.

#### Requirements

There are laws and regulations. There are company policies and customer policies. Failing to notice these will make it difficult to deal with them later. Gathering intelligence on what you are about to do businesswise should make you able to also make some security requirements for the project. This will create the foundation of your security awareness level later on. Are you dealing with credit cards? Surely you have then heard about PCI-DSS. Are you creating an application for healthcare? Maybe you ought to know something about HIPAA. Know your industry and make use of whatever given requirements there are for the field. You should also have a hunch about data classification levels.

To sum up: 
* Know the laws and regulations
* Follow your and your customers policies
* Check for useful standards
* Make security requirements
* Data classification

#### Design

Design sets a foundation for software architecture. Security was all about CIA (confidentiality, integrity and availability). Failures in software architecture most often affects one of the letters of CIA and they are also often pretty expensive to fix. To fight this we would like to setup extra care for design. There are plenty of tools and and practices in different software project management frameworks but I would like to bring out threat modeling. There are different approaches for threat modeling but what I have found useful is to create diagrams for software architecture from different approaches: deployment pipeline, infrastructure and networking, sequence diagrams and workflows. Reviewing those diagrams from the "how would I hack this?" -perspective is really useful. You can also go so far that you will create evil user stories for the backlog. 

To sum up:
* Create architecture diagrams and review them
* Threat modeling 
* Evil user stories


#### Implementation

Implementation is where the stuff that developers love happens. There are numerous ways to improve security or fail bad at this phase. Most important thing will be your developers security awareness. Many of the security issues are more or less stuff that nobody came to think about. Yes, I mean the OWASP Top 10 stuff like SQL injections. One thing you need to understand about developers is that they love to solve problems. So normal trick is to try to dress security requirements as a solvable problems like "make sure that all input is sanitized against sql injections" and "make sure that all output is sanitized against XSS". This is important but of course covers only one problem at a time and it will become a pretty exhaustive list to implement all over again in every project. Often times more eye-pairs for the same problem will help in finding loopholes in your security design. 

As a software developer and security enthusiastic I could go on forever on this topic but more or less I will just b
put a list here things that you should consider:
* Know or setup secure coding practices for your language and frameworks
* Validate all the 3rd party libraries you take in
* Fail securely
* Make sure that your secrets management endures the daylight
* Know the http security headers or atleast know how to check them
* Understand the cryptography you are using
* Basically memorize the whole OWASP TOP 10 and constantly consider them as a threats
* Use XP programming
* Have a review process
* Find tooling that supports your work
* Sanitize inputs
* Sanitize outputs

#### Test

Testing is one that works relatively same as every testing. You should just remember that now that we have security requirements we will also need to verify that we fulfill them. Some helpful things to do is to setup a good continuous integration environment that gives your development team constant feedback about how they are doing. If they are more on the DevOps or DevSecOps then they most likely will build it by themselves but some organization have different people for these tasks. I consider continuous integration as a testing as it is something that is outsourced for a system that gives you a feedback about your work. Some could also think that it is part of the implementation. 

Things that you can automatically test that help security:
* Performance
* Security headers
* TLS and its configurations
* Unit tests (also integration test, end-to-end tests, smoke tests and all the similar)
* Known vulnerability analysis for your dependencies
* Fuzz testing
* Static code analysis for your source code
* Best practice analysis in some cases

You should not forget the manual testing. For example:
* Review what others have done
* Exploratory testing
* Penetration testing

#### Deployment

The moment you publish your source code as a software it becomes legacy and you need to support it. From SSDLC perspective this means things that you need actively do and things that you need to have processes for. 

* Change management
* Reading news (and vulnerability informations)
* Incident and response
* Monitoring and alerting

#### Retirement

This is often forgotten in all projects. At some day the time of our beloved system will come to an end. At this point the system has had a great deal or organical growth and understanding retirements implications can be hard to see. System needs to be taken down in a managed manner so that business can move to new world as it will but at the same time all the resources of the system needs to be disposed in a governed manner. Failing to due so will lead into information leak. 

Things that you should consider:
* Migration plan
* Archiving data (there might be laws)
* Destroying virtual or physical resources
* Cleaning up the data stores
* Cleaning all the DNS names and such to avoid subdomain takeovers (especially with cloud)


#### Example implementation

People at Unity Tech have been so awesomely kind that they have published their SSDLC as an [open source](https://github.com/UnityTech/unity-ssdlc/blob/master/Overview.md). I would strongly recommend looking at it as an example of an implementation.

## My experience on the matter

Taking security oriented tasks on the backlog has been natural since security has been brought up in front. Communication between different parties has been easy since we have had structure and documentation for the security conversations to take place. For example not a single threat modeling session has been in vain. It might feel before like we would already know everything but there is always something we had missed. 

Key factor for making secure software development lifecycle to work is to find a spokesperson within your project for the matter. It does not need to be an extra guy but just somebody who likes to be a communication hub about security matters. This person does not need to be the brighest star on the cyber sky as delegating things is always possible. It is just a good idea to have somebody who keeps on track about all security related solutions on your project and understands the greater picture.

## Useful information sources

The subject is not new and it has had many names. Microsoft SDL is maybe one of the first sources but it feels like more tailored towards product development. OWASP Testing Guide consideres the software lifecycle with the same idea. NIST has had its own publishments and there is also an ISO standard to dive in. Below is a list of useful sources that I have ventured on my journey. 

* [Microsoft SDL](https://www.microsoft.com/en-us/securityengineering/sdl/)
* [OWASP Testing Guide](https://owasp.org/www-pdf-archive/OTGv4.pdf)
* [NIST Secure Software Development Framework White paper](https://csrc.nist.gov/CSRC/media/Publications/white-paper/2019/06/07/mitigating-risk-of-software-vulnerabilities-with-ssdf/draft/documents/ssdf-for-mitigating-risk-of-software-vulns-draft.pdf)
* [Unity Tech Open Sourced SSDLC](https://github.com/UnityTech/unity-ssdlc/blob/master/Overview.md)
* [PCI Secure Software Lifecycle](https://www.pcisecuritystandards.org/documents/PCI-Secure-SLC-Standard-v1_0.pdf)
* [SAFe Code Fundamental practices for secure software development](https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf)
* [BSA Software security framework](https://www.bsa.org/files/reports/bsa_software_security_framework_web_final.pdf)
* And of cours the ISO 27034 application security guideline