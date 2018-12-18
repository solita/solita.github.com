---
layout: post
title: AWS re:Invent 2018 through the eyes of a first timer
author: mkainula
excerpt: AWS re:Invent is the biggest AWS related conference in the world, and this year our company sent 15 people to Las Vegas to learn about the new features, best practices and different use cases of AWS and to network with customers and other AWS experts around the world. This blog post is a summary of the week from the viewpoint of a first timer. For other re:Invent related blog posts, keep an eye out for upcoming posts in this blog and our social media channels.
tags:
- aws
- reinvent
---

![Welcome to re:Invent](/img/reinvent-2018-first-timer/welcome.jpg)

AWS re:Invent is the biggest AWS related conference in the world, and this year our company sent 15 people to Las Vegas to learn about the new features, best practices and different use cases of AWS and to network with customers and other AWS experts around the world. This blog post is a summary of the week from the viewpoint of a first timer. For other re:Invent related blog posts, keep an eye out for upcoming posts in this blog and our social media channels.

# Introduction

This blog post is a summary of the re:Invent week from the viewpoint of a first timer. I work as a Data Developer at Solita and I’ve been using AWS in my work for almost 3 years now, and I’m also a Certified Solutions Architect - Professional. After watching all the big announcements and some of the sessions from previous years online, I made a goal for myself to someday be at re:Invent in person, and luckily this year everything worked out. 

I’ve visited some software development conferences before, but they have all been really small compared to the massive scale of re:Invent. With over 50 000 participants, 2500 sessions to choose from and five days full of content, the scale of things is just huge and there is so much variety in the topics, types and levels of the sessions.

I tried to choose sessions and workshops from quite varying topics, as the project I’m working on consists of a lot of different things (software development, event pipelines, data platform, serverless, infrastructure as code, devops, data science, machine learning, you name it…) that we are doing with a small team. I tried to mix and match sessions with some technologies that we are already using and some that we are considering of taking into use, while also trying to learn about the newly announced features.

## Registration and scheduling

The user experience of registering to the different sessions was quite poor. The website that you had to use for reserving a seat for the sessions could’ve used a lot of work to make it easier to find sessions and to make a schedule that made sense in a logistical point of view. Before the registration opened, you could add sessions from the catalog to your interests, but you had no way of viewing a calendar of your interests without a third party website. With over 2500 sessions to choose from, searching and filtering options are very important and although the provided options were decent, you could still end up too easily in a situation where you had a bunch of different sessions back-to-back starting at the other ends of the campus. The overflow and repeat sessions were also added quite late, so you had to do quite a lot of tweaking after the initial registration to make the schedule work in practice. The schedule feature of the webapp and the planner of the mobile app worked much better for this, but the app was only made available about one week before the event, when most of the sessions were already fully booked.

One thing to keep in mind is that all of the session videos are going to be posted on Youtube a few days after the event, so you should focus on going to workshops, chalk talks and builders sessions if you want to make the most out of the things that aren't available later on.

## Preparing for the trip

There were a bunch of blog posts with all sorts of tips and tricks from previous years, and they were quite helpful in preparing for the trip. The most important one was to leave enough time for transportation between venues, and I can’t stress that enough. Even though the venues can be across the street from each other, the actual locations of the sessions can be very far away from each other, as the event/convention centers are usually a long walk away from the main entrance.

# Notes from the sessions

Here are some quick notes of the sessions I went to, so you can decide whether to check them out on Youtube or Slideshare later.

## Day 1

### Session: ANT322 - High Performance Data Streaming with Amazon Kinesis: Best Practices

Quick overview of different Kinesis features, then focusing more on how to achieve better scaling performance, consistency and latency using enhanced fan-out streams where consumers subscribe to a shard and messages are pushed to them instead of standard method of the consumer periodically pulling records from a shard. 

Case example of NICE inContact which provides call center applications as a service. Low latency and multiple consumers were a key requirement and upgrading to KCL 2.0 with enhanced fan out improved performance with relatively minor changes required. Failover timeouts can affect latency quite much.

![ANT322](/img/reinvent-2018-first-timer/day1-ant322.jpg)

### Session: SEC304 - AWS Secrets Manager: Best Practices for Managing, Retrieving, and Rotating Secrets at Scale

Random session that I happened to check out as I was already at the venue it was held in. Basic demonstration of different features of AWS Secrets Manager and how it can be used to automatically rotate secrets and enforce good security practices using IAM policies. Watched only half of this as I had to get to the next session in a different venue.

![SEC304](/img/reinvent-2018-first-timer/day1-sec304.jpg)

