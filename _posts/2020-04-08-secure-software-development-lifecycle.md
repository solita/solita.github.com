---
layout: post
title: How to implement a secure software development lifecycle
author: Rinorragi
excerpt: Sharing my experience and thoughts about implementing a secure software development lifecycle
tags:
- InfoSec
- Software security
- DevSecOps
---

## What is the Secure Software Development Lifecycle

Have you ever found yourself wondering if the system you are implementing is secure enough? I have. Quite often actually. It is not an easy question to answer unless you are prepared. This blog post is about how to prepare yourself for that question. The short answer is the Secure Software Development Lifecycle which I will call SSDLC from this point onwards. 

Software development is usually divided into different phases. The amount can vary depending on the software project management framework in use. The phases comprise of short iterations or one long waterfall or anything between. These phases could be for example:

![ssdlc phases](/img/ssdlc/phases.png)

SSDLC complements the phases with security requirements. This ensures security is considered in all phases of the software project. 

## Why does secure software development lifecycle matter

It is time for mandatorial motivation! Why does this matter? Why I am reading this? Is this yet another SAFe or ITIL? 

You should think SSDLC as more akin to agile development. Where agile development advocates for adaptiveness and continual improvement SSDLC should do the same. By itself it does not give you any value unless you are able to implement a useful set of tools and processes that supports your business goals. The same applies for SSDLC. The main goal is to provide a set of security oriented best practices for your existing development practices. 

![processes](/img/ssdlc/processes.jpg)

So what happened to "build the software and let security engineers test it afterwards"? The same happened as with all the other testing too. It is much cheaper to catch mistakes early. Security problems introduced in requirements or in design are pretty expensive to fix if you let them go to production. For example you might notice that your software violates the GDPR. You want to fix them early. To catch them early you need supporting routines to have a systematic approach in finding them. That is what SSDLC is all about. 

## How to implement secure software development lifecycle

Start small and make it evolve over time. Treat the improvements in SSDLC like you would treat any other process improvements or quality assurance tasks. Make them as visible for in your agile boards and make a supporting document that clearly tells what you are after.

#### Requirements

Requirements stem from laws, regulations, company policies and customer company policies. Failing to notice these will make it difficult to deal with them later. Gathering intelligence on what you are about to do businesswise should make you able to also make some security requirements for the project. This will create the foundation of your security awareness level later on. Are you dealing with credit cards? Surely you have then heard about PCI-DSS. Are you creating an application for healthcare? Maybe you ought to know something about HIPAA. Know your industry and make use of whatever given requirements there are for the field. You should also have a hunch about data classification levels.

To sum it up: 
* Know the laws and regulations
* Follow company policies for your own company and for your customer company
* Check for useful standards
* Make security requirements
* Implement data classification process

#### Design

Design sets a foundation for software architecture. Security is all about CIA (confidentiality, integrity and availability). Failures in software architecture affect one of the letters of CIA and they are also often pretty expensive to fix. To fight this we would like to review design documents from security perspective. There are plenty of tools and practices in different software project management frameworks but I would like to emphasize threat modeling. There are different approaches for threat modeling but what I have found useful is to create diagrams for software architecture from different approaches: deployment pipeline, infrastructure and networking, sequence diagrams and workflows. Reviewing those diagrams from the "how would I hack this?" -perspective is really useful. You can also go so far that you create evil user stories for the backlog. 

To sum it up:
* Create architecture diagrams and review them
* Do threat modeling 
* Create evil user stories


#### Implementation

Implementation is what developers love. There are numerous ways to improve security or make horrible mistakes at this phase. The most important thing will be your developers security awareness. Many of the security issues are more or less stuff that nobody gave a second thought. Yes, I mean the OWASP Top 10 stuff like SQL injections. One thing you need to understand about developers is that they love to solve problems. The normal trick is to try to dress security requirements as a solvable problems like "make sure that all input is sanitized against SQL injections" and "make sure that all output is sanitized against XSS". This is important but of course covers only one problem at a time and it will become a pretty exhaustive list to implement all over again in every project. Oftentimes more eyes at the same problem will help in finding loopholes in your security design. 

As a software developer and a security enthusiast I could go on forever on this topic but more or less I will just list here things that you should consider:
* Know or setup secure coding practices for your language and frameworks
* Validate all the 3rd party libraries you take in
* Fail securely
* Manage your secrets with best practices
* Know the HTTP security headers or atleast know how to check them
* Understand the cryptography you are using
* Don't roll your own crypto
* Basically memorize the whole OWASP TOP 10 and constantly consider them as a threats
* Use XP programming
* Have a review process
* Find tooling that supports your work
* Sanitize inputs
* Sanitize outputs

