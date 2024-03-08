---
layout: post
title: Advent of Low-code - Solving Advent of Code 2023 with OutSystems
author: rogerwanamo
excerpt: >
   OutSystems is a low-code platform that promises lightning fast development with less coding, but how well will it do when we pit it against tasks that require more complex algorithms?
tags:
 - Low-code
 - OutSystems
 - Advent of code
 - Programming
---

In November last year, a notification popped up on my screen informing me that an info session about Advent of Code was about to start. In our company, we have a lot of info sessions about various subjects that you can choose to attend if you have time and interest. Most of the time I have more pressing matters at hand, but this one caught my eye and I decided to listen in. Little did I know that this split-second decision to press 'Join' on the notification would end up costing me most of my spare time and several missed morning gym sessions in December. Boy, was I in for a ride!

Advent of Code is an advent calendar of programming challenges, founded by Eric Wastl in 2015. Every day from December 1st to December 25th a new puzzle is released, with puzzles getting increasingly difficult over the month. Each puzzle consists of two parts, the second part is revealed after you have solved the first one. Each person receives unique input data for the puzzles, and you only submit the solutions for your input to complete them. This last part I found particularly interesting. As long as you find the right answer, the method doesn’t matter. You can use any programming language of your choice, solve it in Excel, on the old Casio you used in high school, use Minecraft, or do it by hand. Some people even used Microsoft Paint to solve one of the puzzles this year.

At this point, I had only one question in mind: How far into the month can I make it while solving the puzzles in OutSystems?

## What is OutSystems?

OutSystems is a low-code platform that promises lightning-fast development with less coding, using a visual drag-and-drop interface to build applications. It has been my main tool since I started at Solita two years ago, and I can confirm that you can indeed do a lot of things very quickly with it. But how well will it do when we pit it against tasks that require more complex algorithms? Can we use low-code to solve tasks that by definition should require some challenging coding?

![Image of OutSystems Service Studio with the action for solving Day 2, task 2](/img/advent-of-low-code/AoC02-2023.jpg)
>   Solution to Day 2, part 2, implemented in OutSystems Service Studio

My gut feeling was that it should be possible to do just about anything. I mean, it has records, lists, ifs, and for-loops. What more do you really need in life? I could, however, foresee some potential problems. The biggest one would be that it has records and lists and, well, that’s it. Those are the only data structures at my disposal. There are for example no hash maps and there’s no way to make proper linked lists or tree structures since it doesn’t support recursive data types.

