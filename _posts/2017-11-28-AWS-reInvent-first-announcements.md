---
layout: post
title: First major service announcements in AWS re:Invent 2017
author: kimmokantojarvi 
excerpt: There seems to be coming out so many new releases this year's AWS re:Invent that it feels like pre-Christmas. I will be covering the first major releases in this post. 
tags:
- AWS
- re:Invent
- AmazonMQ
- Amazon Sumerian
- AWS Elemental
- AWS AppSync
- PrivateLink
- Amazon GuardDuty
---

## About re:Invent 2017
This year re:Invent is bigger than ever. The whole event has spread throughout Las Vegas strip between MGM Grand and Encore hotels. Biggest venues this year are Venetian, MGM Grand and Aria. It is clear from the city streets that Vegas is packed with 40 000 AWS enthusiasts. 


![Reinvent](/img/aws/reinvent_2017.jpeg)

I thought I would start from the total new service areas into which Amazon is now entering with these new releases.

## New service areas

### Media services
AWS Elemental service is based on the acquisition of Elemental Technologies Inc. few years back and in that sense is not so surprising news. Elemental service is aimed for organisations in publishing and broadcasting industry that are not interested of investing heavy amounts of money just for broadcasting capabilities. Like any other PaaS service it will ease up the entry into video streaming business for anyone interested.

In my mind the most interesting capabilities of Elemental service are related to live-video streaming in general but also to the idea of targeted advertising for video streams. What it means is that basically anyone can start creating commercial-grade video content and make money out of it with advertising. 

More details about the different components of the Elemental service is available from these links:
- [AWS Elemental MediaConvert](https://aws.amazon.com/blogs/aws/aws-media-services-process-store-and-monetize-cloud-based-video/)
- [AWS Elemental MediaPackage](https://aws.amazon.com/blogs/aws/aws-media-services-process-store-and-monetize-cloud-based-video/)
- [AWS Elemental MediaStore](https://aws.amazon.com/blogs/aws/aws-media-services-process-store-and-monetize-cloud-based-video/)
- [AWS Elemental MediaLive](https://aws.amazon.com/blogs/aws/aws-media-services-process-store-and-monetize-cloud-based-video/)
- [AWS Elemental MediaTailor](https://aws.amazon.com/blogs/aws/aws-media-services-process-store-and-monetize-cloud-based-video/)


### AR & VR
With the preview [release of Amazon Sumerian](https://aws.amazon.com/blogs/aws/launch-presenting-amazon-sumerian/) AWS steps into the AR & VR world. It seems that in the beginning this will be mostly used for providing human nature interfaces for Amazon Polly and Lex services. Of course in the future its use will probably expand to other generic virtual reality use cases. 

![Sumerian](https://media.amazonwebservices.com/blog/2017/Sumerian-01-HeaderPic.png)

## Existing service areas

### Application integration
Amazon is proud about how well its SQS and SNS services are scaling for example for their own needs ([Prime Day powered by AWS](https://aws.amazon.com/blogs/aws/prime-day-2017-powered-by-aws/)). But because many enterprise customers have already existing queue and messaging services in use Amazon decided to launch [Amazon MQ service](https://aws.amazon.com/blogs/aws/amazon-mq-managed-message-broker-service-for-activemq/) which is basically packaged Apache ActiveMQ service. They don't even try to present it as something else. This will allow customers to migrate their workflows more easily into cloud. At least in the beginning the service is not going to be scaling automatically and thus customers need to select the type and size of instances to match their performance requirements. 



### Compute
In compute services new M5 instance generation was released together with totally new H1 instances which are intended for big data processing and those instances will include very large storages with high I/O.

Another very interesting news was the release of bare metal instances which basically expose the hardware directly to any software. This is very handy for cases in which virtualized environments can't be used due to licensing restrictions for example. 

Regarding spot instances new releases were hibernation support and changes to spot pricing. The major change in spot pricing is that the prices will be changing more gradually giving more predictable prices. 

### Mobile services
New [AppSync service](https://aws.amazon.com/blogs/aws/introducing-amazon-appsync/) released in preview is basically managed GraphQL environment for mobile applications. With AppSync building collaborative mobile and web applications will be faster and easier. 

### Networking and content delivery
One of the biggest hurdle for many enterprise customers has been so far the difference in network security between on-premise data centers and public clouds. Now with the [release of PrivateLink](https://aws.amazon.com/about-aws/whats-new/2017/11/aws-privatelink-now-available-for-customer-and-partner-services/) customers can more securely access all AWS services as if they were services inside their on-premise network. On the other hand it allows also exposing on-premise services directly into AWS. In practice one could for example expose CRM as a one service and all the different AWS accounts for this customer could use the same service in network level. PrivateLink allows also companies to create and publish commercial services in MarketPlace. 

The release of PrivateLink will definitely be a major game changer for enterprise customer cloud adaptation. 

### Security
Amazon [GuardDuty](https://aws.amazon.com/blogs/aws/amazon-guardduty-continuous-security-monitoring-threat-detection/) is one additional service to increase automatically your AWS environment security. The idea of GuardDuty is that it monitors multiple security streams to automatically detect malicious IP addresses, devious domains, and learning to identify malicious behavior in your AWS accounts. GuardDuty reads data from CloudTrail, VPC Flow and DNS logs. 

GuardDuty operates in own infrastructure separate of your account and the findings of GuardDuty are presented as a separate log or as CloudWatch events so that issues can be addressed automatically. 

### Summary
All the new releases will be listed also in [Amazon website](https://aws.amazon.com/new/reinvent/)


![Reinvent](/img/aws/reinvent_2017_2.jpeg)