---
layout: post
title: re:Cap of the AWS re:Inforce 2019
author: mkainula
excerpt: Summary of the first ever cloud security focused AWS event held in Boston
tags:
- AWS
- re:Inforce
---

This year, re:Invent is not the only big official AWS conference organized. Earlier in June re:Mars focusing on machine learning and artificial intelligence was held in Las Vegas and last week a cloud security focused re:Inforce was held in Boston.

Even though the event was not completely sold out, the scale of things was still quite big, with over 8000 participants attending and over 200 breakout sessions to choose from during the two day conference. There were a lot of different types of sessions available for different type of audiences, all the way from CISOs to security engineers and also for software developers.

The event was held in Boston Convention & Exhibition Center, which is a giant expo hall with many levels. In the middle of the hall, you had a "Security Learning Hub" which was basically an exhibition area for partners. Despite the fact that you didn’t need to change venues like in re:Invent, you still had to walk quite a lot during the days and getting from one end of the convention center to the other took some time.

![Security Learning Hub](/img/reinforce-2019-recap/security-learning-hub.jpg)

If you had been to re:Invent before, everything seemed quite familiar. Unfortunately this also applied to the registration process for the sessions. Before the reserved seating registration opened, you had no way to view the sessions you were interested in a calendar view. Luckily [the same handy tool someone had made for re:Invent planning](http://reinvent-planner.aws.carlosesilva.com) also worked for re:Inforce with slight modifications, and because you only had 200 sessions to choose from instead of 2000, fitting the sessions into your calendar was also much easier. Also, you didn't need to worry about if you had enough time to travel between venues during the day, which was a huge plus as now you could actually select the sessions from everything available instead of just the ones located in the venue your previous or next session was going to be, like in re:Invent. Once the registration and reserved seating was done, everything on-site worked smoothly and everything was well organized, just like in re:Invent.

 All the different breakout session types were also similar to the ones in re:Invent. Regular sessions were an hour long talks with a short Q&A in the end, chalk talks were shorter talks with more time dedicated to Q&A or a demo, workshops were 2 hour long hands-on labs where you could solve problems on your own or as a group in a table, and builders sessions were an hour long hands-on "mini-workshops" with just 5 other people and an AWS expert. This time, I wanted to focus on hands on learning by going into many workshops, builders sessions and also to the four hour long security jam hackathon on the second day.

Here are some short recaps on the different sessions that I attended.

# Day 1

## [Keynote by Stephen E. Schmidt, VP and CISO of AWS](https://www.youtube.com/watch?v=FKphJNfpWk8)

Not that many new announcements were made during the keynote, as the biggest announcements (Security Hub general availability) were already published before the keynote. It was still a decent overview of the current state of security in the cloud, how it has evolved and how it will evolve in the future (more automation and machine learning). The customer stories of big banks and insurance companies going all in on cloud and building and releasing their own security related tools and products were also a bit surprising to hear.

![Keynote](/img/reinforce-2019-recap/day1-keynote.jpg)

## [SDD334-L Leadership session: Security deep dive](https://www.youtube.com/watch?v=Yf80_hCue_Y)
This session turned out to be a bit of a "hand waving" talk instead of a technical deep dive I was hoping it to be. Some traits of successful customer stories around security and primitives of speed, culture and leadership were discussed, highlighting privacy and how to embed security into engineering. Had to leave a bit early to get into the next session.

![SDD334](/img/reinforce-2019-recap/day1-sdd334.jpg)

## [SDD306 - Securing serverless and container services](https://www.youtube.com/watch?v=kmSdyN9qiXY)
A session with a pretty good overview of the security features available in different layers of serverless and container services, focusing on compute services (Lambda, Fargate ECS, EKS). The talk finished with an example of integrating security testing steps into CodePipeline using Lambdas.

![SDD306](/img/reinforce-2019-recap/day1-sdd306.jpg)

## SDD323 - Automating remediation of noncompliant configurations
A builders session focused on using AWS Config and creating a Lambda function for remediating configuration errors (e.g. a non-compliant S3 bucket policy). [Link to materials](https://sdd323-r-reinforce-2019.s3.amazonaws.com/automating-remediation-of-noncompliant-configurations.pdf)

![SDD323](/img/reinforce-2019-recap/day1-sdd323.jpg)

## SDD310 - DevSecOps: Integrating security into pipelines
A pretty nice workshop with a long introduction to the topic, also with some interaction with attendees. After the long introduction, the workshop finished with a small lab for adding a Lambda function into an existing CodePipeline setup that checked if the built code contained any AWS credentials. [Link to materials](http://tinyurl.com/yx9yuhxg) with some nice slides on DevSecOps.

![SDD310](/img/reinforce-2019-recap/day1-sdd310.jpg)

After the first day, there were numerous unofficial after parties or happy hour events sponsored by companies at nearby restaurants. Those were again great for meeting new people and hearing how companies are using AWS.

# Day 2

## Jam Lounge
In last years re:Invent, I stumbled across the jam lounge only on the final day. Basically the idea was that you could register to a website where you could complete different AWS related challenges during the event and compete for prizes. This time, I found the lounge early on the first day, so I wanted to see if I could compete for the top prizes.

After the first day, I had already solved 4 of the 5 available daily challenges and had some issues launching the fifth challenge. Luckily with some help from the Jam lounge personnel early on the second day, I was able to get it working.

I started to do the second day's challenges right after they were released and had some extra time to work on them during a workshop while waiting for Cloudformation stacks to finish creating. The challenges were surprisingly easy, so I managed to complete them all during the workshop and was the first one to finish all of them and won the first prize (Bose QC35 headphones)!

![Jam lounge](/img/reinforce-2019-recap/day2-jamlounge.jpg)

There was also a separate Capture the Flag event going on with a focus on more traditional security challenges (decrypting messages, binary investigation etc.) but I decided to focus on the AWS related challenges in the jam.

## SDD403 - Building secure APIs in the cloud
First workshop of the second day started at 8AM and focused on the security features available in API Gateway. It was interesting to learn more about them, as I haven't used the service that much. After creating a API Gateway from scratch, we added schema validation, VPC link, attached a WAF with some SQL injection and body size rules and Cognito authorization to it. [Link to materials](http://workshop.reinforce.awsdemo.me/)

![SDD403](/img/reinforce-2019-recap/day2-sdd403.jpg)

## SDD324 Setting up a DevSecOps pipeline to automate vulnerability scanning of Docker images
A builders session where most of the one hour's time was used waiting for CloudFormation to create stacks. CoreOS Clair and Klar were used for scanning Docker images for known vulnerabilities and added as a step to a CodePipeline setup. [Link to materials](https://github.com/aws-samples/aws-codepipeline-docker-vulnerability-scan)

![SDD324](/img/reinforce-2019-recap/day2-sdd324.jpg)

## SEJ-001 - Security Jam
This "hackathon" was a bit different compared to re:Invent's Game Day. This was basically similar to the security jam lounge, you had 9 different challenges that you tried to solve as a team in 4 hours. The topics in the challenges were quite varying, everything from IAM to IoT to API Gateway was used. Quite an intense session, luckily I had some talented people in my team so we managed to get 8 of the 9 challenges done and got the first place! We were also the first team to solve a sponsored challenge so we also won some Trend Micro swag and Amazon.com giftcards.

![SEJ-001](/img/reinforce-2019-recap/day2-securityjam.jpg)

## SDD-326 Security best practices for Amazon EKS
Another builders session where one hour was clearly a too short time. Setting up an EKS cluster and tooling from scratch via Cloudformation took almost the whole time, so we didn't get to the actual point of the session (using IAM credentials for controlling access to pods). [Link to materials](https://github.com/meyjames/EKSKube2IAM)

![SDD-326](/img/reinforce-2019-recap/day2-sdd326.jpg)

## Closing reception

After the second day, there was an official closing reception just outside the conference center with plenty of outdoor games, music, food, drinks and a chill atmosphere.

![Closing party](/img/reinforce-2019-recap/closingreception.jpg)

# Conclusion

Overall, everything was well organized and a lot of interesting stuff was happening. Two days almost felt too short for an event like this, as they could've easily had more repeats of the sessions and run the event for a third day. A lot of hands on learning this time around, as I tried to choose many workshops and builders session. I learned a lot about some AWS services that I haven't used that much in my projects during these two days. Hackathons and jams were again perhaps the highlight.

![A Cloud Guru](/img/reinforce-2019-recap/cloudguru.jpg)

Was the event worth attending? Well, obviously you aren’t going to get quite as much and as varied topics in a two day conference as you would in a week long re:Invent. But still, security is such an integral part of pretty much everything that AWS does, so it was actually quite interesting to look at all the services from a different viewpoint than you would perhaps normally look at them. From new announcements point of view, the event was quite lackluster, but perhaps they are saving some feature or product announcements for re:Invent.

![History](/img/reinforce-2019-recap/history.jpg)

Next year, re:Inforce will be held in Houston, Texas on June 16th and 17th.