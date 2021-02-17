---
layout: post
title: Watch your dependencies (dependency confusion and other attacks)
author: lokori
excerpt: Do you know how exactly your build tool resolves your dependencies? Are you sure? Dependency confusion is yet another subtle attack that can hit you if you are not careful, but it's definitely not the only one.
tags:
- Supply chain attack
- Dependency Confusion
- BOM
---

Nowadays most software developers have set up some kind of dependency analysis to detect known security issues in outdated packages, using tools like [OWASP Dependency Check](https://owasp.org/www-project-dependency-check/), [retire.js](https://github.com/retirejs/retire.js/) and others, but **dependency confusion** is a new subtle type of attack. Is your project vulnerable to it? How can you know? Read on.

**Dependency confusion** means that a package resolver erroneously downloads a private package from a public repository. If a package (namespace) doesn't exist, anyone can create it in a public repository as there are no signature verifications. Subtle, easy to exploit and simple. And quite effective! People have made over 100k in just a few days from bug bounty programs by pwning Google, Facebook and other big companies with this. And it's not over yet - fun & profit indeed.

![Confused dog](/img/watch-your-dependencies/confused-doggy.jpg)

## How it works in a nutshell

So if you have something like **"company.auth version >= 1.0"** as a dependency and it's supposed to be downloaded just from your private repository, your build nevertheless might check for this dependency in the public repositories. And if version 1.1 exists out there, the build tool might download that, as it's a new version, leading to a catastrophe as you would give unknown 3rd party accidentally access to run code on your servers and include "interesting" functionality to the software. Would you notice? Maybe. Maybe not.

## Which tools and languages are affected

* Python (PyPi)
* Javascript (npm)
* PHP (Composer)
* Docker containers (allegedly) 
* .NET NuGet 
* There might be others that are not yet widely known.

## How to mitigate / check if you are safe 

* Visma has published a tool for PHP (Composer), Javascript (package.json) and Python: [confused](https://github.com/visma-prodsec/confused)
* Visma has also published a tool for NuGet: [ConfusedDotNet](https://github.com/visma-prodsec/ConfusedDotnet)
* Check and understand how your dependencies are resolved. Are you using **--extra-index-url** with **pip install**? If you are, you are affected.

I can't stress the latter point enough: **Try to understand how exactly your tools work.** The devil is in the details. Looking at my own experiences, [Bower](https://bower.io/) was hot years ago for Javascript dependencies (before npm), but it was actually a horrible mess introducing huge security and continuity risks. Me and my team found out the hard way when our build broke. But instead of a missing dependency we could've been pwned very badly so we were actually lucky.

If you think you know your tools inside out based on your own use cases, what about the abnormal use cases? A hacker won't run builds - unless, for something like [Cryptomining from GitHub Actions](https://dev.to/thibaultduponchelle/the-github-action-mining-attack-through-pull-request-2lmc). But an intruder might use your Python dependency manager for [privilege escalation with pip](https://www.hackingarticles.in/linux-for-pentester-pip-privilege-escalation/). Similar abuse cases can be presented for other progamming languages and package managers.

## More information

This post by Alex Birsan made this whole thing famous: (https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610)
Microsoft has also published an article about mitigating this risk: (https://azure.microsoft.com/en-gb/resources/3-ways-to-mitigate-risk-using-private-package-feeds/)

Is that all? Certainly not, the general threat model for dependency attacks provides plenty of potential: 

![Dependency threat model](/img/watch-your-dependencies/dependency-attack.png)

(Picture from Alex Birsan's article referenced earlier)

These are not new threats and I mentioned some of these in my Disobey 2018 talk, but there are even more perils for developers. Get your paranoia level up, I dare you: [Developer is an attack vector!](https://www.slideshare.net/Solita_Oy/developer-is-an-attack-vector) 

## What about the other package management systems? 

I remember discussing this with my colleague Petri Sirkkala about 10 years ago. We noticed that information about our builds leak to outside servers because the builds check dependencies. We didn't like that, but didn't think much of it because it was Java and it's not that simple to publish fake packages to Maven central repo. It was just a harmless info leak. Even earlier than that, similar issues were widely discussed in the Linux circles and they made mitigations, like signatures that we still lack here in the developer-land. But even though the issue is decades old and it was kind of solved already, history tends to repeat itself. There are so many repos and dependency systems and the world keeps changing.

