---
layout: post
title: Continuous X is nothing, future is real-time
author: lokori
excerpt: Right now, Continous Delivery and Continuous Deployment (CD) and DevOps are all the rage. It makes sense to deploy the new version to test or even production environments as soon as possible. But the future is not continous, it will be real-time, so better get ready... or else.
tags:
- continuous delivery
- real-time delivery
- real-time deployment
- REPL
- Clojure
- C++
---

## The hype train cometh 


We have heard numerous talks and presentations about Continuous * over the past ten years. The big hype started with Continuous Integration (CI) roughly ten years ago, which meant
that different pieces of software were *continuously* put together and tested automatically.

Then we moved on to [Continuous Delivery](https://en.wikipedia.org/wiki/Continuous_delivery) and Continuous Deployment (CD). If we could rely
on the tests and run the tests automatically, it made sense to deploy the new version to test or even production environments as soon as possible. 

This is all fine and good, and while some organizations have not yet embraced and mastered the CD, others are already front-running the mainstream hype train. Continous Delivery
definitely requires certain discipline and professional conduct from the developers to succeed, but it certainly doesn't require inhuman
abilities and intelligence. The "DevOps companies" like [Heroku](https://www.heroku.com/) make it easy to get aboard the hype train now.

![All aboard the hype train](/img/real-time-deployment/hypetrain.png)


## The future will have real-time delivery

Obviously continous integration/deployment is better than sporadic integration or occasional delivery, but
assuming 100x more capacity for computation and storage, we would be now have instantaneous delivery/integration instead. Instead of having to wait 5 minutes or 15 minutes for test
results, we would have them in seconds. A second is so close to real-time that it would not matter to our puny monkey brains anymore. That would be totally awesome, wouldn't it?

### Who dares wins

You may still doubt all this DevOps and Continuous Delivery hype, but trust the great [FAKEGRIMLOCK](http://fakegrimlock.com/) on this: 
_Future will happen whether you like it or not_.

![Hot crowd drives the change](/img/real-time-deployment/hotcrowd-fakegrimlock.png)

ANGER IS SMOKE. FIRE DESTROY. DESTROY MAKE NEW THINGS GROW. COLD PEOPLE
HATE FIRE. NO ONE WANT TO BE FERTILIZER. FIRE NOT CARE.

LOYALTY IS SMOKE. PEOPLE FOLLOW FIRE, GET HOT. NOTHING STOP PERSON ON FIRE.
PERSON ON FIRE WRAPPED IN HOT CROWD? THAT FIRE CHANGE WORLD.

## How far is it?

There are two essential questions regarding this:

1. How close are we? 
2. How will we write the software when we get there?

I will try to answer these questions.

### Oh brave new world, that has such software in it!

We are already there, for some domains! As an example, consider [Overleaf](https://www.overleaf.com) which offers
almost real-time feedback loop for writing academic papers. Ten years ago I was running
[LaTeX](https://en.wikipedia.org/wiki/LaTeX) on my own 300Mhz Solaris workstation, but now it's possible to concurrently write
the papers and instantly update and validate the end result. Totally awesome development in ten years.

Similar examples are popping up now everywhere. As another concrete example from
a completely different domain, take a look at [KLIPSE](https://github.com/viebel/klipse) - real-time evaluation of ClojureScript in 
the browser. Infinitely better than static code samples. 

## And the winner is..

It is difficult to predict winners, but I believe the future belongs to programming languages
and environments which can take advantage of the resources and offer real-time feedback to
the developers. Take a look at this chart:

![programming languages](/img/real-time-deployment/programming_languages.jpg)

Everything is not placed precisely in the chart, but that is not relevant to the point I want to make.

In theory, it's entirely possible to run extremely fast C++ compilers given 
enough resources, but mutable state and the nature of the C++ programming language 
will make real-time programming difficult. Also the [template metaprogramming](https://en.wikipedia.org/wiki/Template_metaprogramming) 
model makes it  difficult to have really fast compilers for C++ in practice.

A statically checked and compiled language such as [Haskell](https://www.haskell.org/) may have more success, but at the moment 
the languages on the top are designed to offer real-time feedback and have built-in capabilities 
suited to programming and debugging "live" systems. The languages at the bottom are stuck with the
traditional model of "edit-compile-run", but even they are trying to get up. For Java we have things
like [JRebel](https://zeroturnaround.com/software/jrebel/) and hot deploy as a practical example, so you
could arguably place Java in another location on the chart. So instead of claiming winners, I only 
predict that **the programming languages and tools of the future will offer real-time feedback to the developers.**

At the moment I'm happy to sit in the [Clojure](http://clojure.org/) camp and we do have a warm campfire there now. 
Hot crowd is arriving.

## The next future after the future happens?

Extrapolating further, if we assume 1000x resources, we will have some very interesting possibilities. 
I can't know whether this will happen or not, but I offer this as a theoretical thought experiment.

We are already running mutating [genetic algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm). The [DeepMind](https://deepmind.com/) is playing Go against itself to 
find the best branch and parameters from the universe of possible DeepMind version n+1 candidates running in parallel. Instead of linear designed evolution we have semi-automated parallel evolution there.

If we had 1000x resources, we could apply this to conventional software outside the field of artificial
intelligence. We could then have multiple would-be-branches running and tested (and possibly deployed) and
select the one branch which doesn't crash and burn when automated fuzzers run millions of test 
cases against it. That would be interesting.

