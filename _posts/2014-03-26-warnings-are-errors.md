---
layout: post
title: Warnings are Errors
author: aautio
excerpt: You know how to treat compiler errors – just fix them. But what about compiler warnings? Here are some thoughts and suggestions.
---

We all know what to do when our compiler spits out an **error**. The error indicates that we've made a mistake somewhere. What we do with errors is obvious: fix the error to get things running again.

But what about compiler **warnings**? They indicate that there might be a problem lurking somewhere. They most often indicate a potential bug, a small mishap or some other problems.

I think we should treat warnings with the same respect and severity as errors. We should stop work and fix them immediately. We should not continue with other matters before these problems have been resolved.

If we do not fix warnings immediately, they start to pile up. After one unattended warning we soon have another one. And then we have ten of those. Soon we no longer notice when new ones arise and all the warnings have lost their meaning.

![Warnings](/img/warnings-are-errors/eclipse.jpg)

If we encounter a warning that we can not fix, then we ignore it by changing our code or tuning our development environment. We want the warning to disappear from our logs and warning lists. But at the same time we want to keep our habits simple and clean.

## Good habits need attention

Keeping our codebases clean and warning-free might sound obvious, simple and easy – just as it should. Everything is quite simple and easy when we are coding all by ourselves.

But when there are many people working as a team the culture and skills of the team matter a lot. A team won't get things done if it doesn't have some common habits and common goals.

So, how can you ensure that your codebase generates no warnings? Here are some simple approaches:

 - **One individual for the whole team.** Have one person browse through all the commits and fix all the warnings every day. (*yikes!*)
 - **Automate everything.** Set your CI build to fail on warnings.
 - **Standardize environments.** Have a controlled development environment with enforced settings for everybody. Set your IDEs to treat warnings as errors.
 - **Weekly routine for the team.** Gather the team for a short review every Friday. Browse for problems together. Tools like Sonar could help. Fix everything together at the same time. Take care of the routine.

Good habits or good code are rarely an accident. I'd love to hear your take on the subject.
