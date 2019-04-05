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

Human errors can be expensive. When you are making decisions, and acting on them while not fully concentrated, it leaves room for mistakes. Typical human error might be writing your address wrong when ordering an item. Or copying single digit of bank account number wrong, from a handwritten note. Perhaps you are acting on too little information, or are in a hurry. Those mistakes happen everyday to someone. In most cases they can be recovered from by a bit of extra work, no harm done.

![Accidents at sea (source listed at end of arcticle)](/img/safer-and-cleaner-seas/marine_casualty_information.png)

Mistakes that happen when operating a moving vehicle or any kind, such as car, train, ship or an airplane, are typically much more severe. These mistakes are not just about mild embarrassment or some monetary cost. Any mistakes involving a moving vehicle typically bring much higher costs to recover. Sometimes they may even result in environmental disasters, bodily harm, or even loss of life. Doing routine work that has to be repeated just right is a big reason for human errors.

This is typically why any kind of professional transportation uses multiple overlapping safety controls in place to prevent any accidents. Still, sometimes things manage to go wrong, and accidents do happen. Sometimes it's a matter of failing equipment or parts, but often it can also be attributes to mistakes in judgement, not being informed enough, trusting bad information, etc.

### Optimization and Situational Awareness

Another interesting topic is optimization. Some of the lesser mistakes do not have such severe outcomes, but they still cost time, money, and expend extra fuel resources. If we were able to optimize better, and avoid even smaller mistakes, it would instantly be beneficial to  both operating costs as well as the environment. Use less fuel, save some money, help save the planet. By optimizing things we can also expect to avoid some frustration from people who are running the ships, as well as people from the port authorities offices, pilots, ship owners, coast guard, tugs, etc.

Finally, how about just improving feeling of safety and confidence, by improving situational awareness? This can be done by bringing the right information in right format, right time, for people who are making the decisions. Baseline for having any information outside your ships own sensors might have been at some point, and still very much is, radio traffic. Radio traffic itself is very prone for miscommunication, things get lost in translation, etc. There are protocols again to cope with this, but it's still difficult to get the situational awareness just right everytime. If only we had a better way...

Well, one great part of working at Solita is that we sometimes get the opportunity to get a glimpse at the future, and even effect how it will look like. Those kinds of projects are the greatest, because they rechange the feeling that we can have an impact, we can make the future just a little bit brigther.

### Sea Traffic Management

Sea Traffic Management is an EU wide project, currently at Validation phase. There are various goals, but at the core of it is the optimization of sea traffic across EU. Optimization means here better efficiency, improved safety, and of course, better use of resources. 

Here are the currently listed goals for full deployment of STM by year 2030 in relation to year 2015:
- Safety: 50% reduction of accidents.
- Efficiency: 10% reduction in voyage costs and 30% reduction in waiting time for berthing
- Environment: 7% lower fuel consumption and 7% lower green house gas emissions.

7% might sound low, 100% would certainly be much better. But on EU-wide scale, in year 2017, we spent 37 231 000 tonnes of fuel oil and gasoil combined. So using better optimization and coordination, we can still do much better. So, while waiting for better forms of energy to acquire wider use, optimization can bring those numbers down to more positive direction, already today. Achieve more, spend less. In other words, we are able to transport people, as well as items, cheaper than today. Possible, instead of polluting more and more, start polluting less and less every year. Meanwhile, new energy forms will certainly find their way in, and their use will be optimized as well, for further benefits.

![STM Route shown on application screen (early draft)](/img/safer-and-cleaner-seas/fuel_consumption.png)

Of course, being able to make everyday communication and information exchange more precise, can also have a pretty large impact on marine traffic. Today, human errors cause inefficiency, delays, increased costs. More severe mistakes of course have potential to cause much larger problems. Of course, computers make mistakes as well. But computer errors tend to be more systematic and predictable, and we have ways to lessen that likelihood, by applying professional software engineering principles. 

### What did Solita have to do with Sea Traffic Management?

Finnish Transport Agency was ant still is participating in STM project validation phase. Goal is to find ways to improve communications, mainly at Sea of Bothnia. For our northern hemisphere, icebreaking operations and ice condidtions are creating unique challenges and solutions for the STM project. A small team from Solita, among people from other software consultancies were working together to focus on STM validation aspect of another project.

![Route visualization (early draft)](/img/safer-and-cleaner-seas/route_visualization.png)

Technical part of what we were doing was nothing spectacular. Quite a big part of it was just moving files from place to another, sometimes producing them, sometimes visualizing them. Of course, baseline being radio traffic, even this was a big improvement. Interesting part was the constantly evolving standards, evolving goals and milestones, and how to fit all pieces together, also in line with the special needs our northern hemisphere creates. Of course, security was an essential facet to take care of.

STM Validation was and still is a big project, with numerous teams working on different aspects in different places. Our main focus was the ice navigation, routing through ice more efficiently, without causing merchant ships to get stuck on difficult routes, causing delays. Additionally, how to communicate with Ice Breaker fleet so that existing pathways can be efficienctly reused. All this will naturally bring great savings in both cost and environmental impact. Another aspect was digitalizing communicatons between ports and vessels. This means better capabilities to estimate when ship is going to be leaving port or arriving to port, which can also help optimizing how icebreakers will be able to assist ships. Additionally, standards can be also used to route nautical warnings and even small text messages when conversing and optimizing routes.

