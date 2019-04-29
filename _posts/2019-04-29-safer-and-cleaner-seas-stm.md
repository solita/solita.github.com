---
layout: post
title: Safer and cleaner seas via Sea Traffic Management
author: arto
excerpt: Air traffic has been digitalized long ago. Now, the seas are going the same route as well. The future holds much safer and cleaner marine traffic for all of us.
tags:
- Environment
- Automation
- Digitalization
- Project
- Distributed
- Java
- XML
---
**Human errors can be expensive**. When you are making decisions and acting on them without your full concentration, mistakes are likely to happen. A typical human error might be writing your address wrong when ordering an item. You might mistype a bank account number when copying from a poorly handwritten note. Perhaps you are acting on too little information, or are in a hurry. These kinds of every day mistakes happen all the time when acting in a hurry or based on incomplete information. In most cases you can recover from them through some extra work, no harm done.

![Accidents at sea (source listed at end of the article)](/img/safer-and-cleaner-seas/marine_casualty_information.png)

Mistakes tend to be much more severe when operating a vehicle of any kind, such as a car, train, ship or an airplane. These mistakes are not just about mild embarrassment or some monetary cost. **Any mistakes involving a vehicle bring much higher costs to recover**. Sometimes they may result in environmental disasters, bodily harm, or even loss of life. 

This is why any kind of professional transportation has multiple overlapping safety controls in place to prevent any accidents. Still, occasionally things can go wrong and accidents do happen. Sometimes it is a matter of failing equipment or parts but often it can also be attributed to mistakes in judgment, not being informed enough, or trusting bad information.

### Optimization and Situational Awareness

Some of the lesser mistakes do not have such severe outcomes, but they still cost time, money, and extra fuel resources. If we were able to optimize better and avoid even smaller mistakes, it would instantly reduce the operating costs as well as benefit the environment. **Use less fuel, save some money, help save the planet**. 

Doing routine work that has to be repeated just right is a major reason for human errors. By optimizing things, we can also expect to avoid some frustration from people who are running the ships, as well as people from the port authorities' offices, pilots, ship owners, coast guard, and tugboats.

Finally, how about just improving the feeling of safety and confidence by improving situational awareness? This can be done by making sure that the people making the decisions have the right information, in the right format and at the right time. A baseline for having any information outside your ships own sensors might have been at some point, and still very much is radio traffic. Radio traffic itself is very prone to miscommunication, and things might get lost in translation. There are protocols again to cope with this, but it's still difficult to get the situational awareness just right every time. If only we had a better way...

One great part of working at Solita is that we sometimes get the opportunity to get a glimpse of the future, and even affect how it will look. These projects are the greatest because they recharge the feeling that we can have an impact; we can make the future just a little bit brighter.

### Sea Traffic Management

Sea Traffic Management is an EU wide project, currently in the validation phase. There are various goals, but at the core of it is the optimization of sea traffic across the EU. Here optimization means better efficiency, improved safety, and of course, better use of resources. 

Here are the currently listed goals for full deployment of STM by the year 2030 in relation to the year 2015:
- Safety: 50% reduction of accidents.
- Efficiency: 10% reduction in voyage costs and a 30% reduction in waiting time for berthing
- Environment: 7% lower fuel consumption and 7% lower greenhouse gas emissions.

7% might sound low, 100% would certainly be much better. But on EU-wide scale, in the year 2017, we used 37 231 000 tons of fuel oil and gasoil combined. So, using better optimization and coordination, we can still do much better. While waiting for more efficient, environmentally-friendly forms of energy to acquire wider use, optimization can bring those numbers down to more positive direction, already today. Achieve more, spend less. In other words, we are able to transport people, as well as items, cheaper than today. It is possible, instead of polluting more and more, to start polluting less and less every year. Meanwhile, new energy forms will certainly be adopted, and their use will be optimized as well, achieving further benefits.