### Session: DVC304 - Red Team vs. Blue Team on AWS

Pentester (red team) vs. account administrator (blue team). Example case of how to attack into a vanilla AWS account that has some Wordpress site deployed into it following a tutorial found online. Pentester was able to get full access to a RDS database and steal data using only leaked read only credentials and AWS CLI, which can be a powerful tool for finding information. In this case, a Lambda function contained hardcoded DB password in a config file, network security was nonexistant and an old Wordpress version was easily exploited to connect to the database and leak the data. To mitigate this attack, the administrator used IAM instance profiles, NACLs, EC2 parameter store for secrets, WAF, monitoring using GuardDuty, Inspector and separated layers in network architecture.

![DVC304](/img/reinvent-2018-first-timer/day1-dvc304.jpg)

### Session: ANT308 -- Building Serverless Analytics Pipelines with AWS Glue

Overview of what Glue does and how it relates to Spark, DataFrame vs. DynamicFrame, listing performance improvements and features recently launched for the service, for example for orchestration of the jobs. New feature announced, instead of running Glue jobs in Spark, you can soon use Python shell as a runtime for them (launching December 2018). This is great for small or medium sized jobs and for example small data transformation or machine learning workflows. Example workflow of movie recommendations using collaborative filtering. Case example of Realtor.com, moving from Data Pipeline and ECS tasks to Airflow and Python shell Glue jobs lead to better implementation speed, less code, more performance and serverless infrastructure.

![ANT308](/img/reinvent-2018-first-timer/day1-ant308.jpg)

### Workshop: ANT321 -- Tiered Data Sets in Amazon Redshift

Even though workshops were advertised to be done as a team effort and attendees were split into big tables with multiple persons, tasks were done individually following a step by step guide provided by the instructors who then walked around to see if anyone had any questions or problems. Would have expected a bit more talking and group effort, but no-one in the room seemed to do them in groups. The workshop itself was quite basic if you were already familiar with Redshift and Redshift Spectrum. Covered how to load data from S3 using COPY and external tables, then focused more on partitioning the data and how to combine Redshift and Spectrum tables using views. Materials available at https://github.com/aws-samples/amazon-redshift-tiered-storage

![ANT321](/img/reinvent-2018-first-timer/day1-ant321.jpg)

### AWS Nordics Customer Reception

Managed to make a quick stop at the AWS Nordics Customer Reception before heading to the next workshop. It was nice to see so many people attending from the Nordics, and especially to see a lot of Finnish colleagues. Would have liked to be there longer, but had to rush to my next workshop after 30 minutes of networking.

![ANT321](/img/reinvent-2018-first-timer/day1-nordicreception.jpg)

### Workshop: CON323 - Deploying Applications Using Amazon EKS

