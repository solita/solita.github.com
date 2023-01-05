---
layout: post
title: Exploring Process Automation opportunities - RPA and low-code application development
author: jjjsaha
excerpt: I finished my masters' thesis on this subject last year. The research approached the topic from two different angles, RPA and low-code application development. The specific tools studied were Robot Framework and Microsoft Power Platform.
  
tags:
  - thesis
  - RPA
  - low-code
  - Robot Framework
  - Power Platform
---

Last year I finished my masters’ thesis about process automation. The research approached the topic from two different angles, Robotic Process Automation (RPA), and low-code application development, more specifically [Robot Framework](https://robotframework.org/) and [Microsoft Power Platform](https://powerplatform.microsoft.com/en-us/). Contrary to the majority of current research material about the topic, this research didn’t focus on the experiences of business owners or IT-specialists, but instead attempted to clarify what kinds of process automation solutions have been created, what kinds of solutions are desired and what kinds of solutions are considered helpful, from the point of view of people working on the processes themselves. Here are the summarized findings of my research.

## Process automation

Automation in general aims to decrease the necessity of human interaction in different processes. Manufacturing various products has been a target of automation for decades. As technological development has progressed is has become possible to automate repetitive tasks in modern office work as well. Repetitive tasks that follow certain rules and have a significant risk of human error are usually very suitable for process automation. The global business process automation market is expected [to grow up to $19,4 billion by 2026](https://www.marketsandmarkets.com/Market-Reports/business-process-automation-market-197532385.html)

Process automation has not yet become a popular research subject, which is why there are still common misconceptions regarding this subject. Most notably, researchers often refer robotic process automation (RPA) as the one and only form of process automation and state that these two terms as the same. RPA is just one form of process automation since any form of development which reduces the necessity of manual labor can be considered as process automation. This includes system integrations, process planning and software development. RPA has been the most studied form of process automation for few years, which is why it has gained majority of the focus. 

## RPA

Robotic Process Automation, or RPA, has nothing to do with mechanical robots used in different factories, but instead is a purely software-based solution, designed to mimic different tasks performed by human employees. Developing an RPA solution often starts with determining all the steps a human worker performs in a certain process, including every input and click of a button. All the potential exceptions and errors should also be documented. After scripting all the steps, the software robot can mimic the described process.

The reason RPA solutions can be more productive than human workers in certain processes it that RPA solutions are faster, and they do not make any humane errors, like typos or misinterpretations. From developers’ point of view, creating RPA solutions can be fast and low effort since the solution is implementable to use existing systems without the necessity to alter said systems in any way. The RPA solution can do all the same tasks as a human worker, so access to required systems can be obtained in a comparable manner, as with human employee.

The necessity of structured data and specific types of processes is the main shortcoming of RPA solutions. If the process has multiple exceptions and requires an elevated level of deduction, creating a reliable RPA solution can be next to impossible. Also, as the solutions require the processes to remain as they are, system updates and changes to the process workflow are likely to cause the solution to malfunction.

## Low-code in process automation

Low-code is a programming technique derived from the concepts of Rapid Application Development, where the programmer has the freedom to spend more time designing the functionality and aesthetics of a application, rather than the syntax of the code itself. Low-Code Development Platforms are based on graphical user interfaces, which allow for the users to create applications and automated workflows without writing any code. Low-code contributes to the universal shortage of professional software developers by lowering the entry barrier to create solutions and applications. This research focused on Microsoft Power Platform as the selected low-code development platform.

Developing applications and automated flows with Power Platform, or any other LCDP, is faster and easier than traditional software development. Also, the simplified nature of development allows for the employees outside the IT-department to participate in application development. This makes it easier for employees who have more knowledge about the business processes themselves to make sure that the application, or automated solution, meets all the business requirements. 

## Research

Focus of this research was to discover what types of process automation solutions the responders have experience with and how well have these solutions functioned. Additionally, this research aimed to examine the experiences regarding process automation in different organizations, both positive experiences and negative. This research gathered materials via survey form sent to ten different organizations from varying fields. The responders in these organizations were not IT-specialists, but people who have worked on the automated processes themselves i.e., people who notice the actual benefits or problems regarding the solutions.

The survey, created with Microsoft Forms, was responsive to the answers selected, for example, if the responder states that they do not have any experience regarding process automation, the survey would not question them about their experiences, but instead about potential reasons for the lack of experience.

## Results

Overall, responders had been quite satisfied with the created solutions. When asked to grade their satisfaction about the solutions with the scale from 1 to 5, the results averaged on 3,41. Clear majority of the automated processes was repetitive manual tasks, which was not surprising. When asked about hopes regarding process automation, the responders wanted more of the same; automatic invoicing, notifications and reporting which has already been done. The main problems with the current solutions were with the reliability of the solutions. In some cases, the processes had been so complex that the automated solution requires constant supervision to work. One responder even stated that the tasks related to ensuring the functionality of the automated solutions often end up as responsibility of few selected employees, which has caused feelings of inequality amongst the workforces.

Majority of the responders were not sure, what tools their’ organization had been using for process automation, which was expectable since the survey did not focus just to IT-specialists. None of the responders explicitly stated Robot Framework as their answer, but the written answers included for example “Python” or “Custom software development,” which does not exclude the possibility of Robot Framework being used. Few of the responders had recognized Power Platform as a used tool.

## Conclusions

People want the type of solutions that have already been made, especially in various financial processes. This is understandable since financial processes are often highly regulated and follow certain patterns. Successful implementation of certain solutions has created a “snowball effect,” by changing the mindset within the organization. When employees notice certain automated processes, they start to realize development potential on other processes as well. Similarly, if the implementations have been unsuccessful, the mindset remains or becomes negative, which makes it all the harder to implement anything successfully. This scenario proves again, that process automation and process development are not purely IT-related projects but are related to the organizational culture.

The main reasons preventing this “snowball effect” from happening, is often the poor implementation of the planned solution, or the automated processes are not eligible for automation in the first place. All automation processes should initially start by determining if the process itself is suitable for automation, often, there are some changes required for the solution to work, but it is essential that these changes are done before any software solution is being built. If the team implementing the solution does not focus enough on planning the solution beforehand, there is a risk that the proposed solution starts to alter the human efforts within the process to serve the automated solution and not the other way around.

If one would compare the two different tools mentioned in this research, Robot Framework and Power Platform, there is no definitive answer for which tool would be better for process automation or process development. Both tools have their strengths and weaknesses. When compared, Robot Framework has the advantage of being able to use any existing systems. Power Platform on the other hand is more flexible when creating solutions that require user interaction, for example filling out a form or triggering an automated flow when needed.


Full thesis work can be read from [here](https://jyx.jyu.fi/bitstream/handle/123456789/82113/URN%3aNBN%3afi%3ajyu-202206303713.pdf?sequence=1&isAllowed=y)

I work with Solita's low-code team, [more info here](https://www.solita.fi/en/low-code-development/)