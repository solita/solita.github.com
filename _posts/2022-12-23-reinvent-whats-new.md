---
layout: post
title: AWS re:Invent 2022 - What's new in AWS?
author: vjkvir
excerpt: >
  
tags:
  - AWS
  - re:Invent
  - Cloud
  - Conference
  - Workshop
---

![paste](/img/reinvent2022-whats-new/05-reinvent.jpeg)


I had decided to go to re:Invent quite late and wasn’t even a hundred percent sure what was waiting for me there. It was my first re:Invent and first trip to the USA ever. On the other hand, I had read tips n’ tricks for re:Invent but nothing had prepared me for how enormous it is. 

I woke up at 5 am Saturday and traveled to the airport. I was going to fly light (first mistake :D) without checked baggage and so I was quite fast past security checks. After that some coffee and waiting colleagues to arrive. Then we went to the Finnair business lounge for breakfast.

![paste](/img/reinvent2022-whats-new/01-reinvent.jpeg)
*The breakfast was comprehensive and delicious.*

The flight was scheduled to depart at 12:30 but was delayed about an hour and a half. It was good to notice that the breakfast serving had changed to lunch in the lounge. After eating a good meal, it was time to board. The flight went okay watching a couple of movies and listening to some music. It landed a little past 4 pm CST in Dallas. My connection flight was already delayed so it was time for some food again. The connecting flight took off finally at 09:05 PM CST and arrived at Las Vegas at 10:10 PM PST, only a little over two hours late. From the airport, I took a taxi to my hotel and fell into bed around midnight after being awake for roughly 28 hours.

## Sunday 27.11.

Woke up around 8 am and went to get some breakfast. After that, I catch up with colleagues and drove to a near outlet for some shopping. The day went quite quickly there and in the afternoon we drove back. Badge pickup had already opened, so I picked up my badge and hoodie. 

![paste](/img/reinvent2022-whats-new/03-reinvent.jpeg)
*Picking up the badge.*

In the evening Matias booked us a table at Nacho Daddy restaurant. The meals were big and good. I was back at the hotel around 8:30 pm.


## Monday 28.11.

### First conference day!

My first session was a workshop on How to set up Microsoft identity solutions on AWS. It was a rather straightforward thing, but it was impossible to complete the workshop due to the organizer having some capability problems with the Remote Desktop connections. That’s why after reading the material through I went for an early lunch.

The second workshop for the day was Building a monitoring strategy. The theory part was a comprehensive walkthrough of what's included in a monitoring strategy, who needs what kind of information, and when. In the exercise section, there was a sample company from the energy industry which had many IoT sensors producing data. The task was to build a monitoring strategy for that company. 

On Monday evening there was AWS Nordics reception in a restaurant where we could meet other conference attendees from northern Europe. There was good Italian food and some drinks.


## Tuesday 29.11.

Tuesday started with Adam Selipskys Keynote, which I watched from the Content Hub screen stream as I had sessions on Mandalay Bay after that and it would have been a waste of time to travel to Venetian first in the morning just to get back to Mandalay after the keynote. The travel time between Mandalay Bay and Venetian was half an hour at least. Mr. Selipsky’s speech's first theme was sustainability and he said that Amazon is now the world’s largest corporate purchaser of renewable energy and that their goal is to be powering the company with 100% renewable energy by 2025. Furthermore, they are trying to be water-positive by 2030, so they will return more water than they are consuming.

Keynote’s announcements of new services which caught my attention were a **preview of Serverless OpenSearch** and **AWS Graviton 3 processors**. The open search server-less service allows customers to perform, real-time application monitoring, interactive analytics, a website search, and so on without having to worry about configuring, scaling, and provisioning infrastructure. Although the price is quite high as the smallest cluster costs about 690USD/month.

Graviton 3 processors are used in the new C7GN instances, and they offer 25% better computing performance than Graviton 2 while using up to 60% less energy. Graviton is driving better price performance for example Fargate and many other AWS-managed services.

After the keynote, I went to a chalk talk: **Resilient and well-architected applications with chaos engineering (BOA324)**.