Similar setup as previous workshop, following step-by-step guidelines with not much guidance. This was actually the part 2 of a 3-part workshop series, so for many (including me) the first 20 minutes were spent on spinning up an EKS cluster and installing the CLI tools to a new Cloud9 IDE environment. The workshop material was quite well documented and guided (available online at https://eksworkshop.com/). Topics covered ranged from health checks to auto scaling applications and clusters, setting up a CI/CD pipeline and monitoring. I’m not yet that familiar with Kubernetes so some of the configuration needed seemed to add quite a lot of overhead and felt cumbersome. The topics also touched on CodeBuild, CodePipeline, X-Ray and CloudFormation, so it was also nice to see how they functioned as I haven’t used them much previously (as we use Jenkins and Terraform/Ansible in my current project).

![CON323](/img/reinvent-2018-first-timer/day1-con323.jpg)

## Day 2

### Session: STG303 - Deep Dive on Amazon S3 Security and Management

Generic overview of different ways to control access to S3 buckets using IAM policies, bucket policies and ACLs. Demos of the different options of the new feature, S3 Block Public Access, which restricts public access on a bucket or account level. Case example of Intuit data lake and controlled access restricted using VPC endpoints, IP blocks and principal organization ids and also a shared access for legacy applications using User-Agent header as a “password” for uploading files to S3 without an IAM user or authentication.

Not much new information here, but it was interesting to hear how many different ways there are for restricting and allowing access.

![STG303](/img/reinvent-2018-first-timer/day2-stg303.jpg)

### Workshop: ANT318 - Build, Deploy and Serve Machine learning models on streaming data using Amazon Sagemaker, Apache Spark on Amazon EMR and Amazon Kinesis

Todays workshops were a bit better instructed than yesterday, with instructors going through all the steps in detail, but overall these still relied heavily on following provided instructions step by step. In this workshop we were provided Qwiklabs access and a ready CloudFormation template for setting everything up. 

In the exercises, the idea was to build a machine learning model based on flight event data and try to predict if a flight is late when given a start airport, start time, destination and airline. The actual exercises were ready Jupyter notebooks that were run using SageMaker. In the later parts, a Kinesis stream and a simple Scala backend app was set up for serving queries coming in using a REST API and using a SageMaker endpoint for fetching predictions using the previously built ML model.

Quite a lot of things were covered in 2 hours, but would’ve hoped for more time and actual thinking instead of just running the ready made notebooks step by step.

![ANT318](/img/reinvent-2018-first-timer/day2-ant318.jpg)

### Session: DEV317 - Advanced Continuous Delivery Best Practices

A session focusing on how to leverage CD best practices using AWS tools (CodeBuild, CodeDeploy and CodePipeline). Started out with a simple pipeline of just build, test and deploy but improved on it step by step. First adding simple health checks, system tests, rolling deployments, segmenting deployments into smaller groups, green/blue deployments, canary instances and finally multi region deployment one region and segment at a time. Pretty informative and the terms were clearly explained, but most of the applied techniques only work if you have a large amount of hosts that you are deploying the software for. Would’ve been interesting to hear how to apply these in containerized or serverless applications, but that was apparently covered in a different session

![DEV317](/img/reinvent-2018-first-timer/day2-dev317.jpg)

### Session: DAT302 -  ElastiCache Deep Dive: Design Patterns for In-Memory Data Stores

Overflow rooms are great for random sessions, jumped right into the next session that had just started 5 minutes ago without having to walk to a different location. This one demonstrated new features of Redis 5 that are usable in ElastiCache. Big focus was on different scaling techniques for Redis clusters, horizontal (partitioning data into shards) vs. vertical (scaling up the instances), cost is about the same but a lot of benefits in sharding. Different use cases for ElastiCache were also showcased, for example caching, realtime sentiment analysis, IoT, Kinesis clickstream filtering, mobile apps and so on. Caching patterns, cluster sizing best practices, monitoring and how to resolve issues found using metrics were also discussed.

![DAT302](/img/reinvent-2018-first-timer/day2-dat302.jpg)

### Session: SRV303 - Monitoring Serverless Applications

Not that great of a session, presented by New Relic and CapitalOne speakers who just reiterated the difficulties of developing, scaling and monitoring complex serverless applications without proper debugging tools, local development environment and metrics, but offered no new solutions except for an upcoming New Relic Lambda Monitoring feature that was not even properly demoed. Would’ve hoped for new AWS solutions announced for this.

![SRV303](/img/reinvent-2018-first-timer/day2-srv303.jpg)

### Workshop: ANT313 - Serverless Data Prep with AWS Glue

Final workshop of the day, right in the middle of Pub Crawl. Here we loaded the NYC Taxi dataset from S3 to Glue Data Catalog using Crawler, then did some raw queries to it using Athena, then cleaned up and optimized it for reporting queries using Spark and finally created a ML model for customer tipping behaviour using Sagemaker. A bit similar to the Sagemaker workshop I attended earlier, but a bit more Spark and Glue was used here

![ANT313](/img/reinvent-2018-first-timer/day2-ant313.jpg)

## Day 3

### Keynote: Andy Sassy

Quite a lot of new stuff announced, excited to try some of them out but unfortunately not many sessions or workshops available here. As for the keynote event itself, it was a big hall and a really big crowd, but a surprisingly smooth process to get in, basically walked straight in 20 minutes before the keynote started and got the best seats in the house :sadtroll:. A nice experience to see it live in person, but will watch tomorrow’s keynote from an overflow location to save some time from traveling between locations.

![Keynote](/img/reinvent-2018-first-timer/day3-keynote.jpg)

### Hackathon: Game Day 2018

After the keynote had some time for a lunch with other Solita people and to make a quick visit at the expo before heading to the other side of the campus for a 5 hour Game Day hackathon. The shuttle arrived a bit earlier than I expected, so had some time to visit the MGM Grand Arena where they were showcasing the just announced DeepRacer robocar. Checked out a walk-in garage where you could come in to try out your reinforcement learning model on a test track with a real car instead of just running simulations.

![Deep racer arena at MGM Grand](/img/reinvent-2018-first-timer/day3-deepracer.jpg)

As for the Hackathon itself, we formed a group of 4 with two guys from Finland and one guy from a Japanese software company. There were about 60 other groups and we each tried to run our own microservices that were then advertised to a centralized “marketplace” where you would pick other teams services to be run on your “service router”. Each team would then periodically get points for 1) each request made against their service and 2) successfully routing requests to other teams services by keeping the service router up and running.