![STM Route is shown on application screen (early draft)](/img/safer-and-cleaner-seas/fuel_consumption.png)

Of course, being able to make everyday communication and information exchange more precise, can also have a pretty large impact on marine traffic. Today, human errors cause inefficiency, delays and increased costs. More severe mistakes, of course, have the potential to cause much larger problems. Of course, computers make mistakes as well. But computer errors tend to be more systematic and predictable, and we have ways to lessen that likelihood, by applying professional software engineering principles. 

### What does Solita have to do with Sea Traffic Management?

The Finnish Transport Infrastructure Agency was, and still is participating in the STM project validation phase. The goal is to find ways to improve communications, mainly in the Sea of Bothnia. For our northern hemisphere, icebreaking operations and ice conditions create unique challenges and solutions for the STM project. A small team from Solita, among people from other software consultancies, worked together to focus on the STM validation aspect, part of a much larger project.

![Route visualization](/img/safer-and-cleaner-seas/route_visualization.png)

The technical part of what we were doing was nothing spectacular. Quite a big part of it was just moving files from one place to another, sometimes producing them, sometimes visualizing them. With the baseline being radio traffic, even this was a big improvement. The most interesting part was the constantly evolving standards, evolving goals and milestones, and how to fit all the pieces together, also in line with the special needs our northern hemisphere creates. Security was an essential facet to take care of.

STM Validation was and still is a big project, with numerous teams working on different aspects in different places. Our main focus was the ice navigation, routing through ice more efficiently, without causing merchant ships to get stuck on difficult routes, causing delays. Additionally, how to communicate with the Ice Breaker fleet so that existing pathways can be efficiently reused. All this will naturally bring great savings in both cost and environmental impact. Another aspect was digitalizing the communications between ports and vessels. This means better capabilities to estimate when a ship is going to be leaving port or arriving at a port, which can also help optimize how icebreakers will be able to assist ships. Additionally, standards can be also used to route nautical warnings and even small text messages when conversing and optimizing routes.

![Route listing and states](/img/safer-and-cleaner-seas/route_listing.png)

It is important to note that before the STM project, there had not been a great common standard for digital communications at sea when the scope is any ships within the EU. To be more precise, there had been multiple different standards before the STM project. This had led to incompatibilities and resulted in most communication being by email and radio calls. Of course this communication takes place at sea, where weather conditions might bring a few more twists on how easy it is to communicate and understand each other.

![Visual Route editor](/img/safer-and-cleaner-seas/visual_route_editor.png)

The new RTZ format for nautical routes is at its core a very simple XML schema, that can deliver basic route information, as well as some more interesting metadata. So, from any internal route models or schemas, it's possible to transform it in to an RTZ version for transport. We created some visual route editors to help with the validation. Note that this was not a part of the actual navigation tools, the main goal here was to experiment and validate. But we still had to get the turn radiuses just right, on our projected map surface.

![Turn radius calculations](/img/safer-and-cleaner-seas/turn_radius.png)

### Technical solutions

STM components and architecture are very simple, and platform agnostic. One big part is a set of standard schemas for specific messages. One of the first schemas that we were working on was the RTZ route exchange format, which allows exchanging route information in many different lifecycle phases between parties. A ship might initiate the conversation by exporting its planned route to an RTZ file, then sending it to the harbor or icebreaker for optimization. The receiving party can then apply some guidance on the route, for example advising to avoid the specific area, or rerouting via a waypoint where there's already a pathway in the ice which is suitable for the ship in question. After optimization, the new route suggestion may be sent back to the ship, then imported into the actual navigation systems for verification and usage.

