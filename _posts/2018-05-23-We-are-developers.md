---
layout: post
title: We Are Developers
author: arto
excerpt: A tale of a conference trip to We Are Developers in Wien
tags:
- conference
- developers
- AI
---

## We are developers

![Ready to attend](/img/we-are-developers/badge.jpg)

I had the opportunity to attend to We Are Developers, a developer conference in Wien, with more than 8000 attendees. Unlike many other conferences I have been frequenting, this one is not centered around any specific technology. It also has very wide scale of presentations. There were sessions on oauth2 and vue.js details, even a session called 'Stupid tricks with enums'. On the other hand, there were panel discussions on topics of AI ethics, or how to deal with burn-out and stress at intensive workplaces. Other than making it necessary to check very carefully which sessions I was attending, I found it very interesting to be able to change the abstraction level and attend many sessions I did not have any previous knowledge of.

![We are developers!](/img/we-are-developers/overview.jpg)

Wien was a very interesting place to visit - my first time there. It was a suprise to figure out it's the 6th largest city in Europe, ahead of Barcelona for example. There were not a lot of high buildings either, whole city was filled with old buildings of moderate height. Graffiti and street art on the other hand was abundantly present everywhere. Conference attendees included a large number of developers and recruiters from nearby places such as Berlin.

### The nicer Steve

There were also some amazing, legendary speakers. Conference opened up with Steve Wozniak, and topics ranged again very widely. It was fascinating to hear stories of days that predate even my own first steps in development - and you could sense the passion and excitement and full-on nerdism that fuelled the fire that changed the world. 

![The nicer Steve](/img/we-are-developers/woz.jpg)

But equally interesting was to hear his thoughts, from this unique perspective, on modern topics such as Blockchain, Bitcoin, and of course AI. I have been avoiding the term AI myself, since I don't think any of the systems around today are even remotely something that I would classify AI. There's a lot of machine learning going on, but AI is something entirely different. It will surely happen, but we're not there yet. Woz put it to words better than I could ever have: Current machine learning algorithms learn by observing masses of data, for example to learn what is a dog. Yet a child only has to look at one to learn its characteristics. Even the best machine learning algorithms operate very differently than human brain. There are some experiments that are farther: But they are typically operating on very narrow field of expertise, and still pretty stupid, compared to a human mind. 

On blockchain technology, Steve Wozniak was comparing it to big IT bubble of the 2000: it is awesome technology, but possibly living now more hype than actual usage, and it will be huge in ten years' time. It fascinates technical people because of aesthetics - it feels logical and right. But right now, it's typically slow, and only used in few special cases, namely e-currency.

![Mr John Romero and the original Doom chainsaw](/img/we-are-developers/romero-chainsaw.jpg)

John Romero was reminiscing some good old days of game development, including 3.5" disks-based version control system. There was less stuff relevant for today, but I liked one of the reflections: If the team is not playing the game themselves, it's not very good. Eat your own dogfood, folks. An ancient rule, still often not followed.

### Ethics of AI

I had the pleasure of attending many sessions that dealt with autonomous processes and machines, and machine learning. Michael Fausten from Bosch gave an excellent session on self-driving cars, including the challenges, capability levels, and even how their agile process works. One of our own, Lassi Kurkijärvi, gave a brilliant speech on Human/AI Partnership. 

![Reshaping our lives](/img/we-are-developers/lassi.jpg)

We are living in an age where anything is possible. There are rarely any limits on what can be done with today's technology. This causes us to reflect more and more on ethics of automation and AI. It is very tempting to use automation and machine learning to make manual processes more predictable, and lightning fast, optimizing how the world churns around us. But automation taken too far can be also frightening, since errors or unforeseen situations can cause chain reactions at a speed that can't be followed by mere flesh. This has already happened and will happen again. Also, machine learning is very powerful tool, and can be used as force of evil just as easily as force for good. We will keep pondering which choices make the world a better place instead worse, and how far to take automation in each case. That's why I prefer to think of these as tools to assist human beings, with suitable safety controls in place. 

