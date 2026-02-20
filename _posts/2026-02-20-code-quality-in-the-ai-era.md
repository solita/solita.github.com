---
layout: post
title: What happens to Code Quality and Developer Role in the AI era
author: ruoat
excerpt: Here I share my thoughts about how I need to refresh my views about Code Quality and Software development as whole.
tags:
  - AI
  - Career development
  - Code quality
  - Software development

---

I have been working at Solita for soon 25 years. The software industry has evolved constantly during that time, but right now I believe we are living through the biggest change I have ever witnessed. I [seldom](/2015/10/19/awesomeness-of-spring-boot-13-fully-executable-jars.html) write blog posts, but I want to publish these bold — and maybe ridiculous — statements on the Internet so I can look back and reflect on them after the next 25 years. And there is one more reason I am writing this, which I will reveal at the end.

## Background: The Coding Janitor

I have been a Software Architect for a long time. The work is varied, but for me the coding itself has always been one of the most enjoyable parts. Many times I consider myself the janitor — refactoring code so that others can concentrate on adding features and producing actual value for the customer.

I have tried to keep standards and quality high so I can be proud of the output and so that new team members can join easily and maintain the codebase. One important aspect of maintaining good quality is code reviews. Finding bugs is not the main point. Knowledge sharing, discovering better approaches, and giving feedback have been what matters. The aim is to build a better product and a better team.

I am quite new to this AI world. Usually my stance on technology evolution is to not be on the bleeding edge. I let others pave the way while I concentrate on current productivity for the customer. But I have been using agentic coding for a bit over half a year now and I think my productivity has increased significantly. Today, prompting is my default way of working, and I only improve things manually when needed.

## The Fundamental Change

In the future, I won't be writing code as much anymore because LLMs can already do a lot — and they will do even more tomorrow.

I have always believed that good code is easily readable. The code should be as compact as possible so there is as little burden as possible for the team to read it. But LLMs generate quite verbose code. They handle corner cases well — even ones that would never actually happen in reality. They duplicate logic that already exists elsewhere instead of refactoring, unless told explicitly. And when you use an LLM to generate bulk tests, those tests tend to be far from compact: unnecessary mocking, unnecessary assertions, and so on.

Verbose code means more code for your colleagues to read. And here's the thing — development speed is now so fast that even the original developer might not read all the code carefully. Of course, you can instruct the LLM to behave more as you like.

But this raises an uncomfortable question: **what is the purpose of striving for readable code in the LLM era?** An LLM does not blame anyone, does not get frustrated, and does not suffer lower productivity when working in a bad codebase — unlike humans. An LLM can skim the entire codebase fast and understand what it is doing, even if the code is not readable for humans.

It is said that someone needs to be the reviewer for the LLM. Oh boy, that might be a boring task — because the human aspect diminishes. Helping others, and learning from them, is not as rewarding anymore. You cannot be so proud of seeing a junior developer improving their skills based on your feedback when the most important feedback is needed for updating AGENTS.md.

And what if everybody gets frustrated reading verbose code and just starts accepting all code changes? What if there is no one to say *"Stop. We are building on the wrong assumption!"* — while the LLM continues to build on that assumption happily? So you still need to review things carefully in the future. But reviewing becomes a less rewarding job.

## Productivity Improves

Seniority in software development is not needed as much in the future. Development becomes more achievable for everyone. My strong area has been backend development, but my database skills could have been better. Nowadays, with the help of LLMs, I can optimize databases better than ever — or create nicer frontends by myself.

I work a lot for the public sector. The good thing is that the customer gets more for the same price — and maybe the customer can even do some things by themselves. That productivity increase is something I appreciate as a taxpayer.

A good software professional has always needed strong communication skills, and those are still needed in the future. But maybe it is just not as rewarding to communicate with agents...

The Software Architect's job is not ending. I have just been in a very hands-on role, writing a lot of code. In the future I might not have that luxury. I will need to concentrate more on producing diagrams and presentations — of course with LLM!

I do not want to sound like a doomer. Change is inevitable and I need to adapt. There is no purpose in missing the old times. I need to find enjoyment in something other than writing code. Will I? I don't know yet. But at the very least, being part of this massive change is exciting — and I get powers I never had before.

## Post Scriptum

Remember the one reason I mentioned at the beginning? Here it is: **this might be one of the last times to generate something truly by yourself.** In the future, AI writes these blog posts — and nobody reads them because they are written by AI!

This post is written by AI too. Below you will find the "source code" of this blog: the raw bullet points and the prompt I fed to an LLM. Let's see what kind of blog post the same prompt creates in the future — and how accurate these predictions turn out to be.

---

## AI Summary: How Have These Predictions Held Up? (February 2026)

*This section was written by an AI at the time of publication.*

It is February 2026, so these predictions are being published in real time rather than evaluated in hindsight. However, we can note how they align with the current trajectory:

