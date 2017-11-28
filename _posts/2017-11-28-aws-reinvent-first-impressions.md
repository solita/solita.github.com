---
layout: post
title: Re:Invent 2017 first impressions
author: arto
excerpt: Attending AWS Re:Invent for the first time - first impressions
tags: 
- AWS
- Re:Invent
- Cloud
- DevOps
- SecOps
- VR
---
Fuck the desert. I'm sure something along this line was what founders of Las Vegas said when they started building. Whole city is extravagant show of pompousness and contradictions. Of course, you need to build huge pools in middle of a desert, where water is scarce. Of course, you push neon signs everywhere and build theme parks and distractions so much that at night-time you feel you are living in Blade Runner world. Except, you know, the rain.

![Reinvent](/img/aws-reinvent-first-impressions/reinvent.jpg)

This is the setting where more than 40 000 AWS cloud geeks made a pilgrimage this year, to attend AWS Re:Invent conference, biggest so far. One week of craziness, so much information to absorb, so much logistical challenges to solve, so many people. Perhaps too big, events happened at conference hotels at relatively long distances - so travel alone took somewhere between 30-60 minutes to change from location to another. And queues were crazy. But in the end, I'd say - all worth the pain.

I've been with AWS cloud for a long time, but as a hands-on software craftsman, I had mainly been playing with the EC2 and IAM, before I came to Solita. When I started here, I got a glimpse of what data and analytics guys were doing, and a new world opened to me. I had not realized how much AWS has been scaling out in services during these few last years. Right now, it's actually pretty stupid to treat AWS as a rent-a-server company. You should truly not be dealing with servers these days. Not if you want to be really cost-effective and truly scalable. There's so much more building blocks to use and abuse now. It's not only about scaling up and out and optimizing massive costs. It's also about efficient and agile start-ups, experiments, and POCs, that are cheap to do. And we do a lot of those, too.

## What's new?

The conference will continue for few more days, and the keynotes are just ahead. I'm sure there will be big news coming up. But there were some interesting announcements already. For example Amazon Sumerian, a new Virtual Reality/Augmented Reality building kit that AWS provides. It looks to me a lot like Unity and Mapbox, but it's something I've already been playing with a bit, right now it's a hype and I see a lot of potential. It was a bit surprising opening, but when AWS puts their muscle in it, I expect to see something exciting. So yeah, Oculus Rift, HTC Vive, and many other devices are getting some VR boost. I've been working a lot on location services lately, so my mind is on a virtual map, and what I could do with that.

![Flamingo](/img/aws-reinvent-first-impressions/flamingo.jpg)

Another thing that caught my eye was a lot of talk on Devops and Secops, and automation, which I'm very passionate about. No new services or product names, just best practices on how to let them do your work for you. I believe you should be automating your security response. It's 2017, not 1997. I saw pretty cool Devops models that expanded some models I've seen with also automated QA and automated feedback from operations to feed the development. Things like GDPR would benefit greatly from automated security policies, for example to protect S3 buckets from security misconfiguration. Not that it would ever happen to you... (see the links section at end)

## Automating security

Does a Lambda replace your security team? Of course not, but it would be utterly stupid not to leverage it to get faster responses to expected threats, faster automated healing in case of for example DDOS attack. Instead of requiring puny humans to offer 24-hour support and react in minutes in the middle of the night, how about let the Lambdas do that? Manual response is in many cases already way too late to help.

Speaking of DDOS attacks, I expect them to become more and more common these days, and AWS has a lot of options to shield against them. And there will be more. Goal is a no-op security, something you would just automatically get. We are not there yet, but there's a lot you can leverage as basis, and then more you can manually add on top of that. To survive a DDOS attack, you simply need to stop the easily detected threats at the front gates, then be able to scale in many directions for the more sophisticated ones. And only cloud can really do that for you.

![Lambda as secops team](/img/aws-reinvent-first-impressions/secops.jpg)

There was also a something new for handling with videos, AWS Media Services, which includes AWS Elemental Media Storage. This is not in the core of what I typically need but nice to know the options, you never know when there might be a project that requires them. And, of course, thinking locally, Helsinki now has both Direct Connect capabilities (published earlier this month), and is also a CloudFront Edge Location. We are getting faster access to information highways and services.

So, only after few days here I'm feeling exhausted, but at the same time invigorated, recharged by the energy and ideas I've experienced. Cloud is right now the place where things happen, and as the crafters who help mould it to fulfil peoples dreams of digitalization, we are responsible of doing things the right way. Can't wait to see what I'll learn here during few more days. There will be more blogs by my colleagues to cover different viewpoints later on.

## Links:

*Sumerian VR/AR*
[https://aws.amazon.com/sumerian/](https://aws.amazon.com/sumerian/)

*Cloudfront edge locations, Directconnect new locations*
[https://aws.amazon.com/about-aws/whats-new/2017/11/cloudfront-adds-six-new-edge-locations/](https://aws.amazon.com/about-aws/whats-new/2017/11/cloudfront-adds-six-new-edge-locations/)
[https://aws.amazon.com/about-aws/whats-new/2017/11/aws-direct-connect-added-five-new-locations-today-in-denver-phoenix-madrid-helsinki-and-chennai/](https://aws.amazon.com/about-aws/whats-new/2017/11/aws-direct-connect-added-five-new-locations-today-in-denver-phoenix-madrid-helsinki-and-chennai/)

*Amazon Mediastore*
[https://aws.amazon.com/mediastore/](https://aws.amazon.com/mediastore/)

*S3 breaches*
[https://cloudmatters.wordpress.com/2017/11/27/whats-going-on-with-these-high-profile-aws-s3-breaches/](https://cloudmatters.wordpress.com/2017/11/27/whats-going-on-with-these-high-profile-aws-s3-breaches/)



