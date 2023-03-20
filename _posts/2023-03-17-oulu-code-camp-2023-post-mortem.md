---
layout: post
title: Beers, Bots and Black Friday - Solita Code Camp 2023
author: jlansineva
excerpt: >
  Oulu Solitans gathered for fun, hacking, drinks and sauna at Solita Code Camp 2023. Code was written, both good and bad. What worked, what didn't? Here's my story. 
tags:
 - code camp
 - fun
 - hacking
 - hackathon
 - sauna
 - beer
 - after work
 - programming
---

At Solita we have a long-standing tradition of code camps - [with records dating back to 2012](https://dev.solita.fi/2012/11/23/codecamp). Last event of the kind was held seven years ago, but like fine wine, a good thing can't be rushed. Here, a code camp is sort of a hackathon, a gathering of devs hacking away at some task, with a focus on Fun. At Oulu, we were located at Tervatoppila Saunamaailma (Saunaworld), in a nice cozy cottage-like atmosphere - just 10 minutes drive from the centrum. Of course, the saunas were booked as well to wash off the hacker’s blood, sweat, and tears - that’s a given. We also had catering and, most importantly, drinks. 

[![The venue frontyard](/img/code-camp-2023-oulu/thumb-frontyard.jpg)](/img/code-camp-2023-oulu/full/frontyard.jpg)
*Frontyard of Saunamaailma*

I arrived in due time, found myself a spot at a table, grabbed a drink, and got set up. I had thought about looking at the templates beforehand, but coming from a game jam background I opted not to. To me, part of the fun is the hectic and manic hacking, observing as your initially well-thought and clean code throughout the event further and further breaks down, losing any semblance of coherence, finally embracing the chaos and becoming one with it. Surely preparing ahead would be cheating.

I decided to use Clojure, as I figured banging out stuff in the REPL - an interactive development environment that allows you to hook into the running application and evaluate code at runtime - could be very efficient in this type of fast hacking type environment. I haven’t used Clojure too much in this type of real-time context, so that was relevant to my interests as well. For web development, Clojure is my daily driver, so I’m pretty familiar with the language. As the allotted time was around five hours, that seemed advantageous. Granted, code camps offer a great opportunity to experiment with new technologies without pressure, with the trade-off being that you probably won’t accomplish much, especially if starting cold.

[![Hacking by the fireplace](/img/code-camp-2023-oulu/thumb-fireplace-coding.jpg)](/img/code-camp-2023-oulu/full/fireplace-coding.jpg)
*Our table, hacking away*

## Getting started

The task for the code camp was to write a bot that was able to navigate a store, pick up the items with the best discounts, and when done, exit via the cash register to bank their score. Over time, the bots get exhausted, losing life, which can be replenished by potions (curiously presented as beer). If the bot’s life goes to zero, the bot is removed from the playing field. Some items can also be utilised as weapons, which can be used to attack other bots, for shenanigans. The store is represented as a top-down 2d map, where items spawn randomly. It has walls that must be navigated past and can have traps that cause damage.

The game itself was run on an Azure-based server instance. The bots communicated with the server with simple REST API, sending a movement, pick-up, or use action. Once per second, the game was updated with the latest actions for the bots. A local server for dev was also available, but I figured I’d be fine with the cloud setup.

[![The difficult map](/img/code-camp-2023-oulu/thumb-solita-map.png)](/img/code-camp-2023-oulu/full/solita-map.png)
*The more difficult map*

## Time to hack the planet

I cloned the repository, opened up the Clojure template, and fired up the REPL. I ran the function (api/register “Seppo”) and got a response. Perfect. My bot appeared on the playing field but died quickly since I wasn’t quick enough to send actions. Next up, some random movement. First though, since the server had chat available, that needed to be used. All would fear the war cry “Hail seitan”

I quickly got some random movement going, so it was time to focus on the Plan. I figured most would concentrate on optimising their score, so my goal instead was to focus on gathering as many weapons as possible and use them to blast my opponents off the map, keeping myself alive as long as possible. Any time a weapon spawns, my bot would beeline to it and use it. If no weapons were available, focus on collecting potions to keep the health up, otherwise just wander randomly.

![Alkoritmi](/img/code-camp-2023-oulu/full/alkoritmi.png)
*My alkoritmi - drunkenness had to be implied in code as I was on NA beers*

I needed a way to get the closest weapon and the closest potion. I implemented Manhattan distance calculation (sum of absolute x and y differences from my position to item position) and implemented some dumb movement - just check whether the x or y difference is greater, and move a step closer in that direction. Worked fine unless there were walls, which my bot stubbornly wanted to ignore and push through.

With luck, I got suitable spawns and managed to move toward the correct items. Great! However, item spawns proved to be an issue - bots were ignoring potions so over time the map was full of just potions. I figured I’ll just take my weapon search code, adjust it slightly and for when there are no weapons on the playing field, look for potions. This would both keep my health up and open up the map for more weapon spawns. I made additions for potions and set my bot loose again, and finding items seemed to work ok. Now, only to pick them up.

[![Group of hackers](/img/code-camp-2023-oulu/thumb-group-hacking.jpg)](/img/code-camp-2023-oulu/full/group-hacking.jpg)
[![Hacking by the other fireplace](/img/code-camp-2023-oulu/thumb-other-fireplace-coding.jpg)](/img/code-camp-2023-oulu/full/other-fireplace-coding.jpg)
*We had multiple rooms of people hacking*

## Need a pick-me-up

I had the biggest issues with my pick-up code for some reason. My bot would move correctly to the item but just wouldn’t for the life of it pick it up, it would just move on, notice there was an item close by, and move back to it, ad nauseam. It was sending the correct action, it was at the correct place, but just wouldn’t pick the item up. What the hell was going on? By chance I was looking at the server interface when other bots were operating and noticed that picking up items was not instant - it required multiple turns. And yes, the documentation stated as such, I just missed it.

At this point, it should be good to expand a bit on my bot’s lifecycle. Basically, I started the bot, it ran its course until it crashed due to an exception. For example, sending an action for a dead bot was an error. Once I got my movement working, a bot could theoretically live for a long time, which was not good for my development. I implemented a turn counter as a hard limit. With x turns done, just quit. Later I moved to atoms for different state handling. Whenever I needed to keep a track of a new thing - add an atom. It got a bit messy. Chaotic. So, keeping track of what my bot was doing was at times challenging.

Nevertheless, with enough checks and adding new state atoms, I got my bot to stay put when on top of an item. It managed to pick up items! I added use-action and it did manage to use items as well! It didn’t put any consideration if anyone else was on the stage, it just blasted mindlessly whenever it could. It was something! I did see it get a kill a couple of times as well, so mission success.

Then the map changed.

## Finish him

We had a set of different maps, with different terrain difficulties. My bot operated ok on a simple map. Any more complicated, the luck factor with bot and item spawns became significant as I didn’t have proper navigation yet. And the traps, those my bot chose to merrily ignore. The more difficult maps had higher item spawns, so that was a benefit. A slight benefit, but still. Needless to say, my bot was not super effective with a more difficult terrain with no real pathfinding. With the clock ticking, I decided to refocus my efforts, got some dessert and a drink, and just ran around trying to cause mayhem, until it was time to present our solutions. 

At Oulu, we have for some reason become quite [Clojure](https://clojure.org/)-oriented over time, with many of us have had exposure. There were a couple of [Elixir](https://elixir-lang.org/) solutions, which did quite well. At least one C# .Net 7 solution also performed very well, reaching the top score momentarily and then getting stuck in the harder map. Other used languages were [Rust](https://www.rust-lang.org/), [TypeScript](https://www.typescriptlang.org/), [Python](https://www.python.org/) and JS with [Ramda](https://ramdajs.com/)-library. All in all, there was quite a wide spectrum of languages used, which is always nice to see at this kind of event. Few dipped their toes into unfamiliar territory experimenting with new tech, which fit the nature of the event perfectly. No completely off-the-rocker deep-end esoteric languages this time!

[![Hacking by the fireplace](/img/code-camp-2023-oulu/thumb-heavenly-code-presentation.jpg)](/img/code-camp-2023-oulu/full/heavenly-code-presentation.jpg)
[![Hacking by the fireplace](/img/code-camp-2023-oulu/thumb-team-presentation.jpg)](/img/code-camp-2023-oulu/full/team-presentation.jpg)
*Giving presentations about our solutions*

## Conclusions

So, how did it go?

Well, my strategy of going hog wild, blasting everyone off the map wasn’t the best option. Weapons were single-use, did limited damage, and cost money, so the bot ran out of resources quickly. The item spawn rate was map dependent as well and in the easiest maps there just weren’t enough weapons - I implemented a feature that would drink potions, just to get them out of way for more weapons to spawn.

I realised too late, that picking items took multiple turns - what can you say, my bot got bored easily. It tried to pick a weapon up but just wandered off. I’m not sure why it did that, as my code should’ve just stayed put when on an item. Weird bug. Which leads to…

Debugging in the cloud is hard! There’s only the game state to rely on for debugging purposes and you get no feedback on whether your move was good until the game ticks. In hindsight, a local setup could’ve been helpful for debugging.

Embracing the chaos is fun but there are some drawbacks - mutations, spikes growing on your power armour, stuff like that. I was finding myself - unintentionally - exploring ways to write code imperatively in a functional language. This likely spawned from me messing in the REPL and lifting code into my codebase without caring about the code architecture overall. Global mutations are an easy way to keep state, yet messy and obviously abundant with heresy, send the inquisitors.

I never got around to implementing proper navigation, just relied on luck for “getting there” the straightest line possible. Which was a completely fine approach, unless walls were in the way. This caused too much I thought about A* but figured I’ll do it later. Later came too late. There was a ready-made A* implementation for Clojure I could’ve used.

Fine-tuning my bot I would implement some sort of asynchronous loop that could handle multiple bots at the same time, to make debugging and developing a bit smoother and easier. My current solution was synchronous and blocking, relying on a turn counter. I didn’t use the REPL to its fullest potential - actually developing in the app at runtime. Still, working with the REPL overall was great and it did remove some obstacles to testing my code. 

## tl;dr

Overall, the event was great fun! While my solution never really got “there” I did enjoy the same joy of programming I previously have gotten from game jams that I regrettably so rarely have time for now. Unburdened by the shackles of billable hours, just fast-paced hacking the code together, to succeed and to fail. The food, drinks, and sauna were great, and the atmosphere at the location was completely different from the office environment, cozy, homely, and warm. I would greatly encourage anyone to take part in these types of events, as it is a great detox from all the serious work. It's also a great way to try out new stuff pressure-free! [Bots of Black Friday-repository](https://github.com/janneri/bots-of-black-friday) is available with the server and templates - fork and try it out!

There's been a rumour that the next event of the kind would be happening later this year, so why not [join us](https://www.solita.fi/en/careers/)!

[![Post hacks chats](/img/code-camp-2023-oulu/thumb-post-hacking.jpg)](/img/code-camp-2023-oulu/full/post-hacking.jpg)
[![Beer on a fireplace, just chilling](/img/code-camp-2023-oulu/thumb-beer-chilling-by-the-fireplace.jpg)](/img/code-camp-2023-oulu/full/beer-chilling-by-the-fireplace.jpg)
[![The venue backyard](/img/code-camp-2023-oulu/thumb-piha.jpg)](/img/code-camp-2023-oulu/full/piha.jpg)
[![Palju](/img/code-camp-2023-oulu/thumb-palju.jpg)](/img/code-camp-2023-oulu/full/palju.jpg)
[![Showers](/img/code-camp-2023-oulu/thumb-showers.jpg)](/img/code-camp-2023-oulu/full/showers.jpg)
[![One of the saunas](/img/code-camp-2023-oulu/thumb-sauna.jpg)](/img/code-camp-2023-oulu/full/sauna.jpg)