![Autonymous vehicles](/img/we-are-developers/auto-auto.jpg)


### Quality, security and privacy

There were some interesting talks from current or previous employees of companies like Facebook, Twitter, and Netflix. Many of them dealt with how to handle scalability of work when application you are working on is huge. Other good topics were on security and privacy - you could hardly walk 100 meters without hearing people discuss who should own the data collected from smart automobile, or how should one handle third party dependencies that can include sophisticated attacks. I was not able to find much of a coherent summary on this topic but got a lot of tiny details and a lot of confirmation on some thoughts of my own. I feel, along with many others, that we need to raise the bar of these things in the future. Privacy does not happen before you have security and good quality for software. Since all of these cost money, best way to approach that is to automate it to the best extent you can. It's time to move from automated unit and integration tests onwards to automated security tests and automatically generated privacy documentation. All these need to be taken care of as part of continuous development.

![New World Order](/img/we-are-developers/anonymous.jpg)


Another talk that resonated with me was one on DevSecOps practicalities. Many people think that doing DevOps or DevSecOps means hiring these expensive and rare unicorns, and they will magically make software become beautiful. I believe more in making sure there are no silos between these roles, and there's really more than one way to do that. Talented people working on software is one of those ways, yes, but there's also often a situation where they simple cannot resolve everything within their own team, then it becomes more importantly about common tooling and excellent communication channels, doing things together, yes on same desk. Rapid feedback cycles that reach all involved parties. At my best I have been able to reach this, or help others reach this level - but it is never easy, and it's never 'done'.

![Ready to automate!](/img/we-are-developers/robot.jpg)

![Uber DevOps](/img/we-are-developers/uber.jpg)

I attended also an excellent session by an Uber engineering team member. Uber has a huge system now, more than 2500 developers, more then 3000 microservices - actually nobody knows the total count. They have also grown very rapidly. The service dependency chart is out of this world. I mean literally, it looks like a galaxy map. Their business is one where any service disruption will immediately start leaking a lot of money, so they do 24/7 operating by development team, in full DevOps fashion. The speaker mentioned it was not so much controlling the chaos, but surfing it. It's a challenging environment, and often they just have to 'wing it' - but they do it with help of superior processes, practices and tools, and have fun with it. When you get woken up at 4am because nobody can order a car, you truly appreciate having good runbooks and tools at your disposal.

### Concrete technologies

I attended on some very concrete sessions as well, to balance things out. It seemed every other topic was on Vue framework, current favourite of our front-end coders. Vue is pretty clean and lightweight web framework, does its job well, so it's earned its place. One session I enjoyed a lot was future of end-to-end testing, using Cypress. E2E testing has always been valuable, but also hard to maintain, and I feel there's a new step in natural evolution with Cypress. They also have ambitious roadmap on even more interesting things, like load balancing tests for speed, and making user manuals from test videos.

![Enterprise Angular - threat or possibility](/img/we-are-developers/enterprise-angular.jpg)

![Google](/img/we-are-developers/google.jpg)

![Future of testing a Cypress](/img/we-are-developers/testing-future.jpg)

Google had pretty good insights on future of the web. We have moved from webs on desktop to responsive web that works on desktops and mobile devices. Now we are making a new transition to mobile first, and in some cases even only mobile web. This is getting incentivized by Google - search engine rankings are resolved from the mobile view, and include measurements of speed as well. Where Google is going, will have huge effect on almost any work done in web. There's also new tooling available, including The Chrome User Experience Report. All in all, you will be penalized for having desktop-first, slow, unresponsive websites, especially over unsecure http connections.

![ESLint for code quality](/img/we-are-developers/eslint.jpg)

There was some good ideas on areas of quality, and scaling the app size, including tools like eslinter, standard, and monorepo model. I think there was more emphasis on front-end tools and technologies than back-end. But this was quite okay for me, there's more movement in front-end right now. Well, at least until Java 11 hits the decks.

## The hype words

