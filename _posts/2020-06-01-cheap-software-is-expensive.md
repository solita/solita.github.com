---
layout: post
title: Cheap software is very expensive
author: arto
excerpt: >
  Tailored sofware can be done very quickly by cutting corners and doing things dirty - it might not bring you the happiness you seek however
tags:
 - Development
 - Tailored
 - Custom
 - ROI
 - Competitiveness
---

How much does an algorithm cost? What's the work estimate for function that calculates value-added tax for a price? How many euros does it cost to produce? Does not sound too complicated, right? Any monkey could write that function within within one hour of good concentrated work, right?

![Things always start simple](/img/cheap-software/simple.jpg)

Wrong.

This article is not about getting a good bargain for a software product. This is also not about doing stuff with great existing components, or using a low-code/no-code approach to solve a repeating problem with a reusable answer. This blog is about being careful with the invisible costs of piling features on top of eachothers, and using any and all shortcuts to get there.

## Total cost of bugs

Let's start with bugs. The origin of the word comes from actual insects, getting stuck inside complex machinery. Nowadays, instead of insects, we have programming mistakes or oversights. They tend to hide within imprecisely communicated requirements. They feed on added complexity, and they reproduce within human's imperfect mind. Human brain works on varying levels of efficiency, depending for example on caffeine levels in blood, ability to concentrate on a task, and of course on what is the general motivation at the moment.

![Spot the bug?](/img/cheap-software/complicated.jpg)

In other words: Sure, you can write an iteration of the code in 15 minutes. But it might have a bug or two, a blind spot where it fails to work. VAT is pretty simple algorithm - perhaps you copied it from the vastness of the Stackoverflow, congratulated yourself, and moved on. And now that off-by-one error or bad rounding rule due to using double type for money caused a massive mistake in one time payment, or huge accumulation of small errors over months and years.

What I'm pointing out here is that everyone makes mistakes. People are imperfect, even the most perfect ones. They are easily distracted, by any interruptions or even own worries and desires. Average coder has about 15 minutes of clarity a day, during which perfect code is made. Rest of the day is filled with sneaky bugs.

There are some bugs in history of computer sciences that had a really devastating cost. For example year 2k bugs - relatively small things, people cutting corners, then realizing it is too big an issue to be fixed within normal coding, so they kind of decided to avoid thinking about it. Eventually it needed fixing, and estimated cost of those fixes and issues that were left unfixed was in the ballpark of 500 billion dollars. For example Mariner 1 spacecraft - minor bug caused destruction of 18.5 million dollar in an instance. Fortunately Mariner 2 worked better. Mars Climate Orbiter in 1999, NASA used metric system, Lockheed Martin used imperial units. Result: Probe lowered 50km too low, collapsed in atmosphere, and burned 193 million dollars of money in an instant, not to mention original scientific work that was planned. 

## Making the bugs cheap

Fortunately there's an easy answer to making bugs much cheaper. It's rapid feedback loop. How much does a bug cost? Depends on when  it is found.

- I found it immediately while writing the code, because I was caffeinated and had my spart pants on. Price of bug: 0$ (not counting the pants and coffee)
- My teammate noticed the bug when we were pair programming the algorithm. Price of bug: Still pretty much 0$ - of course pair programming costs money, too, unless two heads are together more productive alltogether than  two separate ones.
- My relentless TDD principles caused me to detect the bug when I was writing the unit test for the algorithm. I wrote another test to catch the bug, then wrote some code to fix it. Cost: perhaps few dollars now, I do have to spend a bit time to write code and tests. On the other hand, tests create specification of how I intended the code to work, so it might work as a documentation as well.
- Our QA team knows how severe bugs can be, and they have great mind for finding ones. They found this one. However, it now took longer, so fixing the bug is bigger task, I need to coordinate the releases, write some tickets and explanations, have the fix retested, do handoffs, etc. Let's say price if a few hundred bucks here, or more if process is not optimal and I have to do task switching a lot.
- Bug got to production environment, and caused an incident immediately. Cost is pretty much same as above, but since this was triggered by angry customer feedback, this just became more severe and heavy fix, so add zero to costs. Also, these bugs come with PR cost as well: Lots of severe bugs, or not hardly any bugs? Add another zero to cost.
- Bug got to production environment, but was sneaky enough to only be detected a lot later, like in the above examples. Cost just went up again. It may have caused havoc already, that's hard to fix. Fixing the actual bug can also be more expensive, first one needs to find it, understand it, and fix it. It might be that development has ended and team has moved on, and now new people are frantically trying to find/read/understand any documentation left over. Do we have a working automation going on, or is fixing bugs probably going to cause new bugs? Add as many zeros as you like.

So you probably got the point. It's cost-effective to fix bugs early. Lots of agile principles, especially ones from Extreme Programming origins, can help with that. Talented engineers these days apply them because they understand this. 

But what just happened to work estimates that we started this article with?

