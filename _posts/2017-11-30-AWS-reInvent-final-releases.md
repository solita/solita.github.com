---
layout: post
title: Werner Vogel's keynote on Thursday at re:Invent 2017 focused more on customer use cases, but included also some new service releases
author: kimmokantojarvi 
excerpt: After yesterday's long list of exciting releases today was little smaller event in terms of new releases. I will though go through shortly all new releases.    
tags:
- AWS
- re:Invent
---

My previous posts about the releases earlier this week are available here:
- [New releases on Monday and Tuesday](/2017/11/28/AWS-reInvent-first-announcements.html) 
- [New releases on Wednesday](/2017/11/29/AWS-reInvent-more-great-news.html) 

![Reinvent](/img/aws/reinvent_2017_5.jpg)

## Werner Vogels show
Last keynote on Thursday morning was hosted by Werner Vogels, Chief Technology Officer of AWS. Venue was this time MGM Grand Garden Arena and as expected it was crowded with people and excitement. Instead of many releases today's keynote was more about customer cases explaining the use of AWS services for different business cases. We got to see how Netflix chaos engineering works or how Heed is improving sports experience with sensor-based analytics. 

![Reinvent](/img/aws/reinvent_2017_6.jpeg)

Here are the highlights of new releases announced in the keynote.

### Compute

The release of new IDE for developing serverless applications and infrastructure was not anticipated, but it will be interesting to see the use cases for [Cloud9](https://aws.amazon.com/blogs/aws/aws-cloud9-cloud-developer-environments/) IDE. It is based on the acquired company Cloud9 from 2016. The demo seen in the keynote focused on the pair programming capabilities and easiness of test and deployment pipeline. Most probably this will be initially used for developing serverless/Lambda applications.

In addition, the whole [Lambda user interface has been enhanced](https://aws.amazon.com/about-aws/whats-new/2017/11/aws-lambda-introduces-enhanced-console-experience/) in order to better integrate with other new AWS services (e.g. serverless application repository). 

Lambda service was improved with the increase of maximum Lambda memory to 3GB and it also now supports Go language.

Really anticipated smaller release was the announcement of allowing to integrate [API Gateway into VPC](https://aws.amazon.com/about-aws/whats-new/2017/11/amazon-api-gateway-supports-endpoint-integrations-with-private-vpcs/) without exposing the APIs anymore to internet. This is a great extension to API Gateway and will probably boost the use of API Gateway. We've seen some customers avoiding API Gateway for internal use because it is exposing APIs to internet. 

Amazon is really trying to boost the growth of serverless applications with the launch of [Serverless Application Repository](https://aws.amazon.com/blogs/aws/aws-serverless-app-repo/). The key idea is to allow people to create and share applications fulfilling common use cases instead of copy-pasting same applications from account to account or project to project. Applications can be totally private or granted with gross-account access or totally public. So at the same time this will be a kind of public open source marketplace for serverless applications. 

### Alexa

[Alexa for Business](https://aws.amazon.com/blogs/aws/launch-announcing-alexa-for-business-using-amazon-alexas-voice-enabled-devices-for-workplaces/) is an extension to the current Alexa family allowing voice interaction at work. Basically it is voice interface for querying all kinds of business information such as meeting times and executing simple actions such as booking new meetings and creating phone calls. The challenge in the beginning is probably the limited list of partners and solutions that are supporting Alexa for Business. That said it will be interesting see how the automation will change our behaviour in the future. 

<img src="/img/aws/reinvent_2017_4.jpg" alt="Las Vegas casino world" style="height: 350px;"/>

### Summary
All the new releases will be listed also in [Amazon re:Invent website](https://aws.amazon.com/new/reinvent/) and [Amazon blogs site](https://aws.amazon.com/blogs/aws/)