There is a lot of buzz on blockchain, but most of its uses still lie in cryptocurrency domain. There is now some toying on other uses of single truth-ledger, including contracts and marketing, but... for me it mostly seems like instead of trying to find good technology to solve a problem, people are looking for good problems they can solve with blockchain. And that is not cool at all.

![AR Crash Simulator](/img/we-are-developers/ar-crash.jpg)

It seems everyone was doing micro-services, and most popular technologies (in presentations and workshops) seemed to be Kotlin, Vue.js, Angular, and Docker. AI was everywhere, so much that anything without AI in it seemed really weird. Devops was everywhere, too. Being a hype word does not equal useless (unless it's blockchain) - but trends do follow a certain pattern. For me it seems that we're now past the craziest microservices and DevOps hype, and living now actual adoption phase, where there's less hype, and more actual things done with them.

![Hololens](/img/we-are-developers/hololens.jpg)

Oh, and Hololens. I love the Hololens. Not sure if it has or will have any relevance to my work, but AR is pretty cool and fun stuff. Would love to do a project on it. Hardware is getting better and better every year.

### The future of development

Last day in conference was the best for me. I had no expectations, so just went where my nose led me. There was a lot less attendees due to a big party previous night, and being last day of conference, so it was much easier to get in any sessions I wanted to. Days best session by far was the one called 'What is work and What is Human - In a Superhuman Future' by Martin Wezovski from SAP. He is an excellent speaker, and since his job is to try to imagine what lies in future for us, it pays to listen to his visions. 

![Conference room](/img/we-are-developers/room-a.jpg)

Of course, predicting future is very hard, we can predict the near future pretty well, but when advancements build on advancements it gets really hard to see what disruptions the future will bring. Neverthless, this presentation was very entertaining to watch, and gave some insights to how our world and work would look like 30 years from now. Theme was also creating superhuman by having machines and automation do the boring stuff - this is the line I've been preaching for an eternity, being a crazy automation geek myself. But this presentation also dealt with some ideas on how to survive this transition. I'm not going to write any piece-by-piece analysis on the details, if you got interested, better watch the original ;)

![Where are we heading?](/img/we-are-developers/mankind-future.jpg)

But I will summarize a bit. Routine jobs and processes will become automated. People will still excel in some areas, where AI is not so good. One of them is strategy. Machines are very good at tactical decisions, but not so good in strategy, because that is traditionally the unknown domain, which cannot be calculated and deducted. Well, at least not until we have actually intelligent general purpose AI - which does not exist today. People are very good at collaboration (on average), on empathy, which are difficult traits for machines to learn. On the other hand, currently if we think of efficient worker, we would probably think of someone who's a fast learner, a diligent worker, and can scale his work well to demand. These are traits that make you very easy to replace by automation in the future. So if you want to become irreplacable, better perk up those communication and empathy skills of yours :)

### Conclusion

We are living very very excited times, and I'm very happy to be working in this industry right now. There's a lot of positive buzz going on, and a lot of ambition on what we can do. I like ambition - you should always aim rather higher than lower, and aim to always improve a bit, as opposed to just repeating yourself. This is how we can find the excitement and inspiration from our work. Always keep on learning, always keep on improving. Make the world a little bit smarter and better place every day.

Videos are not yet released, as of writing this, but will be any day now.


### Some links and pointers

- [https://www.wearedevelopers.com/congress/](https://www.wearedevelopers.com/congress/)
- [https://www.wearedevelopers.com/program/](https://www.wearedevelopers.com/program/)
- [https://developers.google.com/web/tools/chrome-user-experience-report/](https://developers.google.com/web/tools/chrome-user-experience-report/)
- [https://vuejs.org/](https://vuejs.org/)
- [https://www.cypress.io/](https://www.cypress.io/)
- [https://kotlinlang.org/](https://kotlinlang.org/)
- [https://www.docker.com/](https://www.docker.com/)
- [https://www.microsoft.com/en-us/hololens](https://www.microsoft.com/en-us/hololens)