- How long it takes to write the code?
- And to include the test automation that is satisfactory?
- And to make sure we also have good coverage?
- And to refactor it, so architecture stays clean, readable, and something we can expand?
- And to pair program or pair review the code, so that every line is checked by four eyeballs instead of two?
- To make sure that the documentation is satisfactory so it can be maintained by other teams when necessary?
- To make sure we have continuous deployment capability, both technically, and process wise, so that we do not have to fear making changes, fixing bugs and refactoring code that's already being used
- To make sure code is secure by design: Not having vulnerabilities to obvious well known attacks since sql/xml/javascript/whateverinjection, cross site scripting, etc. It's much cheaper to audit/hack yourself constantly than to wait for external audit, a lot of handoffs and task switching later.
- To make sure GDPR privacy rules are being followed, not broken. Cost here can be up to 20 million euros or more, much more.

So, what's the realistic estimate now for that component? And which one would you rather buy? There is probably good middle-ground to be found, depending on what problem the software is trying to solve. But no matter what is the need, I would not myself be tempted to try luck-driven development.

So in the end it is about balancing money, time, and features. But also how well you want those features to be done.

## Lifecycle of a software solution

One important thing to consider is of course the lifecycle expectency of your software solution. If you are writing something that is expected to be used for few years, or for few decades, cost ratio of development to operations is very different, and then decisions you make on the quality and flexibility might be, as well. It might be ridiculous to try to cut corners during the development, if that cost is a fraction of total cost to run the software. If we are creating something that should be around for long time, it's especially important to avoid cutting too many corners, and instead create something that at least starts its life clean, refactored, documented, easy to understand, easy to modify, easy to maintain.

I've sometimes been tasked to create software purely for a marketing campaign, that is expected to run for limited amount of time. Perhaps after that, some parts can be recycled to a new campaign, but in those cases it was not necessary to keep it clean, so ... go wild, I guess. Put that cowboy hat on and forget about refactoring and test automation. Other times, I've been involved in some POC projects, where we want to build rapidly and cheaply something that proves just enough to get the funding and vision for the real thing. Again, make it quick, make it dirty, as long as everybody understands that and is not stupid enough to use that steaming pile of ugliness as basis for the real thing - just recycle the ideas, vision and convication, and keep the codebase ugly.

So understand your lifecycle, are you creating a product, are you creating a long-running service, or a quick-and dirty demo/poc/campaign app, one-short, with limited lifetime. Don't bring a hammer into a pillow party, or vice versa.

## So, can I still have it cheap? Pretty please?

Yes you can. Now that you reached this point, I will reveal a secret. Cheap is not a problem. Making shortcuts is a problem. You can find cheap by applying agile, and remembering that we're still doing about 80% of unnecessary ambitious features only 20% of people need, if even that. Scrum and Kanban as well as Lean are good ways to concentrate on the essential, perhaps do less features but do them properly. I'm always inspired by how much money Google has made using just one input box on an html form - but doing it in ingeniously engineered way. 

![Features as defined. Jar represents money and time.](/img/cheap-software/overflowing.jpg)

So drop that unneeded unwanted extra stuff that someone was daydreaming but is not really essential for success. Think about this like gardening: Good garden is not crowded by all vegetables and flowers one can imagine. Good garden is well though, has just what you want and need, and everything there deserves and gets your full attention. Well, you got me there, I have to admit that I just brought a greenhouse, so I'm full on into gardening right now.

![Yeah, my new greenhouse](/img/cheap-software/greenhouse.jpg)

So I would rather keep on doing excellent input boxes that really drive the business and are well and professionally made, than that fast-coded cowboy style php webshop that pretty much causes disaster after another. Actually, during my career, I've been brought more than once to salvage the steaming remains of unprofessionally coded steaming pile of cow manure. You can imagine how much it costs to have to do that in a hurry.

Another thing to keep in mind is getting the requirements right. It's very difficult to do before we start coding, because that's the moment when we know the least about challenges, limitations and possibilities ahead. That's why all agile methodologies tend to shine bright, because we delay making decisions as late as we can. On the other hand, this requires good refactoring, it's essential to keep the codebase in good health, flexible even. And of course maintaining your codebase adds to expenses at that point.

But, of course you have to remember that high price does not guarantee excellent results, either. Agile project that does not have vision or focus or worthy goal can be a horror story. And is a supercoder that much better investment that just a damn good one? Hard to say. How do you evaluate quality?

Well, perhaps that's a great topic for another blog in the future... :)


## Some links for your entertainment:


- [Year2k cost](https://en.wikipedia.org/wiki/Year_2000_problem) 
- [Year 2k38](https://en.wikipedia.org/wiki/Year_2038_problem) 
- [Mariner 1](https://en.wikipedia.org/wiki/Mariner_1) 
- [Splunk Datetime](https://docs.splunk.com/Documentation/Splunk/8.0.3/ReleaseNotes/FixDatetimexml2020) 
- [Excellent blog on tech debt](https://dev.solita.fi/2020/05/18/easy-steps-to-techdebt.html)











