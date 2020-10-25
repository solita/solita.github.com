---
layout: post
title: Predicting the future - an introduction to project work for aspiring software developers
author: tommi.kenakkala
excerpt: Key takeaways for software developers on common recurring challenges in software projects. What software developers should expect, anticipate and mitigate.
tags:
  - Software engineering
  - Project management
  - Ways of working
  - System Theory
---

# Predicting the future for aspiring software developers

## Introduction (i.e. is this worth your time)

![Pirate Sparrow Why meme](/img/predicting-the-future-for-software-developers/facepalm-bear.png)

Software projects face similar events and challenges time after time. The warm and fuzzy "Oh not this again" -feeling.
How can you avoid re-enacting horror stories from past projects if you are fresh in the field and just wondering what the old grizzly is grumbling about?

This post puts down some thoughts about how to inspect your way of working and some opinionated ways on how to view project work. With those in your mind, you just might be able to "predict the future", to avoid some shortcomings and repeating success as you go.

The arts of software engineering and project management have been around for a long time. There exist monuments of literature and academia on the subjects, which I encourage you to study (references later on). Instead of repeating the Agile manifesto or waterfall model, this is a collection of a few thoughts and hands-on observations to accompany your agile way of working. Hopefully this is helpful especially to those new to software engineering projects.

Following section "WoW" is a bit more hands-on about ways of working, the following "System" and the "High stakes" sections are a bit heavier describing observations about the environments where projects exist.

## The "WoW"

That's short for "_Way of Working_", a popular acronym on the field (and now you can throw it around like a pro).
Next let's see how to develop your way of working.

The precondition of developing anything is to first perceive its current state or output. If the current state of a process or a machine cannot be observed it will present itself to you as a "black box" whose inner details are a mystery. Then your only option is to implement changes and examine what changes happen e.g. in the output of the "black box".

A common problem in developing our way of working is we do not even attempt to observe it. It's not a "black box" because we could observe it. And that happens with the help of visualization.

### Visualization

Visualizing your workflow enables continuous improvement (see "Lean software development" later on).
Visualization happens using a tool of your preference. There ongoing and upcoming tasks are placed on a board - digital or physical.
The structure of a board could be a e.g. Scrum board or a Kanban board (or ScrumBan or or...).

Example board where columns are team-specific:

| ToDo                  | Planning | In Progress  | Waiting for testing | Testing | Done                |
| --------------------- | -------- | ------------ | ------------------- | ------- | ------------------- |
| WI 10<BR>WI 11<BR>... | WI 6     | WI 5<BR>WI 7 | WI 3                | WI 2    | WI 1<BR>WI 0<BR>... |

"WI" stands for "Work item" in previous example.