![Route editor](/img/safer-and-cleaner-seas/route_editing.png)

![Visual Route editor](/img/safer-and-cleaner-seas/complex_route_editing.png)

You have to note that before the STM project, there had not been a great common standard for digital communications at sea, when scope is any ships within EU. To be more precise, there had been multiple different standards. But this has lead to incompatibilities, and caused all communication in most cases preferring radio calls and freeform emails. Of course this communication takes place at sea, where weather conditions might bring a few more twists on how easy it is to communicate and understand eachothers.

![Route information available in systems](/img/safer-and-cleaner-seas/route_and_vessel_popup.png)

New RTZ format for routes is at its core a very simple XML schema, that can deliver basic route information, as well as some more interesting metadata. So from any internal route models or schemas, it's possible to transform RTZ version for transport. We created some visual route editors to help with the validation. Note that this part was not actual navigation tools, main goal here was to experiment and validate. But we still had to get the turn radiuses just right, on our projected map surface.

![Turn radius calculations](/img/safer-and-cleaner-seas/turn_radius.png)

### Technical solutions

STM components and architecture are very simple, and platform agnostic. One big part is a set of standard schemas for specific messages. One of the first  schemas that we were working on was rtz route exchange format, which allows to exchange route information in many different lifecycle phases between parties. Ship might initiate conversation by exporting their planned route to rtz, then sending it to harbor or icebreaker for optimization. Receiving party can then apply some guidance for the route, for example advising to avoid specific area, or reroute via a waypoint where there's already a pathway in ice, suitable for ship in question. After optimization, new route suggestion may be sent back to ship, then imported into actual navigation systems for verification and usage.

Few of the other useful standard formats are Port Call Message Format, and Area Exchange Format (S124), which can be used to deliver geolocation information such as specific point or area. There's also specification for generic Text Message Format, to deliver attachments, descriptions, or even chat messages between two parties. These together allows for example to share plans and updates on port arrival or departure, nautical warnings on areas to avoid, or to negotiate an optimal route that requires some discussion. Digitraffic already has excellent APIs making nautical warnings, so we simply converted that information, and made it available via STM channels in a wider scope.

![Testing screen showing list of nautical warnings from Digitraffic, converted to STM S124 Area standard](/img/safer-and-cleaner-seas/nautical_warnings_test_screen.png)

All of these standards can be used to replace traditional radio communication, which is very prone to human errors. Area, text and route information can be easily transported via existing simple channels, such as email attachments. Email systems are quite robust, and asynchronous, so to some extent they can also work over unreliable networks. 

However, to achieve even more robust message delivery, STM has more parts that can be used to replace any email based communication. STM standard defines components called SeaSwim connectors, and Maritime Connectivity Platform. This means abstracting the communications protocol to a robust and secure platform that is able to identify parties using certificates, and deliver any standards-based messages securely over network, tolerating shaky/bad/missing network scenarios. There is also a registry for services and identities, which can be used to negotiate on how to communicate with a new, unknown party.

![Seaswim Connector architecture](/img/safer-and-cleaner-seas/ssc_architecture.png)

At the moment, STM is at validation phase, which means things are still moving and evolving rapidly. There are multiple small projects testing these standards and technologies from different viewpoints, to find any issues and fix them early. Some navigation devices are already being equipped with STM capabilities, meaning they are able to converse with STM services. Finnish and Swedish icebreakers have STM capabilities in their information systems, and are actively trialing them even as I am writing this blog article. Next year will bring even more devices to play. 

### Conclusion

Information available in STM network is already being used to supplement existing navigation systems and communication methods, making them more intelligent. Right now it's used just as one of the ways to cross-check information. Traditional ways of working are still the main way of working at sea. But one day soon, marine traffic will catch up with air traffic.

Improved communicaton, more efficient use of resources, less pollution, are some of the short term benefits we are already enjoying. On longer term, we will probably see more intelligent algorithms taking over some of the routine work. Having more operational data available will definitely bring benefits for data analysis and larger scale optimizations as well. It seems future seas will be much safer than cleaner than they are today.

Stay tuned.

### Some links and references

- [Finnish Transport Agency](https://vayla.fi/web/en)
- [Digitraffic APIs](https://www.digitraffic.fi/)
- [STM Validation Project](https://www.stmvalidation.eu/)
- [Youtube: Sea Traffic Management (STM) 2018 - Status, Results and Future](https://www.youtube.com/watch?v=vutEjuR4r6c)
- [STM Validation Phases](http://stmmasterplan.stmvalidation.eu/improvement-phases/)
- [EU Wide Fuel Usage Statistics](https://www.fuelseurope.eu/publication/statistical-report-2018/)
- [EMSA Analysis on Safety at Sea](http://www.emsa.europa.eu/infographics/item/3391-what-can-we-learn-from-the-analysis-on-ro-ro-ships.html)