Here's a simple example of RTZ route format:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<route xmlns:stm="http://stmvalidation.eu/STM/1/0/0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.1" xmlns="http://www.cirm.org/RTZ/1/1">
<routeInfo routeName="Oslo Pilot Boarding" vesselVoyage="urn:mrn:stm:voyage:id:sma:201810191046" >
<extensions>
<extension xsi:type="stm:RouteInfoExtension" manufacturer="STM" name="routeInfoEx" version="1.0.0" routeStatusEnum="1" />
</extensions>
</routeInfo>
<waypoints>
<defaultWaypoint >
<leg />
</defaultWaypoint>
<waypoint id="1" >
      <position lat="59.07503333" lon="10.57360000" />
<leg />
</waypoint>
<waypoint id="2" >
      <position lat="59.07503333" lon="10.57360000" />
<leg />
</waypoint>
</waypoints>
</route>
```

Other useful standard formats include the Port Call Message Format, and Area Exchange Format (S124), which can be used to deliver geolocation information such as a specific point or area. There's also a specification for generic Text Message Format, to deliver attachments, descriptions, or even chat messages between two parties. These together, for example, can be used to share plans and updates on port arrival or departure, nautical warnings on areas to avoid, or help negotiate an optimal route that requires some discussion. Digitraffic APIs (see link at the end) already have nautical warnings available, so we simply converted that information, and made it available via STM channels in a much wider scope.

![Testing screen showing list of nautical warnings from Digitraffic, converted to STM S124 Area standard](/img/safer-and-cleaner-seas/nautical_warnings_test_screen.png)

All of these standards can be used to replace traditional radio communication, which is very prone to human errors. Area, text and route information can be easily transported via existing simple channels, such as email attachments. Email systems are quite robust and asynchronous, so to some extent, they can also work over unreliable networks. 

However, to achieve even more robust message delivery, STM has more parts that can be used to replace any email-based communication. The STM standard defines components called SeaSwim connectors, and the Maritime Connectivity Platform. This means abstracting the communications protocol to a robust and secure platform that is able to identify parties using certificates and deliver any standards-based messages securely over the network, tolerating shaky/bad/slow/missing network scenarios. There is also a registry for services and identities, which can be used to negotiate how to communicate with a new, unknown party.

![Seaswim Connector architecture](/img/safer-and-cleaner-seas/ssc_architecture.png)

At the moment, STM is in the validation phase, which means things are still moving and evolving rapidly. There are multiple small projects testing these standards and technologies from different viewpoints, to find any issues and fix them early. Some navigation devices are already being equipped with STM capabilities, meaning they are able to converse with STM services. Finnish and Swedish icebreakers already have the STM capabilities in their information systems, and are actively trialing them even as I am writing this blog article. Next year will bring even more devices into play. 

### Conclusion

The information available in the STM network is already being used to supplement existing navigation systems and communication methods, making them more intelligent. Right now, it's used as just one of the ways to cross-check information. Traditional ways of working are still the main way of working at sea. But one day soon, marine traffic will catch up with air traffic.

Some of the short term benefits that we are already enjoying are improved communication, more efficient use of resources, and less pollution. In the longer term, we will probably see more intelligent algorithms taking over some of the routine work. Machine Learning can have its place in predicting vessel movement and optimal routes. Having more operational data available will definitely bring benefits for data analysis and larger scale optimizations as well. It seems future seas will be much safer and cleaner than they are today.

Stay tuned.

### Some links and references

- [Finnish Transport Infrastructure Agency](https://vayla.fi/web/en)
- [Digitraffic APIs](https://www.digitraffic.fi/)
- [STM Validation Project](https://www.stmvalidation.eu/)
- [Youtube: Sea Traffic Management (STM) 2018 - Status, Results and Future](https://www.youtube.com/watch?v=vutEjuR4r6c)
- [STM Validation Phases](http://stmmasterplan.stmvalidation.eu/improvement-phases/)
- [EU Wide Fuel Usage Statistics](https://www.fuelseurope.eu/publication/statistical-report-2018/)
- [EMSA Analysis on Safety at Sea](http://www.emsa.europa.eu/infographics/item/3391-what-can-we-learn-from-the-analysis-on-ro-ro-ships.html)


