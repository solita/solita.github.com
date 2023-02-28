---
layout: post
title: FooConf 2023 Helsinki
author: teepeltola
excerpt: A blog post about the new emerging Finnish developer conference, FooConf 2023 Helsinki, held 1.2.2023
tags:
  - fooconf
  - software architecture
  - cloud
  - DevOps
  - cloud native
  - conference
---

## Arriving

We got a chance to participate in a new conference called FooConf in Helsinki, on the 1st of February. The conference was organized by the developer community and by some of the same organizers behind the famous JFokus conference held in Sweden annually.

There were two of us Solitans, **Teemu Peltola** and **Markus Visti**, from the Turku office, participating. The alarm rang at five, so it was an early start. The bus ride, sponsored and organized by Vaadin and Qalmari, started from Turku bus station at 6:15.

![paste](/img/2023-fooconf/fooconf2023_1.jpg)
_Bus start_

We arrived in Helsinki at about 8:30. The venue for the conference was Helsinki Congress Paasitorni. The conference program and the speakers were well-known in the developer community. The program can be found [here](https://www.fooconf.fi/schedule). There were some common talks for everyone but otherwise, everyone was able to choose the speakers during the day from three different tracks.

![paste](/img/2023-fooconf/fooconf2023_2.jpg)
_T-shirts_

## Talks

The day started with some welcome words by the organizers and after that, there was the first keynote speech of the day, Learning by Tinkering by **Tom Cools**. The speech was about learning and how to keep up with the ever-evolving technologies. The key takeaways of the speech were:

- Limit yourself (do not take on all new tech in the same project)
- Focus on the concepts that don't decay as fast, like Object Oriented Programming, Functional Programming, TDD, DDD, Design Patterns and Clean code
- Reflect (check your pet projects in GitLab, check what went wrong)
- Be conscious about your learning goals (stick to your plan)
- Alternative approaches (do the same thing many times with another tech/lang, e.g. machine learning)
- Share what you learned!
- Do good
- Be yourself

The speech was really interesting and provided something to think about. The topics covered were common to many developers.

![paste](/img/2023-fooconf/fooconf2023_4.jpg)
_Learning by Tinkering By Tom Cools_

After the first speech, we took some different tracks. Teemu listened to Cloud-native dev tools by **Grace Jansen** from IBM. It was a good introduction to OSS Java cloud-native technologies like Open Liberty, MicroProfile, Jakarta EE, testing (TestContainers, Microshed) and deploying (Buildpacks.io, Paketo buildpacks, Telepresence). It was a good overview and something to check for future projects as well. Nice demos, tips and tricks. Good to check slides for more information and links.

Markus went to listen to the speech about JavaScript frameworks of tomorrow by **Juho Vepsäläinen** of Aalto University. The speech presented first the past and current trends in frameworks but quickly went on to prospects and the idea of Transitional Web Applications (TWAs). The main goal is to minimize the amount of loaded JavaScript and increase the amount of static content on pages, leading to more efficient web applications. Two approaches of these were introduced: the Island Architecture (11ty/is-land, îles, Capri and Astro -frameworks) and Resumability (Qwik-framework), and demos for Astro and Qwik were shown. Juho also presented his Ph.D. project called Gustwind (with side projects), which is using JSON as the building block for web applications.

Next in line for Teemu was a very nice speech about how a Legacy app went to serverless bar by **Sébastien Blanc** from Aiven. It was a humorous story featuring a 13 years old legacy app called Bob which wanted to go cloud and serverless. The story included funny characters like Join the table, Maria, Kafka river etc and ended up in an Aiven product demo, about serverless, Kafka, Kubernetes and autoscaling.

![paste](/img/2023-fooconf/fooconf2023_5.jpg)
_Legacy app went to serverless bar by Sébastien Blanc_

Let’s do a thing and call it Foo by **Maaret Pyhäjärvi** was next in line for Markus. It was a speech about how to approach testing, which was defined as “Find (some of) what others may have missed”. The main takeaways from the speech were: testing is the responsibility of the whole team (even a team with designated testers), KNOW the domain where the application will be used (e.g. in clocks number 4 in roman numerals is IIII not IV) and choosing the right level of test coverage. Finally, the speech gave some useful insights from Maaret's own experiences in testing.

After lunch, we both listened to the speech about Security by design by **Daniel Deogun** from OmegaPoint. It was about how to implicitly write safe software by going through the log4j vulnerabilities as an example. We learned that good design mitigates risks but not fully. There was a good discussion about what is safe and what is not.

![paste](/img/2023-fooconf/fooconf2023_6.jpg)
_Security by design by Daniel Deogun_

Teemu continued with a speech about Apache Pulsar, an event streaming platform by **Mary Grygleski** from DataStax It started with the basics of event streaming and went through the details of Apache Pulsar. Interesting speech which also discussed how Pulsar relates to Kafka, which can be used as a bolt-on with Kafka

Markus listened to **Leif Åstrand** from Vaadin about Why and How to build a Collaborative UX. The speech was a presentation of the experiences of Vaadin on how they have tackled the issues when a collaborative UX is needed. Starting with use cases the speech went on to describe the architectural decisions to consider. The speech ended with a discussion about clustering in collaborative apps and how to implement a “distributed system without building a distributed system”. The speech provided good ideas for Markus which might come in handy shortly in his project work.

Next in line for both Teemu and Markus was a speech called Devops that matters by **Melissa McKay** from JFrog. It was a discussion about starting with DevOps from a developer's point of view. Some of the common problems of dev teams and operations were discussed. It was emphasized that DevOps is a mindset from code to deployment and back. The most important takeaway from the speech was that silos should be eliminated! Melissa gave many useful practical tips.

![paste](/img/2023-fooconf/fooconf2023_7.jpg)
_Devops that matters by Melissa McKay_

Then it was time for the last speech of the day, Thinking Architecturally by **Nate Schutta**. It was a truly humorous speech about software architecture. Nate is an experienced speaker and the speech provided some insights into everyday work in a very humorous way. There were some common themes with the first speech of the day by Tom Cools as Nate also emphasized the importance of constant learning and focusing on the core skills instead of learning all the new shiny technologies. We should learn from good and bad decisions. It was also repeated that we should be kind to ourselves.

![paste](/img/2023-fooconf/fooconf2023_8.jpg)
_Thinking Architecturally by Nate Schutta_

# Afterparty and summary

After the conference, we had some drinks in the Foo Bar. It was nice to have a chat with some of the speakers and hosts. After some drinks, it was time to get back to Turku.

![paste](/img/2023-fooconf/fooconf2023_9.jpg)
_Some drinks after the event at Foo Bar_

The conference was very well organized and we hope that it will be organized again next year! We highly recommend attending these kinds of events, since they give you new ideas and you can learn about new technologies and take them into your projects.

Solita supports and encourages its employees to attend conferences both in Finland and abroad. This is super cool and gives you lots of possibilities to keep you up to date with current technology and trends.

## Links

- [FooConf site](https://fooconf.fi)
- [FooConf program and links to speaker slides](https://www.fooconf.fi/schedule)