The lack of more sophisticated data structures, coupled with the fact that I don’t have full control over the generated code for optimization, could potentially lead to some issues with speed. This issue was confirmed in an [OutSystems blog post](https://www.outsystems.com/blog/posts/why-we-love-advent-of-code/) from 2021 about their software engineers’ experiences with Advent of Code. According to the blog, some attempts have been made at solving it in OutSystems, but computer memory and time have become issues in the harder and larger problems. Nevertheless, I would not let this discourage me. The goal was simple: make it as far into the month as possible using only the basic logic components provided in the OutSystems action flow. I would also avoid using for example javascript nodes, which would kind of defeat the purpose as they’d let me write whatever code I want.

## Getting ready

Before the month started, I looked up the first puzzle from last year to see what to expect and what I’d need to implement the solutions. The puzzle was simple enough, but one thing immediately became clear. When parsing the input I had to make a small exception from my no Javascript rule. I wanted to work entirely client side and there is no built-in client-side function for splitting strings. It should be possible by iterating through the string and checking substrings, but that felt like an unnecessary hassle. I’d rather spend my time implementing the more interesting parts of the solutions.

I made a few string-splitting actions that became the first actions in my ever-expanding utility library. Next, I set up a reactive application, made a web block for handling the common functionalities of each task, such as switching between sample and full input, timing the execution, and so on, and made a screen template for the daily tasks. With this, I was all set and ready to go. At least this part was swift and easy to do in OutSystems!

![Image of UI widget created to handle the tasks in the browser](/img/advent-of-low-code/AoC-webblock.jpg)
>   My simple UI component for handling common functionality in tasks

## And so it starts

The first week of puzzles was rather straightforward with few surprises. The only problem directly related to my chosen tool was that I didn’t know how to best share my solutions in our company's daily solution Slack threads. My colleagues could simply post their code, but I only had screenshots of the solution, often split into multiple action flows. Other people can’t see exactly what is defined in if- or assign-elements, nor can they run the code to test it, but I shared some screenshots anyway since it was all I had. Not every day though, some days the solution didn’t feel that interesting to look at.

![Image of OutSystems solution to Day 6, task 2](/img/advent-of-low-code/AoC06-2023.jpg)
>   Solution to day 6, part 2

Sharing screenshots served as a good reminder to keep the code and labels readable. The more complex the logic gets, the more important this is, which I was reminded about several times during the month. Sometimes it might be tempting to take shortcuts and write long complex expressions in if- or assign-nodes, but this will come back to haunt you when debugging. Few things are more annoying than running the debugger, only to find it fails at some expression that evaluates several different conditions in one node and you cannot easily work out which one fails. For readability and maintainability, it is almost always better to properly draw out the logic instead of hiding it inside nodes.

Early on I also added a lot more common actions to my utilities library. Some of the most frequently used included various string-to-grid actions (string to list of lists), actions for initializing lists or grids of given sizes, as well as a bunch of logging actions that would console log different types of lists and grids in readable forms. These would make input parsing easier in the later days, but that process would still always be rather slow and tedious. That is one use case where I’d take any programming language with decent list comprehension capabilities over OutSystems any day.

## Ramping up the difficulty

The first surprise came on day 8. I could see one potential way to solve part 2, but a general solution handling all possible inputs seemed extremely complex compared to what we had seen so far in the month. Turns out Advent of Code sometimes expects you to not make a general solution at all, but instead inspect your given input and create a solver for that specific input. This kind of solving was new to me and felt odd at first, but knowing the puzzles could work like that would come very much in handy in later days.

![Image of OutSystems solution to Day 10](/img/advent-of-low-code/AoC10-2023.jpg)
>   My original full solution to Day 10, both parts

Day 10 was the first task that took a significant portion of the day to solve. Luckily this was on a Sunday. From there on the daily difficulty did fluctuate quite a bit for a week or so, until it really ramped up in the last week. That last week was quite brutal. Most days I would spend two hours before work and several more hours after work to solve them. Still, having made it this far there was no way I’d give up. I kept pushing, then finally on the 25th… I was one task short.

Unfortunately, part 2 on Christmas Eve was too much to handle, especially on that day when I also had some other plans. That was also the task that made me the most jealous of people using other programming languages, such as Python programmers who could just feed a few equations into SymPy and get the answer out. OutSystems unfortunately doesn’t come with luxuries like that. I wasn’t done yet though. After a brief vacation, I came back to tackle the beast and finally a week after the challenge ended I had all 50 stars collected, each and every one of them solved in OutSystems.

![Image of OutSystems solution to Day 24](/img/advent-of-low-code/AoC24-2023.jpg)
>   My Christmas tree solution to Day 24, part 2 (please, don’t write code like this…)

## So, how about that performance?

It goes without saying that OutSystems cannot compete with faster compiled languages, but on most days it was still more than fast enough. There were a few notable exceptions where my initial solutions took long enough to run for me to make coffee and grab a snack. In those cases, it helped that I was doing it all client side since I didn’t need to worry about OutSystems server timeouts at all.

Slow execution almost always came down to list handling. The built-in list actions are slow and the greatest time gains came from refactoring to use list actions of lower time complexity, or from removing the repeated use of list actions. The slowest list actions, ListSort and ListDistinct, I learned early on to never use inside loops with lots of iterations. Later a lot of the optimizations were all about avoiding the use of O(n) list actions like ListIndexOf or ListAny and replacing them with direct index references.

One typical case of avoiding ListIndexOf was when keeping track of already seen or processed elements. Instead of storing seen elements in a list and searching through the list every time I needed to know if an element was processed, it was much better to make a separate boolean list of fixed size for direct lookup of seen indexes or add some IsSeen attribute to the original record list. Another case was when dealing with maps. Days 8 and 20 had input in the form of maps. Each row had a text key and referred to one or more other rows by their text keys. The first thing I did was replace the text keys with sequential integers, then put them in a list where the index was the key, allowing for direct lookup instead of searching for the key.

The greatest time gains were still to be found by finding more efficient algorithms and efficient ways to represent the problem. In particular, many puzzles would have had a trivial brute-force solution, but those would have been far too slow. For example, on day 5 a brute force solver for part 2 would probably be running still today. Luckily I spotted this from the size of the input and didn’t fall for that trap. I immediately went for a solution that bulk processed ranges of numbers, instead of individual values. This was the first action flow of the season that ended up looking a bit more complicated.

![Image of OutSystems partial solution to Day 5, part 2](/img/advent-of-low-code/AoC05-2023.jpg)
>   The function for converting ranges, Day 5, part 2

In my favorite puzzle, the 3D Tetris/Jenga puzzle on day 22, you had to start by dropping 1500 blocks in 3D space to find out how they would end up resting on top of each other. At first, I was setting up some massive 3D tables to record which spaces were occupied, but I quickly realized such a thing was completely unnecessary. A 10x10 integer height map was all we needed to find out how far each block would drop.

![Image of OutSystems solution to Day 22, part 2](/img/advent-of-low-code/AoC22-2023.jpg)
>   Full solution to Day 22, part 2

## Improving the worst-case scenarios

Once the challenge was done, three problems stood out with very slow solutions. I looked through these again in the hope of finding at least some optimizations.

The first problem was day 16, which clocked in at over three minutes. This problem involved shooting laser beams into a grid of mirrors and splitters to find out how many cells would be illuminated. It was clear that my original solution did a lot of repeated work. I had no memoization and the same mirrors would be hit from the same directions multiple times over the iterations. It seemed a bit tricky to make proper memoization that would store which parts of the grid would be illuminated for each mirror. Instead, I went with a more lightweight option that only cashed the distance the beam would travel in each direction from a mirror before hitting the next. This brought the running time down to under 20 seconds and I was happy with that.

Day 17 required some pathfinding with a twist and my initial Dijkstra-based solution ran at over 4 minutes.  I know the way I handled the twist was quite clumsy and not very optimal, but I mainly looked for optimizations in the Dijkstra, as that seemed more useful for the future.

The first place to look for optimization was the priority queue that determines what cell to check next. I didn’t have a priority queue, I had an unordered list. Luckily we can emulate a min heap binary tree structure with an ordinary list and some custom insert and remove actions that bubble up/down as necessary using direct index references. Implementing these custom inserts and deletes already cut the running time in half. After some further optimizations to how it checked if a cell was already seen the running time went down under 90 seconds. Finally, right now as I’m writing this blog post I noticed a bug in my min heap implementation. Fixing that brought the running time down to just over a minute.

The last super slow solution was day 23 with a run time of over 6 minutes. This was a longest path problem, which is NP-hard, essentially meaning there is no fast algorithm to solve it. I could only find some minor improvements in the implementation, but a much bigger improvement by understanding the problem space. Removing some edges that couldn’t be part of any valid solution brought the time down to about 75 seconds.

Here are the final solve times for all 25 problems in milliseconds:

![Graph showing solution times per day for all tasks](/img/advent-of-low-code/AoC2023-SolveTimes.png)

The numbers might not be particularly impressive compared to what you can achieve with conventional coding, but I think they are fast enough to say that you definitely can do Advent of Code in OutSystems. I’m also sure most of the solutions could be improved further by implementing more efficient algorithms.

There is also the option to work with server-side logic, which is faster for slower problems. However, when I tried to run my initial slow implementation of day 17 in a server action I kept running into server timeouts. I couldn’t get around these despite trying all possible ways to increase the timeout limit. I don’t know if this was caused by some limitation in the free OutSystems personal environment or by something else I was missing. My improved solution for day 17 was fast enough to avoid server timeouts and was about twice as fast as the client-side implementation of the same code. And of course, if you ever need heavy calculations like these in a real OutSystems project, you can always write a C# extension for much better performance.

## Final thoughts

Completing Advent of Code was rather time-consuming and quite challenging at times, but also very educational and above all a lot of fun! Doing it in OutSystems taught me a lot of new things about the platform and forced me to find new ways to use the available tools.  I can warmly recommend giving AoC a try if you are at all interested in coding puzzles and challenges, whether it be in OutSystems or using some other language or tool.

Over the course of the month, I also noticed a great improvement in the quality of my OutSystems code. Early on I would make quick and dirty solutions, which often required complete rewrites when part 2 was revealed and required some things to be done differently. Later in the month, I defaulted to better-structured code, which made it easier to reuse in part 2.

![Image of OutSystems solution to Day 20](/img/advent-of-low-code/AoC20-2023.jpg)
>   Solution to Day 20

As for the promised lightning-fast low-code development, I must admit that it doesn’t necessarily apply to these kinds of tasks. Drawing complex logic flows can be rather tedious and often more time-consuming than it would be to write the same logic in code. Take for example a simple operation like incrementing a variable. In Java I’d write i++; and be done with it. In OutSystems I add an assign-node to the canvas, select the variable i from a dropdown, type in the new value i+1, and finally for readability type i++ in the label.

On the other hand, the most time-consuming part is usually figuring out how to solve the problem and how to fix your bugs when the solution inevitably doesn’t work. Especially for the second part, I find that the visual representation of the code is very helpful. It makes it much easier to understand the logic flow and to find bugs or flaws in the logic.

Will I be doing it again next year? Absolutely! I’m not sure if I’ll again do it in OutSystems or look for some new challenge, but I will certainly participate in one way or another. Then there is also the backlog of puzzles from the eight previous years. Oh my, this is gonna be a long year…