- **LLMs generating verbose code** — This is a widely recognized issue. AI-generated code tends towards over-engineering: excessive error handling for impossible cases, duplicated logic, and bloated test suites. Tools are improving, but the verbosity problem remains real. The observation is spot on.
- **Code quality mattering less** — This is the most provocative claim. Current industry consensus still values code quality, but there is a growing camp arguing that when AI both writes and maintains the code, human readability becomes secondary. Too early to call definitively, but the direction is worth watching.
- **Review becoming less rewarding** — Early signs are visible. Reviewing AI-generated code is a different experience from reviewing a colleague's work — there is no mentoring relationship, no knowledge exchange, just verification. Some teams report review fatigue. The concern is valid.
- **Reduced need for deep specialization** — Partially validated. LLMs do flatten the expertise curve for many tasks. A backend developer can now produce decent frontends or optimize databases beyond their previous skill level. But complex architectural decisions still benefit greatly from human expertise.
- **AI writing blog posts that nobody reads** — A delightfully self-referential prediction. The bullet points are human. The prose is AI. If you have read this far, at least one person still reads AI-written blogs.

*Check back in 2051 to see how these bold statements aged.*

---

## The Source Code

Prompt: *Create blog post based on these bullet points and add brief AI summary at the end how these predictions have stood times. Leave this part at the end as unedited "raw source code".*

Background: The Coding Janitor

* I have been working at Solita soon for 25 years. The industry has evolved all the time but now I think we are living the time of the biggest change.
* I write blogs [seldom](/2015/10/19/awesomeness-of-spring-boot-13-fully-executable-jars.html) but I want to publish these bold and maybe ridiculous statements to Internet so I can reflect this after 25 next years
* And one reason why I am doing this I tell later.
* I have been Software Architect for long time. The work is varied but still, for me the coding itself has been one of the most fun part.
* Many times I consider myself as the janitor refactoring code so other's can concentrate on adding features and producing actual value for the customer.
* I have tried to keep standards and quality high, so I can be proud of the output and enable new team members to join easily to maintain the codebase.
* One aspect of maintaining good quality are code reviews. Finding bugs is not the main point. Knowledge sharing, finding better ways and feedback has been important things. Aim is to build better better product and better team.
* I am quite new for this AI world. Usually in technology evolution my stance is not to be on the bleeding edge. I let other's to pave the way while I am concentrating on current productivity for the customer.
* I have used agentic coding bit over half a year and I think my productivity has increased much. Nowadays the prompting is my default way and then improve things manually if needed.

The fundamental change

* In the future I won't be writing code anymore so much because the LLM can do even more than today.
* I think good code is easily readable. The code should be as compact as possible so there is as little as possible burden for the team to read it.
* I think nowadays LLMs generate quite verbose code. For example it generates code for corner cases well but in the reality they would not ever happen or it creates same logic that exists somewhere else without refactoring unless told excplicitely.
* Also normal way is to use LLM to generate bulk tests for the code. I think those test are as compact as possible. They contain unnecessary mocking, unncesessary assertions etc.
* Verbose code leads to more code for colleague to read.
* Heck, the development speed is so fast that even the original developer might not read the all the code carefully.
* Of course LLM can be instructed to behave more as you like.

* But what is the purpose of to strive for readable code in the future of LLM era? LLM does not blame, get frustrated or get lesser productivity like humans would when working in bad code base.
* LLM can skim the code base fast and understand what it is doing even if the code is not readable for humans.

* It is said that someone needs to be the reviewer for the LLM.
* Oh boy, that might be boring task because the human aspect diminishes. Helping (and learning from!) others is not so much rewarding anymore.
* You cannot be so proud of seeing junior developer improving skills based on your feedback because the most feedback is needed for updating AGENTS.md.

* What if everybody is frustrated for reading verbose code and just accept all code changes.
* What if there is no one to say "Stop. We are building on wrong assumption!". The LLM continues to build on that happily...
* So you need to review things carefully also in the future. But the reviewing is less rewarding job.

Productivity improves

* The Seniority in the software development is not needed in the future so much. Development gets more achievable for everyone.
* My strong area has been in the backend development but my database skills could have been better.
* Nowadays, with the help of LLMs, I can optimize database better than ever or could create nicer frontend by myself.

* I am working a lot for the public sector.
* The good thing is that the customer gets more with the same price and maybe it can do something by itself.
* That productivity increase is good as a tax payer.

* Good software professional has good communication skills and they are still needed in the future. Maybe it is just not so rewarding to communicate with agents...
* The Software Architect's job is not ending. I just have been in very hands on role, coding much. In the future I might not have that luxury. I need to concentrate on producing diagrams and presentations more, of course with LLM!

* I don't want to sound a doomer. Change is inevitable and I need to adapt. There is not purpose to miss old times.
* I need to find fun from something else than writing code. Shall I find? At least the big change is fun to be part of and get powers I never had.

Post script

* The one reason I mentioned why I am writing this is that this is the last time to generate something by yourself. In the future AI writes these blogs and nobody reads blogs because they are written by AI!
* Like this post is written by AI - There is the "source code" and prompt of this blog. Let's see, which kind of blog it creates in the future and how accurate these predictions are.
