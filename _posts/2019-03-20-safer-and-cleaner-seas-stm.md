---
layout: post
title: Safer and cleaner seas via Sea Traffic Management
author: arto
excerpt: Air traffic has been digitalized long ago. Now, the seas are going same route as well. Future holds much safer and cleaner marine traffic for all of us. 
tags:
- Environment
- Project
- Distributed
- Java
---
Our environment is at distress. Climate change is making our future world look very different than it is today. Since industrial age, mankind has been polluting the environment more and more, to produce what growing population of planet earth needs and wants. We have gotten very good at moving things around the world, including such essential things as food, water and medicine. If all transport were to stop today, all cargo would stop moving as well, and we would have some serious problems.

On the other hand, to transport something we need energy sources, more or less clean ones, more or less efficient ones. We also need to expend that energy, and in some cases, a lot of it. Cargo planes, ships, trucks, and trains need a lot of energy, but if they stopped moving, cogs of our society would stop, too. Future will no doubt bring along new forms of energy: cleaner, more efficient ones. But while waiting for future to arrive, existing energy forms usage requires optimization right now.

Another area where we can improve are human errors. People make mistakes. On a typical day, anyone of us can make dozens of small or not so small mistakes. Use permanent marker on a whiteboard. Use salt in coffee instead of sugar. Forget to signal when changing lanes. Most mistakes are common and quite small, and cause no harm. But when a severe enough mistake happens at sea, people's health and life may be at danger. Additionally, some of the worst disasters generate environmental disasters as well.

### Sea Traffic Management

Sea Traffic Management, formerly known as Mona Lisa, is an EU wide project, currently at Validation phase. Goals are various, but at the core is optimization of sea traffic across EU. Optimization means here better efficiency, improved safety, and of course, better use of resources. 

Here are the currently listed goals for full deployment of STM by year 2030 in relation to year 2015:
- Safety: 50% reduction of accidents.
- Efficiency: 10% reduction in voyage costs and 30% reduction in waiting time for berthing
- Environment: 7% lower fuel consumption and 7% lower green house gas emissions.

7% might sound low, 100% would certainly be much better. But on EU-wide scale, in year 2017, we spent 37 231 000 tonnes of fuel oil and gasoil combined. So using better optimization and coordination, we can still do much better. So while waiting for better forms of energy to acquire wider use, optimization can bring those numbers down to more positive direction. In other words, we are able to transport people as well as items cheaper than today, and possibly instead of polluting more and more, start polluting less and less every year. Meanwhile, optimization will improve, and new energy forms will certainly find their way in.

Of course, being able to communicate with less room for errors, can also have a pretty large impact on marine traffic. Today, human errors cause inefficiency, delays, increased costs. More severe mistakes of course have potential to cause much larger problems. Doing routine work that has to be repeated just right is a big reason for human errors.

Computers make mistakes as well, but they tend to be more systematic and predictable, and we have ways to lessen that likelihood, by applying professional software engineering principles.

### What did Solita have to do with Sea Traffic Management?

Finnish Transport Agency is one of the parties that is participating in STM project validation phase, to find ways to improve communications, mainly at Sea of Bothnia. We were working with them within a project, and I was part of a small team with focus on the STM validation aspect. 

Technical part of what we were doing was nothing spectacular, quite straightforward messaging was big part of it. Interesting part was the constantly evolving standards, evolving goals and milestones, and how to fit all pieces together, also in line with the needs northern hemisphere poses.

STM Validation is a big project, with numerous teams working on different aspects in different places. Our main focus was the ice navigation, routing through ice more efficiently, without causing merchant ships to get stuck on difficult routes, causing delays. Additionally, how to communicate with Ice Breaker fleet so that existing pathways can be efficienctly reused. All this will naturally bring great savings in both cost and environmental impact. Another aspect was digitalizing communicatons between ports and vessels. This means better capabilities to estimate when ship is going to be leaving port or arriving to port, which can also help optimizing how icebreakers will be able to assist ships. Additionally, standards can be also used to route nautical warnings and even small text messages when conversing and optimizing routes.

You have to note that before STM project, there has not been a great common standard for digital communications at sea. Or rather more, there has been multiple different standards. But this has lead to communication in most cases preferring radio calls and freeform emails. Of course this communication takes place at sea, where weather conditions might bring a few more twists on how easy it is to communicate and understand eachothers.

### Technical solutions and lessons learned

STM components and architecture are very simple, and platform agnostic. One big part is a set of standard schemas for specific messages. One of the first  schemas that we were working on was rtz route exchange format, which allows to exchange route information in many different lifecycle phases between parties. Ship might initiate conversation by exporting their planned route to rtz, then sending it to harbor or icebreaker for optimization. Receiving party can then apply some guidance for the route, for example advising to avoid specific area, or reroute via a waypoint where there's already a pathway in ice, suitable for ship in question. After optimization, new route suggestion may be sent back to ship, then imported into actual navigation systems for verification and usage.

Few of the other useful standard formats are Area Exchange Format, which can be used to deliver geolocation information such as specific point or area, which can be attached with Text Message Format, to deliver description, or even chat messages between two parties. This allows for example to share nautical warnings on areas to avoid, or to negotiate an optimal route that requires some discussion. 

All of these standards can be used to replace traditional radio communication, which is very prone to human errors. Area, text and route information can also be easily passed via existing simple channels, such as email. Email systems are quite robust, and asynchronous, so to some extent they can also work over unreliable networks. 

However, to achieve even more robust message delivery, STM has more parts, that can be used to replace any email based communication alltogether. STM standard defines components called SeaSwim connectors, and Maritime Connectivity Platform. This means abstracting the communications protocol to a robust and secure platform that is able to identify parties using certificates, and deliver any standards-based messages securely over network, tolerating shaky/bad/missing network scenarios. There is also a registry for services and identities, which can be used to negotiate on how to communicate with a new, unknown party. 

At the moment, STM is at validation phase, which means things are still moving and evolving rapidly. There are multiple small projects testing these standards and technologies from different viewpoints, to find any issues and fix them early. Some navigation devices are already being equipped with STM capabilities, meaning they are able to converse with STM services. Finnish and Swedish icebreakers have STM capabilities in their information systems, and are actively trialing them even as I am writing this blog article. Next year will bring even more devices to play. 

### Conclusion

Information available in STM network is already being useful to supplement existing navigation systems and communication methods. Right now it's just one of the ways to cross-check information, traditional ways of working are still the main way of working at sea. But one day soon, seas will catch up with air traffic.

Improved communicaton, more efficient use of resources, less pollution, these are the short term benefits we are already enjoying. On longer term, we will probably see more intelligent algorithms taking over some of the routine work. Having more operational data available will definitely bring benefits for data analysis and larger scale optimizations as well. Hopefully future seas will be much safer than cleaner than they are today.


### Some links and rerences

- [https://vayla.fi/web/en](https://vayla.fi/web/en)
- [https://www.stmvalidation.eu/](https://www.stmvalidation.eu/)
- [http://stmmasterplan.stmvalidation.eu/improvement-phases/](http://stmmasterplan.stmvalidation.eu/improvement-phases/)
- [https://www.fuelseurope.eu/publication/statistical-report-2018/](https://www.fuelseurope.eu/publication/statistical-report-2018/)