AWS Well-Architected is a framework that consists of six pillars – security, liability, operational excellence, performance efficiency, cost optimization, and sustainability. Chaos engineering is the process of stressing an application by creating disruptive events, observing how the system responds, and making improvements. The session focused on the reliability pillar and showed three different architecture examples which could be tested with chaos engineering using the AWS Fault Injection Simulator service. 

![paste](/img/reinvent2022-whats-new/10-reinvent.jpeg)

**Lunchtime!**


With my stomach fulfilled I decided to go watch a breakout session of best practices for advanced serverless developers (SVS401) by Julian Wood from Content Hubs Overflow screen. The talk consisted of six sections and was very interesting. You can watch it from [here](https://s12d.com/svs401-22) but here are some best practices that I noticed. 

![paste](/img/reinvent2022-whats-new/12-reinvent.jpeg)


He started the session by explaining the meaning of serverless. We should think of it as a mindset and should focus on business value, rather than enabling technology. Furthermore, we should concentrate on the flow of data and events which leads us to event-driven architecture. 

Another pick was handling event state. As Dave Boyne, the AWS Serverless Developer Advocate once said Events are the language of serverless applications. That’s why asynchronous and eventual consistency should be embraced. Also, you could enrich events with content and metadata and pass the state as events. 

The third pick comes from the fabulous functions part. When using lambdas we should optimize cold starts by lazy initializing shared libraries, loading only the needed dependencies, and connecting functions to VPC only when those are needed.

Next, I had a workshop with the title **Become a network support expert: We break it, you fix it (NET307-R)**. There were six tasks to complete, each of them having a little different problem. The CloudWatch Dashboard worked as the playground from where you could see if the task was completed or not. The problems were quite small, like why an IoT Breaker from a public subnet couldn’t connect to IoT Backend in a private subnet in the same VPC. To investigate these problems, the workshop gave some nice AWS services which I hadn’t heard of before like, VPC Network Access Analyzer and VPC Reachability Analyzer. The fix for this was to add the right port range from the public subnet to the private subnet’s inbound rules.

In the evening there was the **AWS EMEA reception** in a nearby hotel’s ballroom. Again, there were good food, drinks, and good conversations. As the day had been quite long, I called it a night around 9 pm and walked to Mandalay Bay. I must say, the Strip is long and wide and it doesn’t sleep! :D

![paste](/img/reinvent2022-whats-new/14-reinvent.jpeg)
*The venue was divided into sections.*


## Wednesday 30.11.

Woke up early and ate a good breakfast before heading to the first workshop of the day: **Ship securely: Automated security testing for developers (SEC307).** My expectations were quite high based on the introduction text in session booking. The first thing to do was set up the environment by configuring CDK and deploying the pipeline and the needed tools in the pipeline. The demo environment used SonarQube, pip-audit, and license check in different phases. There was also a little react frontend app and using it you were able to test and understand some of OWASP's Top 10 vulnerabilities. After that, one was able to see them in SonarQube and fix them in the environment. Pip-audit showed the problems in demo application dependencies. In total, the workshop didn’t give me as much as I had thought. It was still a nice experience!

My next session after lunch was **Design and build modern mobile apps (ARC302)**, but before heading there I had some spare time and went to listen to a breakout session with the title **A closer look at AWS Lambda (SVS404)** from Overflow screen. It was interesting deep dive into how lambdas work under the hood. You can watch it [here](https://www.youtube.com/watch?v=0_jfH6qijVY).

The workshop of Design and build modern mobile apps consisted of building a newsfeed social media app using React Native, Expo, and AWS Amplify. I hadn’t used Amplify before, but it turned out to be a fast and intuitive tool to use. Also, I noticed that I was familiar with the other tools and frameworks in the workshop, so I didn’t get much new.

My last session for Wednesday was a workshop on AWS CDK: **Develop AWS CDK resources to deploy your applications on AWS (DOP309)**. Again, my expectations were high but unfortunately, those weren’t met in this session either. The instructors started by explaining what is AWS CDK and how to use it. After that, the hands-on tasks were to implement a simple lambda stack and a CloudFront stack. Well, I did the exercises and left early, as there wasn’t anything to do anymore. 

I also visited the Expo on Monday and Tuesday but decided to take a small round before heading to buy a suitcase and some souvenirs. After three hours, I collected couple more swags from the expo, bought many souvenirs, and finally found a suitable suitcase.

![paste](/img/reinvent2022-whats-new/16-reinvent.jpeg)

I took an uber back to the hotel and fetched some food from McDonald's. At eight pm I was so tired that I decided to go to bed.


## Thursday 1.12.

The second last conference day! I woke up a little too late to attend Dr. Werner Vogels Keynote in the Venetian so I walked to breakfast in the Mandalay Bay and watched the keynote from the Content Hub screen.

The keynote started with a characteristically hilarious Matrix spoof but pivoted soon to the complex and asynchronous nature of our daily life and why we should be aiming to replicate that asynchronicity into the systems we build. Dr. Vogels' thesis was that synchronous, one-by-one systems result in something as simple as a bowl of fries reduced to each fry being individually sliced, fried, and placed into a bowl. That, of course, is very inefficient and leaves the consumer underwhelmed by the cold results. Vogels wanted to point out that whilst asynchronous systems may look much more complex and daunting than ordered, synchronous systems; the result is usually much more composable, robust, and resilient because we can change individual components without breaking the whole system.


Vogels made a couple of service announcements and what I picked up is **AWS Step Functions Distributed Map**, **Amazon EventBridge Pipes**, **AWS Application Composer**, and **Amazon Code Catalyst**. 
First, the step functions are a simple way to iterate objects through steps in an easy-to-use workflow but when we add distributed mode for the Map state, we can run thousands of parallel workflows to be spawned based on object updates in S3.

**Amazon EventBridge Pipes** enables a simple and reliable way to create point-to-point integrations among many sources while customizing starting position, batching, and concurrency, and then filtering your data.

**AWS Application Composer** is a visual canvas for architecting, configuring, and building serverless application stacks. It allows you to use existing Cloud Formation and SAM templates.

**AWS Code Catalyst** is a unified software development service that allows teams to speed up the development process by offering templates for different types of frameworks. It creates pipelines, repositories, infrastructure, and services from blueprints so the team can focus on accelerating the enhancement of their application.
I recommend watching the keynote, it’s worth it!

Next, I had quick lunch before heading to a workshop. The lunch began at 11 am but the doors opened about ten minutes early, I walked apace inside and suddenly I noticed that I was leading the group because all other were walking so slowly. I was quite surprised when all waiters and waitresses started to clap and hooray me when I walked past. I should have taken on a video of the situation. :D Nevertheless, the food was good again!

The workshop on **Build smart camera applications using Amazon Kinesis Video Streams WebRTC (IOT309-R)** sounded interesting, but as there weren’t any real camera devices to play with like RPi, a recorded sample video had to be used as an example. I must say that I didn’t get much out of it, but the idea behind was clever and I would say WebRTC with Amazon Kinesis is worth testing. 

I somehow managed to do a little double booking from 2 pm to 5 pm as I had two workshops on my calendar. As the first one’s topic contained Amplify, I decided to go to the first one for the start and move to the another one at 2:30 pm. 
**Build a cross-platform mobile app in Flutter with AWS Amplify (FWM307)** workshop gave me a brief introduction to the Flutter framework and reviewed how Amplify works, but that’s about it. So, I did the exercises and left for my last workshop at the conference.


**AWS DeepRacer: Get hands-on with machine learning (DPR202)** was very interesting. Although the concept of DeepRacer is already a couple of years old, it was new to me. AWS DeepRacer is a cloud-based 3D racing simulator, a fully autonomous 1/18th scale race car driven by reinforcement learning, and a global racing league. Every participant got 30$ voucher for the workshop to be able to create the first model and run the first iterations of simulations.

You can read more about the DeepRacer [here](https://aws.amazon.com/deepracer/).

After the workshop, I had time to visit my hotel to take the backpack there as the evening was reserved for **re:Play party**, and the backpacks weren’t allowed there. I caught a shuttle bus from Mandalay Bay to the Venetian and did a quick tour of the Bellagio’s botanical garden on my way back to the Venetian, I also watched the Bellagio Fountain water show.

![paste](/img/reinvent2022-whats-new/21-reinvent.jpeg)
*A view from Bellagio's botanical garden.*


### Time to re:Play

Busses left from Venetian quite quickly after 7 pm but the arriving and getting out of the bus in the Festival Grounds was a mess and took very long. Looked like I had had a bit of good luck with getting on a bus because later I heard my colleagues had waited about half an hour for a bus to arrive and pick them up. 

![paste](/img/reinvent2022-whats-new/23-reinvent.jpeg)

The area was outside with large tents, multiple food & drink pick-up points, DJs playing, and also a silent disco where you could put noise-canceling headphones on and enjoy. Food options consisted at least of chicken wings, hotdogs, and small pulled pork hamburgers. The main artist was Martin Garrix. We listened to a couple of songs but then decided to head back to the hotel. After all, it had been a long day.


## Friday 2.12.

The last day of the conference. I had a couple of sessions about Code Catalyst booked. Those gave a good hands-on introduction to the service. I can see the potential in it but I’m still a little paranoid concerning the security aspect of this kind of service. Final thing was to catch the last slides and summary of the introduction to the new **AWS VPC Lattice**. 

**Amazon VPC Lattice** helps you to improve productivity by offering an application layer service that consistently monitors, connects, and secures communications between your services. Defining policies for monitoring, network access, and traffic management to connect compute services is simple regardless of whether you use instances, containers, or serverless.


It was lunchtime and we went to a nearby BBQ restaurant with my colleagues. The afternoon went by doing some last-minute shopping and walking around the Strip. Around four we separated and I walked to the second hotel of my trip. 

I had to check out from Mandalay Bay on Friday morning because they hadn’t had spare rooms for me anymore and that’s why I had booked another hotel room from the Mardi Gras. Thankfully, I was able to leave my luggage at the Mandalay Bay Bell desk as it was nearer to the airport than the Mardi Gras. I must say the difference between these two hotels and the rooms was quite big. 
 

## Saturday 3.12 and journey home
Time to fly home! Or... maybe not yet.

I woke up around 8 am and after a shower and checking out, I took an uber to Mandalay Bay. I had plenty of time because my flight was scheduled to leave at 5:31 pm. 

I’m a volunteer firefighter and I have a habit of visiting different fire stations while traveling. This time the nearest one was only a five-minute walk away from Mandalay Bay so I walked there and knocked on the door. I was lucky, the fire-persons at that station didn’t have an alarm and they were happy to show me around the station and vehicles. 

![paste](/img/reinvent2022-whats-new/25-reinvent.jpeg)
*In Clark County Fire Department some cars are yellow and not red*


![paste](/img/reinvent2022-whats-new/26-reinvent.jpeg)
*Got also a chance to test the equipment.*

After the tour, it was my turn to introduce our vehicles and rescue services in Finland. They asked me if I would like to have a t-shirt, I should go to the other station nearby because this station had run out of them. So I thanked them, took again an uber and went to visit the other station. 

![paste](/img/reinvent2022-whats-new/27-reinvent.jpeg)
*I wasn't the first nor the last one to visit station number 32.*

After fetching the t-shirts, it was time to head to the airport. I was greatly surprised when I printed my boarding passes saying my flight was tomorrow and not through Los Angeles and London but through Dallas! Well, going to the desk and it turned out the London flight was delayed and the system had rebooked me automatically. Unfortunately, they didn’t have any hotel rooms available in Vegas so they flew me to Dallas. 

After one more night in the USA, I was ready to board a plane at 5 pm. I was lucky to get some sleep on the plane and landed in Helsinki at 11 am on Monday. Finally, I was home around 3 pm.


## Some thoughts afterward and keeping in mind.

* Everything is big in the USA.
* The conference has many good sessions but maybe should concentrate on 300- and 400-level things. 
* Read properly the introduction of the session before booking it. 
* Finally don’t go light and take an empty checked bag with you. 


## Links
If you want to read up on previous re:invent blogs and see how they compared, here's a list:
* [2017](https://dev.solita.fi/2017/12/01/AWS-reinvent-wrap-up.html)
* [2018](https://dev.solita.fi/2018/12/21/reinvent-2018-first-timer.html)
* [2019](https://dev.solita.fi/2018/12/21/reinvent-2018-first-timer.html)

If you want to see all top announcements from re:Invent, that can be found [here](https://aws.amazon.com/blogs/aws/top-announcements-of-aws-reinvent-2022/).