A [Kanban](<https://en.wikipedia.org/wiki/Kanban_(development)>) -flavoured version of previous example would include column limits (decided by the team) on how many work items each column may have at one time. It depends on the case when that is a useful approach, feel free to try it out.

Visualizing the daily and weekly work items and their flow allows an individual and team to understand the reality where they are operating.
The assumed working reality often differs from the actual reality. Visualization allows perceiving how tasks are processed by e.g. a team (or you).
If the work items and flow are not visualized, you are working on assumptions.

![reality meme I reject reality and substitute my own](/img/predicting-the-future-for-software-developers/reality-mb.gif)

Work item visualization and management tools should allow you to add value to your work. They should enable you to improve your and your team's work. If they don't, well...either you or they are not doing it right. The result in both cases is a "waste" generator.

#### Visualization enables discovering hidden work

Sometimes the amount of hidden work is surprisingly large.

First of all there are the main work items or tasks which should be accomplished. In addition to those there are all sorts of ad-hoc tasks which spring outside the team or within the team.
What typically happens is you write a "extra task" on a post-it note so that you remember to do it. This might be ok for a single trivial task...but in the other hand those tend to accumulate per person and per team.
Instead of having a second work management tool in your email/calendar/post-it note heap, why not put those in the shared work item tool to allow visualization.
When a team puts on their board as many of those tasks _as it is reasonable_, it reveals how many "extra tasks" they actually did for example during last two weeks.
That might give the team an explanation why the main tasks don't seem to have progress as expected.
The next step is to consider should some of those extra tasks be postponed and put to a "ToDo" backlog instead of implementing reactively when they were detected (refer to "Lean software development").

Another benefit gained by visualization is seeing the _dependencies_, _bottlenecks_ and _conflicts_ between work items and the team members.
Is some skillset a bottleneck? Do finished tasks return from "Testing" phase to "In progress" phase, interrupting an another task? Does someone keep feeding extra work items to team or team member "from outside"?

### Agile and Lean

_Agile way of working_ ([link](https://en.wikipedia.org/wiki/Agile_software_development)) was greeted by many in software engineering as a game-changer. Now it has been around for a while, even so that some don't know any other way. On the other hand many have only heard about it

> "Agile doesn't work! Agile means no planning! Agile means no documentation!"

Those stereotypes aren't true so do read about it. The theory is simple but practicing it is a never-ending lesson - just like life.

_Lean software development_ ([link](https://en.wikipedia.org/wiki/Lean_software_development)) is an important way of thinking and working. It aims to eliminate or replace repetitive or non-value producing phases and tasks with more efficient ones. Non-value adding phases and tasks are called "waste".
The Lean development principles are:

- Eliminate waste
- Amplify learning
- Decide as late as possible
- Deliver as fast as possible
- Empower the team
- Build integrity in
- Optimize the whole

As a concrete example, organizing the placement of tools on a workbench according to the work process eliminates waste (wasted effort and time) because the next tool is always the closest at hand.

Here in turn are a few examples from software project context:

- Deploying software to test environment differently than into production creates waste, because it enables problems which can not be detected in testing environments.
- Having the same automated source code formatting tools for each team member reduces waste when code layout and style are automatically the same, thus attention of a code inspector is not distracted to style issues.
- Have a overall plan for the whole project but postpone more detailed planning of a work item to point when it's about to be scheduled for work. Work items depend on each other and when previous items change during implementation, the too detailed planning of a later work item ends up being "waste". Postponing detailed planning must of course take into account so called "show stopper" items, e.g. it is important to work on unknowns and most risky items early on to allow adapting to surprises. So the trick here is to identify what is essential for early planning and what is not.
- Have short feedback cycle on code changes. Do a peer review (or pair programming) and integration to master/development branch as early and often as possible. Such prevents two common pitfalls:
  - _The longer you work with a work item, the harder it is to change it_ because of the emotion of "_time I spent on it already_".
  - The longer a feature is separate from "main" code-line, the more likely it is that it will not work in main code-line as it did when separate. Because of entropy.

They Agile and Lean ways of working are not processes as such, but more like ways of thinking and working.

### The "Whys"

Typically people put effort on avoiding the _bad_ things that happened to them.
That is a natural first step. After all, the first goal in swimming is to keep your nose above the water.
Just like breast stroke is for swimming, the next level for your project work is to pay attention on finding the root causes for the _positive_ events, not only for the bad things.
Don't take positive events granted, instead observe why did a task go so well. This is what teams often neglect. This is important because we want to repeat the past successes.
Nurture the environments which made them possible. Small seeds grow into big trees.
Sitting down (or having a stroll) and paying a moment to consider these topics every once in a while keeps you on the long road to success. A minute every now and then makes the difference, not three hours every three months. Just like in any other training.

Now you understand to pay attention to both negative as well as positive accomplishments.
The "Five whys" is the most elementary and easy technique for breaking down a positive or a negative event and discovering its root causes.
Do read the wikipedia article ([link](https://en.wikipedia.org/wiki/Five_whys)) about it before continuing. If there's only one thing you pick up on this blog post, make it this one.
Doing the "5 whys" takes typically only a minute or a few.

![Pirate Sparrow Why meme](/img/predicting-the-future-for-software-developers/why-sparrow.png)

![Jackie Why meme](/img/predicting-the-future-for-software-developers/why-jackie.png)

![why to meme](/img/predicting-the-future-for-software-developers/why-tho-family.png)

The wikipedia example gives you the basic idea:

- The vehicle won't start
- Why? – The battery is dead. (First why)
- Why? – The alternator is not functioning. (Second why)
- Why? – The alternator belt has broken. (Third why)
- Why? – The alternator belt was well beyond its useful service life and not replaced. (Fourth why)
- Why? – The vehicle was not maintained according to the recommended service schedule. (Fifth why, a root cause)

Here's another imaginary example from project work domain:

- Implementing the feature wasn't finished in time
- Why? - The database things took more time
- Why? - They were more complex than we expected
- Why? - We thought the feature was just a simple server logic change
- Why? - In planning phase we thought so
- Why? - We didn't break down the feature into smaller sub-tasks

Notice also how in the second example I could turn inwards and shrug off the issue by thinking I just didn't have good enough the skills for the job.
While that might be the case, it also could include other deeper root causes. Living is learning and skills improve as we go. But only if we reflect back for their root causes.
If you're lucky you might have someone coaching this to you, but don't expect to get that privilege forever. You can do this yourself every now and then. Go on, give it a try!

### Brainstorming (how to come up with great ideas)

![Got any more of them ideas?](/img/predicting-the-future-for-software-developers/ideas.png)

Previous sections discuss about how to see the way of working, its characteristics and how to find root causes.
That's all fine and dandy, but what do you do after finding out those?
Simple! If a fix is needed then just come up with a solution and do it!
Or is it...
Finding only the first solution alternative to a problem narrows our mind.
This is a generic problem-solving challenge, not unique to software engineering.
Like a shipwrecked sailor grasping a piece of driftwood, our mind locks into to the first solution which might keep us above the waves. Locking into the first solution leads to ignoring other alternatives.

If you pardon a martial analogy:
innovating and problem solving are not like getting only one bullet to hit the bullseye.
Innovating is shooting magazines of bullets to the target and then picking the best scoring shot.

The part where we trip ourselves is when we think each idea has to be a groundbreaking new way of thinking, worthy of a Nobel prize. Avoid that pitfall! Instead focus on listing a simple bulleted list of as many good _and bad_ alternatives as you can think of within a reasonable amount of time. Describe each just by using a few words, otherwise you will get stuck in them and again you won't see the forest behind the trees.
Composing several approaches gives usually a bunch of bad ones with a few hidden diamonds.

#### Three-step routine for coming up with great ideas

1. Identify

   - List down as many different solution alternatives as you can (it is up to you whether you want to spend 5min alone or an hour in a meeting with an entire team). Quantity is the key here, not quality! Don't get stuck with evaluating them as good or bad! Go for simply for listing as many ideas as you can.
   - List also solutions which absolutely can _not_ be used to solve the problem. Bad ideas count as well!

2. Evaluate

   - Walk through the list and write what pros and cons each alternative has. Write a few "+" and "-" items under each idea.

3. Review

   - Step back and look at the big picture. You probably see already an obvious best alternative, or a couple.
   - Don't lock a decision yet! Instead consider should some details of different alternatives be combined as an even better alternative or merged.
   - You may end up going with the original alternative which you had in mind before step 1, but just as well you may end up modifying it or selecting a different one.

After doing this a few times this becomes an effortless routine, a way of thinking instead of a managed process.

The bullet-list for an important decision will also act as documentation on why a specific alternative was chosen over others. That way there's a chance someone won't change to one of the absolutely bad alternatives later on.

## The System

![Charlie Chaplin CC BY-SA 2.0](/img/predicting-the-future-for-software-developers/cc-modern-times.jpg "Charlie Chapling in a mahine in Modern times")

Let's take a system-theory view to software project work.
There a system composed of people, processes and ways of working produces systems which are part of larger systems. Systems of human and non-human actors.

Let's define what we are talking about and put down some terms.

- **Project**

  - A project is an endeavor with following defined attributes (the project iron triangle):
    - Schedule
    - Budget
    - Goal
  - A project has a high risk of failing before the kickoff if any of those attributes is not clear and agreed by project stakeholders.
  - When joining a project your job is to ask what these are. You might think they don't affect your daily work at first, but they draw the line in the sand inside which you are working. The exact monetary budget might not be essential, but it _is_ essential to understand if a project is fixed price, if there's two months of money left or if there are years of maintenance in the horizon.
    It is important to understand what are the measurements used to judge if project was successful.
    These allows you to put things in perspective. For example it is waste to do those refactoring tasks if they wouldn't have a long enough lifespan.

- **Goals** are the most important thing for a project definition. It's likely there will be problems evaluating the project results if the goal(s) are not clear in the beginning. A project with a vague goal is also in danger of being cancelled halfway when a stakeholder puts up a question why the project exists. For a software project often one important goal is a delivery (see next item).

- **A delivery** is the hands-on result of a project.
  A delivery may create a new system from scratch (_e.g. implement a new web application_)
  or modify an existing system (_e.g. change the approval workflow of a travel booking system_).

- [**A system**](https://en.wikipedia.org/wiki/System) is a set of things working together.
  The Solar system is a system (it's in the name after all!).
  The calculator application in your mobile phone is a system.
  A bridge is a system.
  Systems are often composed from smaller systems.
  Systems are produced by other systems (software application vs. software project).

- **A change** is an item which alters the structure and state of a system. A change may take a system a step towards the intended goal or away from it.
  One can argue that software engineering simply produces changes to a system.
  We humans may sometimes be distracted because we value other changes more. However, a change of "lesser nature" may have just as big impact as some "important change".
  A software engineering change may implement a feature, modify existing functionality, remove functionality, fix a problem, create or alter documentation and so forth. A change is _any difference_ to previous structure, functionality or state of the system which is produced.
  Changes to system have consequences which are predicted or unpredicted.
  Often both, because systems quickly grow in complexity past human comprehension.

  - For example let's say there's an automated procedure which composes customer documentation by reading a readme file. The procedure could run into trouble due to the file format. This in turn could lead to a problem on software delivery system level because of missing or incorrect documentation, or because the software build failed.
    This way an innocent one-character change to a file - which is not involved in system run-time - may lead to problems for the people working with or within the run-time system.

(_This is where you should take a short break before you continue reading.
Go and get a cup of `[ your preferred beverage ]` and read the previous description on changes once more._
_..._<BR>
_Ready?_

_Oh well, let's continue)_

This _[holistic](https://en.wikipedia.org/wiki/Holism)_ view inspects software as part of the whole instead of a isolated unit in vacuum.
A change to system, if inspected alone without its intended habitat, may present itself as insignificant.
As part of a whole it may change considerably the functionality of a delivery or the expectations of a project.

Events encountered by a project may introduce changes to

- project (=system) which is producing the deliverable
- to the deliverable (=system)
- or a mixture of both

For example the

- schedule, goals or resourcing of a project may change
- environment of the deliverable may change
  (e.g. publish new interfaces into public internet, changes in hosting platform, change of database product)
- expectations for the deliverable may change
  (e.g. change in expected user count, change of user interface languages, changes in feature set).

What was already discussed in the "WoW" section applies also to systems an projects:
The events (changes) encountered by project may be either _favorable_ or _harmful_ depending on the project goal.
Human tendency is often to focus on the negative risks and not value something which "just works". That might not be the case next time, so identify the positive events and changes. Aim to understand their causes and to repeat them in the future.

## High stakes and stakeholders

!["well yes but actually no"](/img/predicting-the-future-for-software-developers/yes-no.png)

Typically there are many people who are not visible in developer's daily horizon.
This chapter describes typical stakeholders for a project and what impacts _a developer_ may create towards them.
Whether to implement a change using alternative A or B might seem irrelevant for developer, but impacts to stakeholders may be very different. These might not be obvious if you spend only a short time in a project, if a project is a Proof of Concept (PoC) project or if you have an overly-protective project manager.
To get started on understanding what impacts your actions have, familiarize yourself with the project stakeholder list. A project manager should have created such as part of stakeholder analysis.

**Typical categories of stakeholders**

- Business representatives
  - Delivery is typically expected to affect monetary business area(s). Areas whose representatives don't necessarily talk to each other often, which may lead to challenges on project team level.
- End users
  - Corporate users typically represented by key users. A Key user is typically an end user with wider understanding on the work processes as well as wider access rights to the system.
  - Consumer users could be represented by a person who will arrange test occasions to get end-user feedback during the project
- IT
  - Delivery has to fit into existing IT and software environment when it is deployed
  - Delivery will often be operated and maintained by a different team than the one who created it
- User support
  - End user support
  - Business-to-business support
- Marketing
  - This may be included in Business side or be a separate stakeholder
  - Internal to a corporation or external for public communications
- Training
  - End user organizations and people may require scheduling additional training, or existing training content must be updated. Changes in project content or functionality impacts training stakeholders.
- Organizational entities
  - For example line managers or corporate directors
- Project collaborators
  - A delivery may be a joint creation by different delivery teams or companies. Teams who either play along nicely or not.
- Regulations and legal
  - Delivery may have to comply to national or international regulations. Compliancy could be ensured by collaboration with a domain expert.
  - In some specific cases delivery may be a pioneering pilot project whose results will affect upcoming domain standards.
- IPR
  - Is delivery complying to Intellectual Property Rights (IPR) like existing patents and licenses?
  - Will new IPR be created for the delivery- or customer organizations? Such processes are typically managed in co-operation with a legal consult specializing in IPR process.
- Open source community
  - Delivery may affect existing open source projects or create new open source projects
  - Is market situation affected by new deliveries? Are competitors affected?

**Typical categories of impact**

1. Business impact

   - Typically there is are business stakeholders who benefit from the change which the deliverable enables. They expect monetary benefits either as new revenue, cost savings in existing operations or creation of enablers for new business opportunities.
   - For example:
     - Creating a need for more software update intervals will not be favored by a business stakeholder if software version updates costs money for the business entity (e.g. service breaks, training cost, lowered productivity due to problems).
     - Enabling localization of a product to new business/market area creates new business opportunities for business stakeholders.

1. Customer and End user impact

   - Customer and end user are listed here together, although often they are two different equally important stakeholders.
   - Will the daily life of end users become more easy or more difficult because of project delivery?
   - Will customer get satisfied end users and revenue?
   - For example:
     - corporate process cost saving when user workload is reduced
     - usability improvements decrease the demand for support resources
     - consumer solution becomes more competitive
     - positive or negative publicity e.g. in social media
     - customer satisfaction and trust levels to project team change
   - As harsh as this sounds, Customer needs and End User needs may conflict. For example corporate software may be judged by cost, schedule or political factors instead of end user usability or quality.

1. Development impact

   - How is future development work affected?
   - For example
     - a complex design will be harder to understand and alter by new developers. Or by you yourself after 6 months.
     - For an existing system a developer may spend most of one's time trying to understand old code and ensuring it doesn't break because of changes.
   - How does a specific implemented change fit to existing design and product roadmap?

     - Is the product struggling to make the first release, is a minimum viable version is enough?
     - Is the product about to enter a "end of life" phase where effort put to refactoring is waste?
     - Remember that end users don't see the code.

   - Quality assurance: automated or manual testing may become more difficult or easy. Is testing coverage improved or reduced?

1. Operations impact

   - How is operating of the delivery affected?
   - For example following operating IT team's tasks may be affected
     - Configuring, deploying or taking backups of the delivery.
     - Quality of Documentation and operating instructions
     - Automation of tasks, e.g. does IT team have to run specific scripts manually in specific order or does the delivery take care of those itself
     - Detection of error conditions and their reporting to application log, to system log or to specific monitoring solutions
     - Problem solving using documentation, application logs or other data like database content

## Final words

Thank you traveller, you have now reached the end of this journey. But remember: every ending is a new beginning.
Consider the previous viewpoints and thoughts, experiment and synthesize.

## Further reading

- [https://en.wikipedia.org/wiki/Five_whys](https://en.wikipedia.org/wiki/Five_whys)
- [https://en.wikipedia.org/wiki/System](https://en.wikipedia.org/wiki/System)
- [https://en.wikipedia.org/wiki/Systems_theory](https://en.wikipedia.org/wiki/Systems_theory)
- [https://en.wikipedia.org/wiki/Software_system](https://en.wikipedia.org/wiki/Software_system)
- [https://en.wikipedia.org/wiki/Holism](https://en.wikipedia.org/wiki/Holism)
- [https://en.wikipedia.org/wiki/Lean_software_development](https://en.wikipedia.org/wiki/Lean_software_development)
- [https://en.wikipedia.org/wiki/Agile_software_development](https://en.wikipedia.org/wiki/Agile_software_development)
- [https://en.wikipedia.org/wiki/Kanban\_(development)](<https://en.wikipedia.org/wiki/Kanban_(development)>)
