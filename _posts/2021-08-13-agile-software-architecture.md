---
layout: post
title: How to do agile software architecture right
author: arto
excerpt: >
  Software architecture can be hard to get right - let's see if we can see what would make it awesome, especially in agile projects.
tags:
 - Software Development
 - Architecture
 - Software Architecture
---

![Code monkeys at work](/img/agile-software-architecture/code_monkey.jpg)

**Any monkey can write code, right?** There, I just said it. Monkeys can actually write code, [see infinite monkey theorem](https://en.wikipedia.org/wiki/Infinite_monkey_theorem). Given enough time, they would randomly write a for-loop, then a working piece of code, then something that actually meets the requirements. Of course, given perfect specifications, you could just apply a bit of **GPT-3** or **Github Copilot** instead and accelerate things somewhat.

There's also a term called [Code Monkey](https://en.wikipedia.org/wiki/Code_monkey) for programmers that just implement perfect specifications and do not use their own brains at all. Honestly, I don't know any coders like that and have never met one if such a mythical thing actually exists. This is because typically having perfect specifications is an illusion. And even if there would be such a thing as a perfect specification, communicating that 100% accurately to another person would be a hard task.

## How to do the requirements right

The moment when we understand the least of how we should specify the requirements is the moment when the project begins. Yet there used to be old models for software development such as waterfall, where the idea was to first do specifications and design, then implement everything, and only then finally test everything. This model would be perfect if you want to sate the code monkey model, but in real life, it's been tested and found lacking.

This is because it's very hard to get even the requirements right when dealing with change. We start by having an idea of what we need - it might be a new product, new service, or just a new version of an old one that needs to be done. But then real life happens. And instead of getting what we need, we get what we deserve.

## What's the problem?

- Business needs might or might not be perfectly understood. Did we have a coherent vision of the business owners' needs? Did we really perfectly capture the end user's wishes, dreams, and needs? Or should we start with an MVP, a pilot program, or some A/B mocks first? If we started with one of these, was it enough? We need to test and validate those ideas, and we need to prioritize them too.
- Did we capture and foresee all non-functional requirements perfectly in the beginning? Did you take care of usability, accessibility regulations? How did the architecture cope with current GDPR regulations and user rights? Is it eternally scalable, reliable, observable? Did you understand all these needs from the beginning, and everyone participating understood them 100% the same way?
- Technologies might or might not have evolved, changed. Does the one who writes the specifications really have a perfect up-to-date understanding of how to apply the latest version of AWS services, or Java 17, or React (insert whatever version is popular this week here). 
- We don't always want to use the latest and greatest of everything, but we should apply the things that improve life, and not always use the ancient dusty tools either. Happiness is found in a good understanding and a perfect balance.
- Even if the technical understanding was perfect, how about if the project takes more than a few months, even years, and technologies evolve and get refined. Should we never revise them? Even if we keep on running the software for a decade?
- Was the architecture built as part of the organization's enterprise architecture model? Did it need to be? If so, what happens when the enterprise architecture is revised and evolved?

What I'm aiming for here is a popular concept in agile development: An **emergent architecture**, a flexible architecture, that responds to our current needs. Needs are defined as point-in-time, not set in stone and worshipped forever. Needs come from various directions. You start with something good enough to carry you onwards for some time (architectural spike), and might even get you all the way to the end. You keep it as simple as possible while meeting the needs. But when it's later challenged by new needs, you can revise it and add just the minimum of complexity to meet those needs.


Note that emergent architecture alone is not a guarantee that it's good architecture: It can be accidental architecture, too complex, or not meeting the original needs at all, or just overall incohesive and bad. As all things and ways in life, this requires skill to get right.

## Agile teams and architecture

Agile teams are typically composed of skilled and empowered developers, who have multiple talents. With an experienced team, you would typically have multiple people with overlapping skills for coding, but also design, security, and yes, architecture. It means the team is involved in the evolution of architecture, not someone outside the team in a high ivory tower.

![Architecture brainstorming](/img/agile-software-architecture/architecture.jpg)

This will also happen if there is no skilled or experienced team, by the way. Coders will need to interpret the architecture, and if there is no architecture, to begin with, they will of course wing it without meeting any other needs than to have code doing what it is asked to do. In that case, architecture will just happen.

## What is a good software architecture like then?

It's minimalism. There's an endless stream of potential needs to apply. So a bad architecture might be a book so long nobody would have time to read it or grasp it. Excellent architecture can recognize and meet the core needs in a minimally described fashion so that everyone in the team can understand and apply it. Start with just one page, try to distill the guidelines. Go deeper when there is good reason to do so. Test that minimalism every time a new person joins the team. Are they able to read it, understand it, apply it? Less is more, and a good picture goes a long way.

To achieve minimalism, a good architecture does not try to reinvent the wheel - it leverages existing standards and references that are already defined and accessible. Examples of this might be Java EE technologies and architectural guidance (Even if it sounds like enterprisy), or .NET reference architectures, or AWS Well Architected. Any language or platform has its own natural ways to do things, try to rather leverage them than fight against them. That way your architecture will require less documentation, and instead can point and refer to standard sources people can read, and are used by thousands of other teams perhaps.

![A whiteboarding session](/img/agile-software-architecture/whiteboarding2.jpg)

It's flexibility. Good architecture can expand to meet new needs or directions that are discovered over time, can grow, while still maintaining the original qualities. Good architecture can be expanded by more than one person, by the team as they continue working on it.

Good architecture stands the test of time. I've sometimes argued that you can get away coding for one year with any architecture, even a bad one or no architecture whatsoever. The quality of architecture only becomes more visible over time. Is it easy to apply? Is it easy to expand? Does it still work, or do the coders ignore it and go around? Does it give useful guidance? None of these things matter so much in the first months when there's not yet so much code. But later on, when the amount of code grows, time pressures start piling up, the architecture will be tested.

Good architecture also goes beyond the initial project phase, it extends to when software is actually running in production and the initial project has ended. Instead of active development, there's a minimal (or less minimal) team running the software for years to come, needing to do bugfixes and minimal changes in response to change in the world around it - is it still easy to find the places to fix, get the fixes applied, and expand the software?

Good architecture is followed, instead of circumvented. If the development team feels the need to constantly go around it and now follow it, it should be revised if it's actually unrealistic architecture, or misunderstood. Typically when people are not following any architecture, this is when we start seeing multiple approaches to do the same thing - which will start making it harder to understand and make changes to the software. 

A good way to check for this is using the code reviews - and make sure they are just not the superficial 'LGTM' type, but actually verify that the reviewed code is minimal and elegant answer to need and architecture. Sometimes it might also be possible to automate some checks, especially on the security side of things. 

A fine line here is: What is productive automation, and what is not. Code reviews are great because it's not only a check, it's also education, so hopefully, good patterns and details are picked up and shared across the team, bad ones are caught early and wither away.

## Conclusion

Is it possible to capture perfect requirements, specifications, and design, before starting to code, and never need to revise them? And what does good architecture mean for you? What is the benefit of having architecture vs just winging it? Are all architectures eventually bad, they just look good in the beginning when things are easy? What do you think?

