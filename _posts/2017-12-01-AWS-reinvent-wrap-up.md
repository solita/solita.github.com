---
layout: post
title: AWS re:invent 2017 wrap up
author: juhofriman
excerpt: Calling all the builders out there! You build it! You run it! And you are proud of it!
tags:
- AWS
- re:Invent
- cloud
---

Chaos. Chaos is the best word to describe this insanely large scale event taking place in an artificial city built in the middle of the desert - Las Vegas! At first, the event just felt bit too much for a small-town boy like myself, but when you just free your mind and go with the flow, and don't even try to attend to all the sessions, you might just get your head up to the cloud.

![The hall](/img/reinvent-wrap-up/reinvent.jpg)

Week was tough, but rewarding. I'm sure whole Solita delegation got heaps and stacks of new ideas in build high class cloud solutions.

## All things secure

Cloud security was a large topic at AWS re:invent 2017. Even Mr Vogel mentioned in his keynote, that every developer must be a security engineer and that is something I can agree completely. When building solutions of any kind, you must take security as a first thing job, and whole team must understand solution end-to-end from the security perspective.

Yours truly took part in the Security Jam hackathon, which was really neat sort of capture the flag competition. Teams we're given AWS accounts that had pre-built solutions running in it with security flaws. Flaws needed to be fixed in order to get points on a road to glory. Unfortunately, our randomly selected team didn't succeed that well, but we had really fun and educational session.

![Security jam going on](/img/reinvent-wrap-up/security-jam.jpg)

AWS offers pretty nice array of security products, but there are loads of pretty impressive companies offering all kinds of cloud security solutions.

**My top-5 AWS security hints**

1. Check your S3-buckets once again and understand the security model of S3.
2. Prepare for DDoS attacks, check out and understand how Shield, WAF, Route53 and CloudFront enables you to mitigate attacks.
3. Monitor your system - you need to know, what's happening all the time.
4. Cut your IAM roles to bare minimum you need in order to keep system running.
5. Understand where you store confidential data. Is there confidential data in RDS? DynamoDB? Elasticache? Logs? EBS? How is that data secured? Have you done risk analysis? What will you do in case of exposure? Check out [Macie](https://aws.amazon.com/macie/).

Speaking of Macie, the next big thing in security will be using machine learning and AI instead of rule based engines.

## All things data

Data is coming more and more in the center of all and this is directly reflected on how we build and craft our systems. We're going towards the world where less and less people actually care about instance operating systems or even instances at all. But the best part of the cloud is that you have both. Raw EC2 instances are not going away.

It's all about **the data** and **the code**.

[SageMaker](https://aws.amazon.com/sagemaker/) is a good example of this in the field of machine learning. Previously you needed to spin up instances to your ML cluster and do all that hard work by yourself. Now you just have the data and the code and spin it through the SageMaker and voila' - you're all set up. To be honest, I really doubt the production class mission critical use of SageMaker, but we'll see how it turns out. At least it seems like something even I could use to try to learn machine learning.

You need to store the data and storing the date got really wide array of new options. [Serverless aurora](https://aws.amazon.com/blogs/aws/in-the-works-amazon-aurora-serverless/) is something that I'm super exited about. I love relational databases and now (well, in few months hopefully) I can just spin up some tables to the cloud instead of provisioning a full RDS instance. There's [Neptune](https://aws.amazon.com/neptune/) as a managed graph database. [DynamoDB global tables](https://aws.amazon.com/dynamodb/global-tables/). [DynamoBD backups](https://aws.amazon.com/dynamodb/backup-restore/) (yay! I really need this!), [Aurora multi-master](https://aws.amazon.com/about-aws/whats-new/2017/11/sign-up-for-the-preview-of-amazon-aurora-multi-master/)...

You have the data, but you need tools to write the code to process the data, right? They announced [Cloud9](https://aws.amazon.com/cloud9), sort of cloud native IDE for developers. And it had the breakpoints for debugging live lambdas! How cool is that! To be honest, I'll stick with my weapon of choice IntelliJ IDEA, but for lambdas cloud9 is definitely something to check out.

When you have the code, you need to deploy it. Whole smorgasbord of exiting new deployment opportunities was introduced for us - the docker freaks. Not interested in provisioning EC2 instances for you docker containers? Use [Fargate](https://aws.amazon.com/fargate/). Love kubernetes? Use [EKS](https://aws.amazon.com/eks/). There eventually will even be Fargate kubernetes!

## All things chaos

I mentioned chaos already. Chaos is something that we have in our systems all the time. When you go from monolith to microservice you introduce even more chaos. People have been really interested in the *chaos engineering* discipline, most notably introduced by Netflix. I had the privilege to attend session by senior chaos engineer Nora Jones of Netflix talking how they do chaos engineering in Netflix scale. We have all heard about the open sourced [Chaos Monkey](https://github.com/Netflix/chaosmonkey), but I really feel that many people don't have that clear vision what chaos engineering actually is. Yes, she also was invited on stage in Vogel's keynote to talk about this.

Chaos engineering is discipline of introducing *controlled*, *managed* and *safe* chaos to the system that is running, and it is meant to expose flaws that can usually not be found with unit or integration testing. I felt that chaos engineering is the next logical step in DevOps and it kinda reminds me about penetration testing.

During Nora's talk, I realized that most of the people already do chaos engineering at some level. I mean we shut down one EC2 instance from our cluster to install patches every night and expect cluster to be healthy again. As a side effect from installing patches, we actually do chaos testing to ensure that the cluster repairs itself in case of EC2 failure. Chaos engineering is something that everyone should and can do. It really is not just for Netflix scale. Just a reminder: you really need to have a **great** monitoring of your system in order to get something out of the chaos caused.

I even managed to catch a copy of their book on O'Reilly called [Chaos Engineering](http://www.oreilly.com/webops-perf/free/chaos-engineering.csp).

![Chaos engineering book cover](/img/reinvent-wrap-up/chaos-engineering.jpg)

Be sure to check out the [Principles of Chaos](http://principlesofchaos.org/) manifesto.

## All things re:invented

Re:invent is something you don't see every day. Over 40 000 people wandering from massive halls to even bigger halls, hoarding for SWAG, listening talks, waiting in lines, drinking beer, tinkering around and trying to figure out how to survive AWS re:invent alive.

Re:play? Let's just say that what happens in Vegas, stays in Vegas.

![re:play](/img/reinvent-wrap-up/partee.jpg)

I'm tired. I'm really tired, but I just have to tinker around with this one thing I had in mind. Using Fargate, step functions and S3.

**I build it! I run it! And I'm proud of it!**
