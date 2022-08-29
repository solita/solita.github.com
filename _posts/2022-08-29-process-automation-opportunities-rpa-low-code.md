---
layout: post
title: Exploring process automation opportunities – RPA and low-code application development
author: jaakko.saha
excerpt: I finished my masters' thesis about process automation lately. The research approached the topic from two different angles, RPA and low-code application development. On the tool side I was focusing to Robot Framework and Microsoft Power Platform
tags:
  - low-code
  - RPA
  - Power Platform
  - Robot Framework
  - thesis
---

Lately I finished my masters’ thesis about process automation. The research approached the topic from two different angles, Robotic Process Automation (RPA) and low-code application development, more specifically [Robot Framework](https://robotframework.org/) and [Microsoft Power Platform](https://powerplatform.microsoft.com/en-us/). Contrary to the majority of current research material about the topic, this research didn’t focus on the experiences of business owners or IT-specialists, but instead attempted to clarify what kinds of process automation solutions have been created, what kinds of solutions are desired and what kinds of solutions are considered helpful, from the point of view of people working on the processes themselves. Here are the summarized findings of my research.

## Process Automation

Automation in general aims to decrease the necessity of human interaction in different processes. Manufacturing different products has been a target of automation for decades. As technological development has progressed is has become possible to automate repetitive tasks in modern office work as well. Repetitive tasks that follow certain rules and have a significant risk of human error are usually very suitable for process automation. The global business process automation market is expected [to grow up to $19,4 billion by 2026](https://www.marketsandmarkets.com/Market-Reports/business-process-automation-market-197532385.html).

Process automation has not yet been researched all that much, which is why there are still some common misconceptions regarding this subject. Most notably, robotic process automation (RPA) is often considered as the one and only form of process automation and these two terms are considered as one and the same. In reality RPA is just one form of process automation since practically any form of development which reduces the necessity of manual labor can be considered as process automation. This includes system integrations, process planning and software development. RPA has been the most studied form of process automation for few years, which is why it has gained majority of the focus. 

## Robotic Process Automation

Robotic Process Automation, or RPA, has nothing to do with mechanical robots used in different factories etc., but instead is a purely software-based solution, designed to mimic different tasks performed by human employees. Developing an RPA solution often starts with determining all the steps a human worker performs in a certain process, including every input and click of a button. All the potential exceptions and errors should also be documented. After all the steps are scripted, the software robot is built to mimic the described process. 

The reason RPA solutions can be more productive than human workers in certain processes it that RPA solutions are generally faster, and they don’t make any humane errors, like typos or misinterpretations. From developers’ point of view, creating RPA solutions can be fast and low-effort, since the solution can be implemented to use existing systems without the necessity to alter said systems in any way. Generally the RPA solution can do all the same tasks as a human worker, so access to required systems can be obtained in a similar manner, as with human employee. 

The main shortcomings of RPA solution are caused by the necessity of structured data and certain types of processes. If the process has a lot of exceptions and requires a high level of deduction, creating a reliable RPA solution can be next to impossible. Also, as the solutions requires the processes to remain as they are, system updates and changes to the process workflow are likely to cause the solution to malfunction. 

## Low-code in Process Automation

Low-code is a programming technique derived from the concepts of Rapid Application Development, where the programmer has the freedom to spend more time designing the functionality and aesthetics of a application, rather than the syntax of the code itself. Low-Code Development Platforms are generally based on graphical user interfaces, which allow for the users to create applications and automated workflows without writing any code. Low-code contributes to the universal shortage of professional software developers by lowering the entry barrier to create solutions and applications. This research mostly focused on MS Power Platform.

Developing applications and automated flows with Power Platform, or any other Low-code Development Platform (LCDP), is generally faster and easier than traditional software development. Also, the simplified nature of development allows for the employees outside the IT-department to participate in application development. This makes it easier for employees who have more knowledge about the business processes themselves to make sure that the application, or automated solution, meets all the business requirements. 

## Research

Focus of this research was to discover what types of process automation solutions have been crafted with different process automation tools and how well have these solutions functioned. Additionally this research aimed to examine the experiences regarding process automation in different organizations, both positive experiences and negative. A survey form was sent to ten different organizations from varying fields. The responders in these organizations were not IT-specialists, but people who have worked on the processes that have been automated i.e., people who notice the actual benefits or problems regarding the solutions. 

The survey was created with Microsoft Forms and was created to be responsive to the answers selected, for example, if the responder states that they don’t have any experience regarding process automation, they wouldn’t be questioned about their experiences, but instead about potential reasons for the lack of experience. 

## Results

Overall, responders had bee quite satisfied with the created solutions. When asked to grade their satisfaction about the solutions with the scale from 1 to 5, the results averaged on 3,41. Clear majority of the automated processes was repetitive manual tasks, which was to be expected. When asked about hopes regarding process automation, the responders seemed to want more of the same; automatic invoicing, notifications, reporting which has already been done. The main problems with the current solutions were with the reliability of the solutions. Apparently in some cases, the processes had been so complex that the automated solution requires constant supervision to work. One responder even stated that the tasks related to ensuring the functionality of the automated solutions often end up as responsibility of few selected employees, which has caused feelings of inequality amongst the workforce. 

Majority of the responders weren’t sure, what tools had been used for process automation in their organization, which was to be expected, since the survey wasn’t directed to IT-specialists. None of the responders directly stated Robot Framework as their answer, but some of the written answers included e.g. “Python” or “Custom software development”, which doesn’t exclude the possibility of Robot Framework being used. Some responders had recognized Power Platform as a used tool. 

## Conclusions

Generally, people seem to want the type of solutions that have already been made, especially various financial processes. This is understandable, since financial processes are often highly regulated and follow certain patterns, which can be taught to software solutions. It would seem that successful implementation of certain solutions has created a “snowball effect”, by changing the mindset within the organization. When employees notice how certain processes have been developed with specific tools, they start to notice development potential on other processes as well. Similarly, if the implementations have been unsuccessful, the mindset remains or becomes negative, which makes it all the harder to implement anything successfully. This scenario proves again, that process automation and process development aren’t purely IT-related projects but are related to the organizational culture as a whole. 

The main reasons preventing this “snowball effect” from happening, is that the planned solutions either are implemented poorly, or the automated processes have not been made eligible for automation in the first place. All automation processes should initially start by determining if the process itself is suitable for automation, more often than not, there are some changes required for the solution to work, but it is essential that these changes are done before any software solution is being built. If the solution is not thoroughly planned beforehand, there is a risk that the human efforts within the process are altered to serve the automated solution and not the other way around. 

If one would compare the two different tools mentioned in this research, Robot Framework and Power Platform, there is no definitive answer for which tool would be better for process automation or process development. Both tools have their strengths and weaknesses. When compared, Robot Framework has the advantage of being able to use practically any existing systems. Power Platform on the other hand is more flexible when creating solutions that require some user interaction, for example filling out a form or triggering an automated flow when needed. 

You can read my complete thesis [here](https://jyx.jyu.fi/handle/123456789/82113)

I belong to Solita's low-code team, [more info here](https://www.solita.fi/en/low-code-development/)
