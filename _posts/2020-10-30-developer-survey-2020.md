---
layout: post
title: Solita Developer Survey 2020 - what technologies do we use and like?
author: juholei
excerpt: >
  todo
tags:
 - Software Development

---

Developer survey has now become a tradition here at Solita. Every two years we survey our developer-minded people regarding what technologies and practices we use in our every-day work. The first survey was conducted in 2016 and you can find a blog post about those results in [our previous blog post](https://dev.solita.fi/java/2016/05/13/Developers-love-spaces.html) and then in 2018 [(blog post in Finnish)](https://www.solita.fi/blogit/development-teknologiakartoitus/). This year we once again took a loot at the survey and came up with a total of 27 questions that would give us interesting insight into what we use, what we like and what could be big in the future. Comparing these results to the previous ones can also give us some information on trends - what technologies are increasing in use and what are in decline?

## Languages we use

![All languages](/img/developer-survey-2020/all_languages.png)

The first question in the survey regarding programming languages asked to list all the languages you have worked with in the previous year. JavaScript and SQL were the dominant ones: SQL is present in some form in most projects we do and JavaScript is ubiquitous in frontend and hard to miss even if you primarily use different languages for frontend. Following them were Java and Python.

Apart from languages that are used for the actual system, scripting languages like Sh/Bash (third most used overall), PowerShell and Groovy were widely used.

The following questions about main backend and frontend languages were new this year and were added to get better information on how the languages are used. As such, these can't be compared as such to previous years. Usage comparisons are then based on the question about all languages used.

![Backend languages](/img/developer-survey-2020/backend_languages.png)

Moving on to more focused questions, Java proved to be the most used language for backend development. 45% reported Java being one of the primary backend languages in ther projects. Rounding out top 3, are then Clojure with about 19% usage and Kotlin with 18%. Compared to results from 2018, percentage of Kotlin users rose from 15% to 24% (comparison based on the question of all languages used). Java and Clojure usage were both a little bit down when comparing 2020 to 2018, which could be explained by the increased usage of Clojure. Neither seem to be going away though, as shown by being top 1 and 2 used languages for backend and both are well liked (more on that later).

As this question was about backend languages, we can assume that JavaScript, TypeScript and ClojureScript here mean that they are run on NodeJS. TypeScript was then the most used language with only a slight margin over JavaScript (11% vs. 10%)

![Frontend languages](/img/developer-survey-2020/frontend_languages.png)

For frontend languages the clear number one was JavaScript with 68% usage. The other languages that have wide usage are Typescript (37%) and ClojureScript (19%). ClojureScript is an obvious choice for projects that use Clojure in the backend, so it seems those two go hand in hand quite much. CoffeeScript has a handful of users - it seems that the number has been stable compared to 2018 figures (4% overall usage in 2020 compared to 5% in 2018). Most likely it's not used for any new projects but it is still in use in some long-time project(s). PureScript also had a handful users here, which seems to be new compared to 2018.

## Languages we like
![Liked languages](/img/developer-survey-2020/liked_languages.png)
## Languages we would like to use
![Languages we would like to use](/img/developer-survey-2020/would_like_to_use_languages.png)
## Frontend frameworks
![Frontend frameworks](/img/developer-survey-2020/frontend_frameworks_and_libraries.png)
## Backend frameworks

## Platforms?

## IDEs

![Editors](/img/developer-survey-2020/editors.png)

A new question this year asked what IDEs or editors we use. Most people use several, perhaps based on what languages they are working with currently. Of course then there are also those who only use one (Emacs people wouldn't probably want to leave it for any task they need to do).

Most popular one was IntelliJ Idea and other IDEs based on it. Idea is definitely very liked for Java work and Cursive for Clojure and Android Studio for Android app development are much used too. Visual Studio Code has gathered a huge following in a relatively short time and it's no surprise being used a lot among our developers too, considering that [StackOverflow survey in 2019 ](https://insights.stackoverflow.com/survey/2019#development-environments-and-tools) had it as the most popular editor.

The eternal war between VIM and Emacs users ended this time in favor of Vim, as Vim was used by 9% and Emacs was used by 7%.

## Operating Systems

![Operating systems](/img/developer-survey-2020/operating_systems.png)

Over half of the respondents reported using macOS as their primary operating system. About a third reported using Windows and a bit over 10% used Linux. A few people reported using multiple operating systems and mostly working in virtual machines. Virtual machine usage for different use cases is probably more common than that, as the question was about the primary operating system in use and not about every operating system people use in some capacity.

## Trends

Usage of cloud platforms is on the rise and that has an impact on lots of things, like solutions used for infrastructure-as-code or CI/CD. For example, Jenkins was still the most used CI/CD solution, but its usage had dropped a quite significantly in percentage and the usage of the solutions provided by the cloud platforms, such as Code* tools in AWS were up. In infrastructure-as-code tools Ansible was still the most used, but its usage had dropped a lot and AWS CDK, Terraform etc. had a lot more usage now than two years ago (TARKISTA!!!).

TypeScript usage has increased significantly in two years. When asking for generally used programming languages, TypeScript was reported by 35% of the respondents, where in 2018 it was only used by 19%. This change also meant that JavaScript,even though still the most widely used language in general, dropped from 84% to 69% of usage.

## Conclusion
