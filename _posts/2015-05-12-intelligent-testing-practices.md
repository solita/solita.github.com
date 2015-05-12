---
layout: post
title: Intelligent practices of software testing
author: pekkama
excerpt: Intelligent practices of software testing creates guildelines to make software testing more context responsive
---

Intelligent practices of software testing
-----------------------------------------

Note! I am not using the term “best practice” here. *Intelligent practice* is something that helps people develop their practices into more suitable for their need. We actually should stop using “best practice” term. Instead we should use whatever helps us solve the problems at hand. The problem solving should come from people and their skills. Influences should be taken from everywhere! Practices should be molded to facilitate problem solving in YOUR context.

Very well. I came up with the following guidelines to help create a better testing environment for me and my colleagues. I am not trying to invalidate your practices that have been found to be best fitting for you. You should keep the practices you deem appropriate for your context. I encourage to revise your practices based on my own findings. It is up to you to change what ever you see reasonable, if anything.


Fight ambiguity with openness and communication
-----------------------------------------------

A few examples on ambiguity: 

- The (written) requirements are vague and ambiguous at best. Usually they are out of context and/or vacuum packed. I remember ISTQB mentioning that “It is testers’ right to deny ambiguous requirements”. I believe it is the testers’ obligation is to address this as soon as it is found. And by addressing I mean talk with people. “I cannot figure out how the system should work. I found out that it works like this. Is this OK to you? If not, can you help me determine how it should behave?”
- The test cases are not concise. If we are to perform good enough testing we need to do testing. Writing test cases *might* be testing – executing test steps from a test case *might* be testing. This all depends on the skills of the tester. If the material we base our testing is poor, we need to be open about it. If we feel that we cannot do good enough testing, something needs to change. That change comes from talking about the issues, being open about the difficulties. 

If something is not clear, make it clearer. Find the information, people, resources that helps you make it clear. Learn from difficulties and be open when you face them. Hiding problems rarely leads to anything positive.


Fight ignorance with eagerness
------------------------------

Ignorance comes in many forms. One can claim she doesn’t know enough about the product to test it. Ignorance might paralyze us. Tasks can be daunting and we might procrastinate because we do not know some specific thing about the subject. 

**Enter eagerness!** Try Proof of Concept type of actions. Try sandboxing the test area. Try having fun. Try getting a group of people who might already know about the domain, the product or the like, and test with them. Try walkthroughs. Try anything and everything to solve the problem. Be eager to to solve issues. If you can't solve them, be eager to get issues solved. Ignoring issues rarely leads to anything positive.


Fight über control with good-enough documentation and reliance to skills
------------------------------------------------------------------------

Sometimes the aforementioned (ambiguity and ignorance) might lead into not trusting our ability to do proper testing. That might lead into a form of control that requires a vast amount of documentation and reports. There is a three-fold solution to this, I believe: rightly timed planning, unburdening reporting and reliance to people ability to the best possible job. When it comes to testing, people usually ask for test plans, test task descriptions (of various levels of detail) and test reports.

When doing good testing, it requires some planning to remove inefficiencies. That planning should be done in advance, albeit on a higher level. We must be able to plan our testing while we test, because we learn about the product, the project and everything surrounding us *while we test*. By timing our planning in sync with our testing, we can react to changes and discoveries more efficiently. The planning should happen as close as possible to the actual execution of the plan. Documents and plans deprecate quickly when new things are added. For example, Rapid Software Testing encourages planning and designing tests during testing. I have found out that a brief planning session before testing session is usually in order to be able to tackle the most important topic during that testing session.

We are chosen to perform the tasks because people expect we can do the task. There is little reason to stupefy the intelligent people that do things for us. Writing test cases, that basically make our brains redundant, is stupefying. In fact, it is stupid to write something that creates stupidity. “Stupid is as stupid does.” In order to be intelligent and harness out intelligent to our testing, it is wiser to write inspiring testing documentation. Missions, threads, ideas, broad descriptions, etc. encourage the use of our brains. I’d say “skill before process” and encourage to constant learning and teaching. Autonomy increases motivation ([see this post](http://how-do-i-test.blogspot.com/2012/01/motivation-30.html)) to do the best possible job. Critical thinking enables you to challenge your biases. Lateral thinking helps uncover possible issues. Thinking is the key, not the process or tools. 

We also need good reporting off of our testing. Reports may be bug reports, testing transcripts, etc. An important thing to remember here is to focus on relevance and sufficiency of our reporting. The report should be a tool to improve and to facilitate discussion within our testing, development and/or project management. Thus I feel that reporting should be done in ways that support our cause, not because we want reports to begin with. Tools may vary from video recordings and screen captures to notebook scribbles. Anything is fair game as long as it supports the cause. 


Fight measuring and quantification with reliance on feelings, observations and communication
------------------------------------------------------------------------------------------

Numbers are cryptic. Numbers can be interpreted in as many ways as there are people interpreting. Let’s say we have 100 test cases from which we have run 90. A clueless test manager might say: ”Only 10 more and we’re done”. An intelligent tester might say: “It seems we have 10 scripts to look at, but what else do we need to take into account?” Quantifying test cases (or bugs for that matter) is ridiculous. It is like counting unicorns! How many unicorns can fit into a cubicle?

A better approach to test case counting might be counting the *time spent testing*. Time is uniform in magnitude. Hour is as long in Finland as it is in New Delhi. What is the size of a test case? Few can tell. Measure what is worth measuring and what is objective.


If this is measuring our progress, how do we measure coverage?

We might want to ask “why we measure coverage” and then choose the metrics based on that. One good coverage indicator is a list of items in the product under test that *we have touched*. If an area is *touched* multiple times, we could be fairly certain that it is covered well enough, and we know the areas that are *untouched*. The human feelings come to play here. If a tester or a developer feels that some area is of poor quality, then we should play that feeling and test that area some more. A test case doesn’t tell how confident the tester is - talking about findings with the stakeholders might demolish the false confidence and lay ground for confidence based on actual findings and behavior.

Whatever you choose as your method of measuring, talk about it. The numbers are devious and one should ALWAYS talk about the coverage and confidence instead of using numbers to /prove/ why something is good. I support creating a measurement strategy that is little or no burden to the actual tester, and then use those findings to *steer testing to the right path* instead of *proving something*. Be critical about numbers because they can fool us easily. Be intelligent and critical on what and how to measure.


Summary
-------

To summarize, my intelligent practices for software testing might include the following:

- Fight ambiguity with openness
- Fight ignorance with eagerness
- Fight über control with good-enough documentation and reliance to skills
- Fight measuring and quantification with reliance on feelings, observations

There might be more and I shall keep looking. The most important thing about these practices (or statements or whatever one might call them) is to communicate with people. Discuss your expectations and goals in testing. Discuss procedures and skills, how they can be improved. Whatever challenges you face, communication is the first step to solving the problem. An umbrella practice might go something like this:

- Fight \<choose challenges\> with \<choose solutions\> and communication

If you feel I need to clarify some of the practices, give more examples or add a fundamental practice to my list, please drop me a line. I’m more than eager to discuss. ;)

- @pekkamarjamaki