#### Test

Now that we have security requirements we also need to verify that we fulfill them. Security testing works relatively similar to any other kind of testing. A helpful thing to do is to setup a good continuous integration environment that gives your development team constant feedback about how they are doing. If they are more into DevOps or DevSecOps then they most likely will build it by themselves but some organizations have different people for these tasks. I consider continuous integration as testing as it is something that is outsourced to a system that gives you feedback on your work. Some could also think that it is part of the implementation. 

Things that you can automatically test that help security:
* Performance
* Security headers
* TLS and its configurations
* Unit tests (also integration test, end-to-end tests, smoke tests and all the similar)
* Known vulnerability analysis for your dependencies
* Fuzz testing
* Static code analysis for your source code
* Best practice analysis in some cases

You should not forget manual testing. For example:
* Review what others have done
* Exploratory testing
* Penetration testing
* Conduct a disaster recovery exercise

#### Deployment

The moment you publish your source code as software it becomes legacy and you need to support it. From the SSDLC perspective this means that you need to actively do the things that you need to have processes for. It also means that you have published your software open for use. You will get feedback and you need to have processes to deal with it. You can gather insights of the usage by monitoring the software but you could also make your software open for hacking with bug bounty program. The minimum requirement is that you know how to process feedback.

* Implement change management process
* Read the news (and vulnerability informations)
* Implement incident and response processes
* Monitor your system and raise alerts when needed
* Introduce a bug bounty program

#### Retirement

This is often forgotten in all projects. Some day the time of our beloved system will come to an end. At this point the system has had a great deal of organical growth and understanding the implications of the retirement can be hard to see. The system needs to be taken down in a managed manner so that business can move to a new world, but at the same time all the resources of the system need to be disposed in a governed manner. Failing to due so will lead into an information leak. 

Things that you should consider:
* Migration plan
* Archiving data (there might be laws)
* Destroying virtual or physical resources
* Cleaning up the data stores
* Cleaning all the DNS names and such to avoid subdomain takeovers (especially with cloud)


#### Example implementation

People at Unity Tech have been so awesomely kind that they have published their SSDLC as [open source](https://github.com/UnityTech/unity-ssdlc/blob/master/Overview.md). I would strongly recommend looking at it as an example of an implementation.

## My experience on the matter

Taking security oriented tasks on the backlog has been natural since security has been brought up in front. Communication between different parties has been easy since we have had structure and documentation for the security conversations to take place. For example not a single threat modeling session has been in vain. It might feel before that we already know everything but there is always something we have missed.

Key factor for making the secure software development lifecycle to work is to find a spokesperson within your project for the matter. It does not need to be an extra guy but just somebody who likes to be a spokesperson for security matters. This person does not need know everything about information security as software development is always team work. It is just a good idea to have somebody who keeps on track about all security related solutions in your project and understands the bigger picture.

## Useful information sources

The subject is not new and it has had many names. Microsoft SDL is maybe one of the first sources but it feels like more tailored towards product development. The OWASP Testing Guide considers the different phases of the software devlopment lifecycle. NIST has had its own publications and there is also an ISO standard to dive in. Below is a list of useful sources that I have ventured on my journey. 

* [Microsoft SDL](https://www.microsoft.com/en-us/securityengineering/sdl/)
* [OWASP Testing Guide](https://owasp.org/www-pdf-archive/OTGv4.pdf)
* [NIST Secure Software Development Framework White paper](https://csrc.nist.gov/CSRC/media/Publications/white-paper/2019/06/07/mitigating-risk-of-software-vulnerabilities-with-ssdf/draft/documents/ssdf-for-mitigating-risk-of-software-vulns-draft.pdf)
* [Unity Tech Open Sourced SSDLC](https://github.com/UnityTech/unity-ssdlc/blob/master/Overview.md)
* [PCI Secure Software Lifecycle](https://www.pcisecuritystandards.org/documents/PCI-Secure-SLC-Standard-v1_0.pdf)
* [SAFe Code Fundamental practices for secure software development](https://safecode.org/wp-content/uploads/2018/03/SAFECode_Fundamental_Practices_for_Secure_Software_Development_March_2018.pdf)
* [BSA Software security framework](https://www.bsa.org/files/reports/bsa_software_security_framework_web_final.pdf)
* And of course the ISO 27034 application security guideline