First, we had to log in to a dashboard, check the instructions and try to get the microservices up and running on a provided AWS account. Two of the services used CloudFormation templates to spin up the service, one used Fargate and one Lambda+SAM. We were also provided with accounts to NewRelic and DataDog monitoring services that were connected to the microservices that we were trying to keep up and running.

During the hackathon, there was an evil chaos engineering team that randomly did some stuff to our services so that they were not working anymore and we had to get them up and running again. The services were leaking memory and crashing randomly so auto scaling groups and load balancers were the first thing that we added to improve them. We weren’t expecting that heavy of a chaos monkey approach, as we struggled a bit in trying to figure out why our services were down only to find out that somehow our VPCs had lost an internet gateway or routing tables had been deleted. We also ran into some really strange error messages due to the limitations placed on the IAM roles we were running the services on.

Overall though, it was a really fun and hectic experience, as you could monitor your own points in real time and see the top teams in a leaderboard on the big screens. In the end, our team placed 22nd out of 63, so I guess we managed to do okay.

![Game day](/img/reinvent-2018-first-timer/day3-gameday.jpg)

### Session: DEV375 - Introduction to Amazon CloudWatch Logs Insights

Managed to spot one session with “NEW LAUNCH” tagged on it after the keynote ended that still had room (other sessions were fully booked right away) and was happening right after the game day ended 

Cloudwatch Logs Instances allows running analytical queries against Cloudwatch logs. You can do a lot more than with regular Cloudwatch log searching, for example quick visualizations, grouping, time series aggregations, calculations, percentiles and sorting. This makes it much more easier to find relevant information from logs. Use cases range from operational troubleshooting, application analysis during development, dashboards and security breaches. Use case example from Gemalto who use it for security incident forcensics and reports using Lambdas. 

The feature itself looks like it could be really useful in some cases, as filtering and searching with regular Cloudwatch logs is really painful. Unfortunately the features are quite barebone as of now, and they don’t support e.g. scheduled queries or reporting results as a metric or alarms straight out of the box (you need to use the API and e.g. Lambdas for all that).

![DEV375](/img/reinvent-2018-first-timer/day3-dev375.jpg)

## Day 4

### Keynote: Werner Vogels

This time I watched the keynote from an overflow room in a different hotel. Quite many were doing the same thing, and the first large room for that even got full. The first half of the presentation focused more on technical deep dives on how distributed databases and S3 work, and the rest of the presentation focused on serverless technologies, see AWS feed for new announcements. The new Lambda features sounded quite exciting.

![Keynote](/img/reinvent-2018-first-timer/day4-keynote.jpg)

### Jam lounge

Left a lot of empty space in my calendar for today, hoping for sessions and workshops for the newly announced services, but unfortunately there were only a couple of those (not nearly for everything that was announced) and the few ones got booked full really quick. So decided to just go walking around the expo areas. Managed to find a Jam Lounge in the expo area where you could complete various AWS related challenges during the week and compete for prizes. Had some extra time so I completed two challenges, one related to Athena and one to a 3rd party networking tool called Aviatrix and got an Amazon Echo Dot sponsored by them. Finished 28th overall in the standings, so not that many people were aware of the whole jam thing, could’ve probably gotten even more prizes if I had been around when the jam ended but had to run to a workshop which started at the same time.

Doing the challenges was a nice contrast to the step by step workshops that I had been going to on previous days, as you were forced to think a bit more yourself but were still able to get help if needed by using hints (that affected your points negatively). Wish I had known about this jam on the first days, would’ve liked to tried out some more challenges.

![Jam lounge at the Expo](/img/reinvent-2018-first-timer/day4-jamlounge.jpg)

### Workshop: STG401 - Building a Data Lake in Amazon S3 & Amazon Glacier

This was an expert level workshop but the instructor presented some really basic level stuff, starting out with a question “Who has heard of S3 before?” :face_with_rolling_eyes:

