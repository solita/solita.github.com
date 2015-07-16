---
layout: post
title: Test automation allergy
author: pekkama
excerpt: Questioning the snake-oil approach to test automation
---

I am allergic to test automation!
---------------------------------

That's correct! I get itchy and my eyes redden every time someome talks about test automation. I get coarse throat when I see a test automation coverage report. I get twitches when we justify our lack of skills as testers with 95% line coverage. That's a reaction to poorly executed and poorly justified test automation. I am allergic to s***ty test automation. And I think everyone should be!

This post is about questioning the snake-oil approach to test automation. I have been doing software testing for a number of years in different types of organizations and workplaces. My approach has been, and still is, skill-driven and holistic. Test automation done well is worth the money invested in it. There has been only few cases where it has been worth the money, though. The best automation is always a supporting act to other testing activities, and the best automation is treated that way.


You cannot automate testing!
----------------------------

Testing isn't a set of steps. Trivializing testing to just execution of steps is plain studidity! Everyone who thinks like that is essentially in denial, ignorant or a stupid in the head. Testing is a vast set of mental and physical activities. It is executing tests, designing tests, analyzing the results, guessing, trying, learning, understanding, and reporting. More than anything, testing is thinking. Machines don't think, they assert only the stuff we tell them to. We cannot create so comprehensive, complex machine that does the job of a human brain. We can automate something, yes. My suggestion is to understand the limits of test automation and make the best of the stuff it is good at.

Test automation should be used to automate *checks*. Assert(A==A). Then add flesh to the bones. And then you have an automated check. The moment you start using test automation to do anything more complex, you will be pouring money into something that might never pay it back. Use test automation as a tool to make development easier (and at some point even help testing). You don't want to check all the things every time, but you want to test how things actually work. You don't want the stuff to break that (we think) worked previously because you don't want regression. Even the best test automation will not reveal everything, as we all know.

Of course there are different granularities in test automation. From unit-testing individual classes and methods to full blown user simulations. And they all have some importance to some task in developing software. Not always but often enough, people talk about test automation as a replacement for all other testing. They try to automate testing and then happily watch the machine do all the work. Sadly, test automation cannot perform the following check:

> "Check that nothing happens that shouldn’t happen and everything else happens that should happen for all variations of this scenario and all possible states of systems and all possible visual/audio/tangible things user might observe and all possible states of the backend and all possible states of the system as a whole, and anything happening in the surrounding systems that should not matter but might matter."

A human cannot test that on one go, but I bet my year’s salary that humans fare better at the task than a machine. Of course contexts vary and there might be occasions where a test automation can test absolutely everything. I (nor anyone whose opinion I value) have ever seen that.


The framework of integrity and constant improvement
----------------------------------------------------

Why the f*** do we want to repeat a test? Why the f*** do we want to repeat a test? Why the f*** do we want to repeat a test? Why the f*** do we want to repeat a test? 

See how silly it is? If you think about it, there are many variables we don't know. We have randomness in our servers, networks, everywhere! Even the bloody electrical current isn't stable So why on earth do we want to try and repeat the situation over and over, if the world we live in is not repeating itself? You might want to answer "to verify that regression doesn't exist". Isn't the point and purpose of regression testing to see if there is something broken? Shouldn't we be searching for the thing that MIGHT be broken?

Actor Frank Langella said in a New York Times [article](http://www.nytimes.com/2014/01/05/theater/frank-langella-steps-into-king-lear-at-bam.html?hpw&rref=theater&_r=0)

> “There’s a tendency to value consistency over creativity. You get it, you nail it, you repeat it. I’d rather hang myself. To me, every night within a certain framework — the framework of integrity — you must forget what you did the night before and create it anew every single time you walk out on the stage.”

This is what test automation does: it finds a way that doesn't break the system and then repeats it. As a tester - as a thinking individual - I choose creativity and ideas before repeatability. I try not to do stupid things, but do the best possible testing every time I do testing. I don't fake it, I try to do the most important thing and I try to communicate my work to other people in a way that makes sense. Test automation doesn't strive for perfection, it settles for acceptable, meager existence.


Passion for good testing
------------------------

> "Doing your best work includes having the courage to let go of pretty good work that you’ve done before." - [James Bach](http://www.satisfice.com/blog/archives/1343)

In Solita we take pride in having the courage to do things in ways that are perhaps new and daring. We have passion for what we do. We care about people our work affects. 

I want better automation! I don't want to settle for sub-standard test automation where "every test goes red every time something changes even slightly". Toss that s***! Build a robust set of checks and take them for what they are: checks If you want good testing, have a person do it. The person will most likely see areas that require automation to make testing easier. If you are a programmer who writes test automation, be a professional programmer! Use whatever programming practices you use to make the automation code as good as possible. Start simple, keep it simple. If you don't know what to test or how to test, learn to do testing! I bet there are people willing to help you out if you feel stuck in your quest to test intelligently.

And the most important thing of all: Think!

I am glad to answer any questions and comments about this this post. Just tweet me [@pekkamarjamaki](https://twitter.com/pekkamarjamaki) and I'll get back to you.


 


