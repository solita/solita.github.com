---
layout: post
title: AWS re:Invent 2017 workshops and hackathons
author: jooelkorpi
excerpt: AWS re:Invent contains several workshops and hackathons. Here are some thoughts on couple of them that I managed to attend.
tags:
- AWS
- re:Invent
- hackathon
- workshop
---

## Why workshops and hackathons?
When I was registering for different re:Invent sessions, the workshops and hackathon were the first in line. There were multiple reasons for this:
1. They wouldn't be filmed, so I couldn't experience them later
2. Most were team based exercises and this way I could connect with other AWS experts
3. I'm at least partly kinesthetic learner and the hands-on approach worked very well


## Feelings from three different sessions

### HAC04 - GameDay | A Digital Adventure (8h)

I was really excited for the GameDay. A whole day hackathon type situation were you are supposed to use many different AWS services and resolve different kind of issues. It didn't completely live up to my expectations, but it was great nonetheless and in few places surprised my expectations.

The narrative premise for the hackathon was that we were new employees/consultants for Unicorn rental -company. All of the previous employees have been fired, systems aren't working and CEO is missing. Our mission is to fix everything. On the practical level, we were in four member teams with progress monitored with points. AWS provided an AWS account and a slack channel for the team. Because of the length of the hackathon, the food was also provided in the same location.

![Current situation](/img/reinvent-workshops/gameday.jpg)

Our team was quite international: Finnish, Swedish, Japanese and American. Still, different native languages didn't affect the work except when I tried to do help teammate with the Japanese laptop. If I would have remembered order of each item in browser context menu it wouldn't have been as bad.

The tasks were quite interesting and used variety of AWS services. I would have wanted more linkage between some tasks, even though current setup made it easier to split tasks between team members. Also, there wasn't any high volumes of traffic or simulated disconnection of an availability zone, probably because of the required work from AWS side and the cost of infrastructure.

Some issues really hindered the progress: wlan and CodeCommit. Wireless network was really slow from time to time and at least once it was completely down. When working with AWS a stable network is quite paramount. Our team had quite a lot problems getting CodeCommit to work with IAM credentials. The problem in my case was that Mac stored the credentials to the keychain even though our credentials needed to be renewed every hour. The credentials needed to be removed every time so that IAM login to CodeCommit would retrieve the new ones from the config file.

### SID312 - DevSecOps Capture the Flag (2,5h)

The name was little bit misleading, because there wasn't any flag to capture. The workshop was about static code analysis of CloudFormation templates in order to catch templates which brake the security practices. These were, for example, security groups with connections open to 0.0.0.0/0. The participants were split into teams of around four members.

Depends on the person, if this kind of workshop would be interesting enough. For me, the way the workshop was implemented was very interesting. All participants had too hash-codes, their own and the teams. Everyone linked their own names(or nicknames) to their codes and also a team name. These were used for keeping track of the scores. AWS team supplied everyone also with a CloudFormation template which included API Gateway, couple of Lambda functions (prod and dev) and a registrator which told the workshop system that start sending templates. The api should send different response depending on which rules the template broke if any. Team got points depending of the how well each individual participant did. This guided people to help their team mates, but also to split the tasks so that the whole setup was ready faster.

My team consisted of four members. First thing that we, and at least our neighbour team did, was to setup a slack team to quickly send code-snippets to each other. Slack was also used to get statics of how well our current Lambda functions were catching the correct templates. There were some difficulties in my team because of unfamiliarity with Python and Slack. For this reason we split into two sub-teams, where I worked mostly solo and the other three worked together. Probably not the most optimum setup, but that is one exciting aspect of these time-bound exercises - you need to make decisions quickly and live with them. We finished somewhere in the middle which was ok at least for me with randomly selected team. The AWS team released the standard solution at the end before point collection ended which I didn't like. It meant that everyone just switched to use it and stopped working in order to get more points.

### SID402 - An AWS Security Odyssey: Implementing Security Controls in the World of Internet, Big Data, IoT and E-Commerce Platforms (2,5h)

The name of the session was very promising and with it being expert level, I thought that I would learn quite a lot. But, it was probably the largest disappointment in the re:Invent. The first thing was that this was a solo workshop even though you could of course ask others in the same table for help or discussions. But, the biggest hit was when I understood that we were just going to follow step-to-step instructions from a [GitHub repository](https://github.com/aws-samples/aws-security-odyssey). The only difficulty in the tasks was because during re:Invent new functionality had been released to the AWS console and the step-to-step instructions weren't valid anymore.

The added benefit of doing this in re:Invent would of course be that there were AWS personnel and other participants to help you. But I left at least half hour early and asked help only when the instructions conflicted with the current console. At least I could have used my time in re:Invent in some other more useful session. But, the material is quite good, if you want to do it yourself.

## Value and requirement for hosting team hackathons/workshops compared to lectures

Value:
- Hands of working
- Gamification elements in the limited view of points and leaderboards
- Team work

Requirements:
- Usable network
- Ready made infrastructure for sending events and keeping track of progress
- Ready made CloudFormation templates etc. for the basic setup

I am planning to hold an AWS training following these principles at Solita at some point during the spring.