This time no ready account was provided so the first 25 minutes were spent on waiting for Cloudformation stacks to complete running. The rest of the workshop was yet again quite simple, following instructions step by step. I was hoping that the AWS Lake Formation would have been used in this workshop, but instead of that the old AWS Data Lake Solution (https://docs.aws.amazon.com/solutions/latest/data-lake-solution/welcome.html) was used, meaning a lot of different AWS services were used. In the first part, a Lambda generating data to Kinesis Data Streams, Firehose and Analytics was used to process and analyze the raw data and upload it to S3. The Data Lake Solution provided webapp was then used to add the analyzed files into the data lake “package” that allowed other users to search and download the files from S3 through the webapp. The second part would’ve consisted of using Glue, Athena and Quicksight for further analyzing the Kinesis raw data, but didn’t have enough time to finish that fully.

Materials for the workshop can be found from https://s3.amazonaws.com/tlicustomershare/DatalakeWorkshop.zip

![STG401](/img/reinvent-2018-first-timer/day4-stg401.jpg)

### Re:Play

The biggest party of the week happened on Thursday evening, held at a nearby festival grounds. Simply, a really massive festival type of party setting with three huge tents and a large outdoors area, loads of random activities, long lines, food and drinks. Oh, and also live music from Thievery Corporation, Future Islands and Skrillex.

![Re:Play](/img/reinvent-2018-first-timer/day4-replay.jpg)

## Day 5

### Session: CON361 - Deep Dive on Amazon EKS

Quick visit to a random session near the breakfast area before heading to a workshop because for some reason the early sessions didn’t have that many people and you could just walk in, I wonder why :thinking:. 

A basic overview of how EKS works and the differences between Control Plane and Worker Plane. Only listened to the first fifteen minutes, but didn’t seem to go that deep into details, will have to check the rest of the session from Youtube.

![CON361](/img/reinvent-2018-first-timer/day5-con361.jpg)

### Workshop: DEV305 - AWS DevOps Essentials: An Introductory Workshop on CI/CD Best Practices

A pretty good overview on how to use CI/CD tools that AWS provides (CodeCommit, CodeBuild, CodeDeploy and CodePipeline). Pretty quick to set up and manage using the CLI and through the console as well. Cloud9 is a pretty handy tool for these workshops, as you can just launch an environment and use the CLI tools and deploy Lambdas from there.

A basic deployment pipeline was set up, with automated builds from each commit to master branch, deployment to dev environment, a Lambda function for testing and then a manual approval process with SNS email notification before the production deployment. 

Materials available at https://github.com/awslabs/aws-devops-essential/

![DEV305](/img/reinvent-2018-first-timer/day5-dev305.jpg)

### Session: ANT401 - Deep Dive and Best Practices for Amazon Redshift

An overview session of the different concepts that Redshift is built upon with some helpful tips on how to optimize and fine tune the performance of the database. A nicely presented session and managed to learn something new (the recommended way of doing upserts with a temp staging table, delete and insert into) even though I work with Redshift daily on my project.

![ANT401](/img/reinvent-2018-first-timer/day5-ant401.jpg)

### Solita Christmas Party

After all the sessions the Solita crew gathered together to have a Christmas party lunch at a nice Mexican restaurant. As the official Solita Christmas Party was happening simultaneously in Finland, we also had a short video call with them, and briefly got to experience the atmosphere of the party on the other side of the world.

![Solita crew](/img/reinvent-2018-first-timer/solitacrew.jpg)

# Conclusion

The week went by really fast as the days are long and full of content from early morning to late evenings. 

Despite the massive scale of the conference, the logistics worked pretty well. There was a massive amount of personnel at the venues guiding you to the right place and answering questions. It was quite amazing how smoothly everything worked out at every venue, and the shuttles between them were quite handy too, as it usually saved a lot of walking through the casinos as most of the shuttles ran from event center to event center. The only thing that didn’t work out regarding logistics was the conference breakfast at Mirage, on the two days I tried to have it there they had already run out of it half an hour before it was supposed to end.

![Venetian](/img/reinvent-2018-first-timer/venetian.jpg)

On the first day I made the mistake of booking sessions and workshops that were held all over the campus. This meant a lot of time spent travelling between venues instead of watching sessions or attending workshops. The following days I tried to make use of overflow venues and stick into one or two venues per day.

Try to network with other peers, there are a lot of different events happening all week long, a handy website called Conference Parties listed these. Plus, you usually get free food and drinks at these events.

As this was my first time, I probably packed my schedule too full of sessions, which meant that I had little time to visit the Expo, for example. As a result, I missed out on things like the awesome Jam lounge which I discovered only on the last day it was open.

One thing that was a bit disappointing was that there weren’t that many sessions available for the new features, and the ones that were available got full instantly.

Hopefully they’ll also make it easier to make better schedules on the following years.

Overall, it was a great week with a lot of new things and best practices learned that can be applied to my daily work. Hopefully I’ll get the chance to attend the conference sometime in the future too. 
